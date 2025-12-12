#!/usr/bin/env python3
"""使用 Playwright 下载 JIRA 附件的模块.

当 JIRA API 直接下载失败时（例如返回 HTML 登录页面），
使用 Playwright 模拟浏览器登录后下载真实附件。
"""
import logging
import os
from typing import Optional
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from .config import jira_settings

logger = logging.getLogger(__name__)


def is_html_content(content: bytes) -> bool:
    """检查内容是否是 HTML 页面.

    Args:
        content: 要检查的二进制内容

    Returns:
        bool: 如果是 HTML 内容返回 True
    """
    # 检查前 1000 字节
    sample = content[:1000].lower()

    # 检查常见的 HTML 标记
    html_indicators = [
        b'<!doctype html',
        b'<html',
        b'<head>',
        b'<body>',
        b'<title>',
    ]

    return any(indicator in sample for indicator in html_indicators)


def is_valid_image(content: bytes, expected_type: str) -> bool:
    """验证内容是否是有效的图片格式.

    Args:
        content: 要检查的二进制内容
        expected_type: 期望的 MIME 类型（如 image/png）

    Returns:
        bool: 如果是有效的图片格式返回 True
    """
    if len(content) < 8:
        return False

    # 检查文件头
    if expected_type == "image/png":
        # PNG 文件头: 89 50 4E 47 0D 0A 1A 0A
        return content[:8] == b'\x89PNG\r\n\x1a\n'
    elif expected_type in ["image/jpeg", "image/jpg"]:
        # JPEG 文件头: FF D8 FF
        return content[:3] == b'\xff\xd8\xff'
    elif expected_type == "image/gif":
        # GIF 文件头: GIF87a 或 GIF89a
        return content[:6] in [b'GIF87a', b'GIF89a']
    elif expected_type == "image/webp":
        # WebP 文件头: RIFF....WEBP
        return content[:4] == b'RIFF' and content[8:12] == b'WEBP'

    # 对于其他类型，不进行验证
    return True


def is_valid_content(content: bytes, mime_type: str) -> bool:
    """验证下载的内容是否有效（不是 HTML 登录页面）.

    Args:
        content: 下载的二进制内容
        mime_type: 期望的 MIME 类型

    Returns:
        bool: 如果内容有效返回 True
    """
    # 首先检查是否是 HTML 内容
    if is_html_content(content):
        logger.warning("检测到 HTML 内容，可能是登录页面")
        return False

    # 对于图片文件，进行额外验证
    if mime_type.startswith("image/"):
        return is_valid_image(content, mime_type)

    return True


async def download_attachment_with_playwright(
    attachment_url: str,
    file_path: str,
    jira_username: Optional[str] = None,
    jira_password: Optional[str] = None,
    jira_server_url: Optional[str] = None,
) -> bool:
    """使用 Playwright 登录 JIRA 并下载附件.

    Args:
        attachment_url: 附件的完整 URL
        file_path: 保存附件的本地路径
        jira_username: JIRA 用户名（默认从配置读取）
        jira_password: JIRA 密码（默认从配置读取）
        jira_server_url: JIRA 服务器 URL（默认从配置读取）

    Returns:
        bool: 下载成功返回 True，失败返回 False
    """
    # 使用默认配置
    username = jira_username or os.getenv("JIRA_USERNAME")
    password = jira_password or os.getenv("JIRA_PASSWORD")
    server_url = jira_server_url or jira_settings.server_url

    if not username or not password:
        logger.error("缺少 JIRA 用户名或密码，无法使用 Playwright 下载")
        return False

    async def login(page, timeout):
        """执行 JIRA 登录操作."""
        try:
            await page.get_by_label("输入用户名").fill(username)
            await page.get_by_label("输入密码").fill(password)
            await page.get_by_role("button", name="LOGIN").click()
            await page.wait_for_load_state('networkidle', timeout=timeout)

            # 检查是否登录成功
            if not page.url.startswith(server_url):
                logger.warning(f"{attachment_url}, 登录失败，请检查用户名和密码")
                return False
            return True
        except Exception as e:
            logger.error(f"登录过程出错: {e}")
            return False

    async with async_playwright() as p:
        browser = None
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                accept_downloads=True,
                ignore_https_errors=True
            )

            # 开始追踪（用于调试，默认禁用）
            enable_tracing = os.getenv("JIRA_ENABLE_TRACING", "false").lower() == "true"
            if enable_tracing:
                await context.tracing.start(
                    screenshots=True,
                    snapshots=True,
                    sources=True
                )
                logger.debug("Playwright 追踪已启用")

            page = await context.new_page()
            timeout = 30000

            # 访问 JIRA 首页
            logger.info(f"访问 JIRA: {server_url}")
            await page.goto(server_url, timeout=timeout)
            await page.wait_for_load_state('networkidle', timeout=timeout)

            # 如果需要登录
            if page.url.startswith("https://sso.chinawayltd.com") or "login" in page.url.lower():
                logger.info("检测到需要登录，开始登录...")
                if not await login(page, timeout):
                    logger.error("登录失败")
                    return False
                logger.info("登录成功")

            # 尝试直接下载
            try:
                logger.info(f"使用 Playwright 下载附件: {attachment_url}")
                response = await context.request.get(attachment_url, timeout=timeout)

                if response.ok:
                    with open(file_path, 'wb') as f:
                        f.write(await response.body())
                    logger.info(f"附件已保存到: {file_path}")
                    return True
                else:
                    logger.warning(f"下载失败，状态码: {response.status}")

            except Exception as e:
                logger.warning(f"直接下载失败: {e}，尝试通过页面下载")

                # 如果直接下载失败，尝试通过页面触发下载
                async with page.expect_download(timeout=timeout) as download_info:
                    await page.goto(attachment_url, timeout=timeout)

                download = await download_info.value
                await download.save_as(file_path)
                logger.info(f"附件已下载到: {file_path}")
                return True

        except Exception as e:
            logger.error(f"Playwright 下载失败: {e}")
            return False

        finally:
            if browser:
                try:
                    # 保存追踪信息（用于调试，仅在启用时）
                    enable_tracing = os.getenv("JIRA_ENABLE_TRACING", "false").lower() == "true"
                    if enable_tracing:
                        trace_path = os.path.join(os.path.dirname(file_path), "trace.zip")
                        await context.tracing.stop(path=trace_path)
                        logger.debug(f"追踪信息已保存到: {trace_path}")
                except:
                    pass
                await browser.close()
