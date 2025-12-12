"""attachment_downloader 模块的单元测试.

测试 JIRA 附件下载功能，包括内容验证和 Playwright 下载。
"""
import os
from unittest.mock import Mock, MagicMock, AsyncMock, patch

import pytest

from jira_mcp.attachment_downloader import (
    is_html_content,
    is_valid_image,
    is_valid_content,
    download_attachment_with_playwright,
)


class TestIsHtmlContent:
    """测试 is_html_content 函数."""

    def test_detect_html_with_doctype(self):
        """检测到 <!doctype html> 应返回 True"""
        # Arrange
        content = b"<!doctype html><html><body>Login Page</body></html>"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is True

    def test_detect_html_with_html_tag(self):
        """检测到 <html> 标签应返回 True"""
        # Arrange
        content = b"<html><head><title>Page</title></head></html>"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is True

    def test_detect_html_with_head_tag(self):
        """检测到 <head> 标签应返回 True"""
        # Arrange
        content = b"some text <head><meta charset='utf-8'></head>"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is True

    def test_detect_html_with_body_tag(self):
        """检测到 <body> 标签应返回 True"""
        # Arrange
        content = b"random content <body><p>Text</p></body>"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is True

    def test_detect_html_with_title_tag(self):
        """检测到 <title> 标签应返回 True"""
        # Arrange
        content = b"prefix <title>Login Page</title> suffix"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is True

    def test_detect_html_case_insensitive(self):
        """HTML 标签检测应不区分大小写"""
        # Arrange
        content = b"<!DOCTYPE HTML><HTML><BODY>Content</BODY></HTML>"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is True

    def test_non_html_binary_content_should_return_false(self):
        """非 HTML 二进制内容应返回 False"""
        # Arrange
        content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is False

    def test_plain_text_content_should_return_false(self):
        """纯文本内容应返回 False"""
        # Arrange
        content = b"This is plain text without any HTML tags"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is False

    def test_empty_content_should_return_false(self):
        """空内容应返回 False"""
        # Arrange
        content = b""

        # Act
        result = is_html_content(content)

        # Assert
        assert result is False

    def test_html_beyond_1000_bytes_should_not_be_detected(self):
        """超过 1000 字节后的 HTML 标签不应被检测到"""
        # Arrange
        padding = b"x" * 1001
        content = padding + b"<html><body>HTML</body></html>"

        # Act
        result = is_html_content(content)

        # Assert
        assert result is False


class TestIsValidImage:
    """测试 is_valid_image 函数."""

    # PNG 测试
    def test_valid_png_image_should_return_true(self):
        """有效的 PNG 图片应返回 True"""
        # Arrange
        content = b"\x89PNG\r\n\x1a\n" + b"additional data"
        expected_type = "image/png"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is True

    def test_invalid_png_header_should_return_false(self):
        """无效的 PNG 文件头应返回 False"""
        # Arrange
        content = b"\x89PNG\r\n\x00\x00" + b"wrong header"
        expected_type = "image/png"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is False

    # JPEG 测试
    @pytest.mark.parametrize("mime_type", ["image/jpeg", "image/jpg"])
    def test_valid_jpeg_image_should_return_true(self, mime_type):
        """有效的 JPEG 图片应返回 True"""
        # Arrange
        content = b"\xff\xd8\xff" + b"JPEG data"

        # Act
        result = is_valid_image(content, mime_type)

        # Assert
        assert result is True

    def test_invalid_jpeg_header_should_return_false(self):
        """无效的 JPEG 文件头应返回 False"""
        # Arrange
        content = b"\xff\xd8\x00" + b"wrong header"
        expected_type = "image/jpeg"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is False

    # GIF 测试
    @pytest.mark.parametrize("gif_header", [b"GIF87a", b"GIF89a"])
    def test_valid_gif_image_should_return_true(self, gif_header):
        """有效的 GIF 图片应返回 True"""
        # Arrange
        content = gif_header + b"GIF data"
        expected_type = "image/gif"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is True

    def test_invalid_gif_header_should_return_false(self):
        """无效的 GIF 文件头应返回 False"""
        # Arrange
        content = b"GIF90a" + b"wrong version"
        expected_type = "image/gif"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is False

    # WebP 测试
    def test_valid_webp_image_should_return_true(self):
        """有效的 WebP 图片应返回 True"""
        # Arrange
        content = b"RIFF\x00\x00\x00\x00WEBP" + b"WebP data"
        expected_type = "image/webp"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is True

    def test_invalid_webp_riff_header_should_return_false(self):
        """RIFF 头无效的 WebP 应返回 False"""
        # Arrange
        content = b"RIFF\x00\x00\x00\x00JPEG" + b"not webp"
        expected_type = "image/webp"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is False

    # 边界条件测试
    def test_content_less_than_8_bytes_should_return_false(self):
        """内容少于 8 字节应返回 False"""
        # Arrange
        content = b"\x89PNG\r"  # 只有 5 字节
        expected_type = "image/png"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is False

    def test_empty_content_should_return_false(self):
        """空内容应返回 False"""
        # Arrange
        content = b""
        expected_type = "image/png"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is False

    def test_unknown_image_type_should_return_true(self):
        """未知图片类型应返回 True（不进行验证）"""
        # Arrange
        content = b"any content here"
        expected_type = "image/unknown"

        # Act
        result = is_valid_image(content, expected_type)

        # Assert
        assert result is True


class TestIsValidContent:
    """测试 is_valid_content 函数."""

    def test_valid_png_content_should_return_true(self):
        """有效的 PNG 内容应返回 True"""
        # Arrange
        content = b"\x89PNG\r\n\x1a\n" + b"PNG data"
        mime_type = "image/png"

        # Act
        result = is_valid_content(content, mime_type)

        # Assert
        assert result is True

    def test_html_content_should_return_false(self):
        """HTML 内容应返回 False"""
        # Arrange
        content = b"<!doctype html><html><body>Login Page</body></html>"
        mime_type = "image/png"

        # Act
        result = is_valid_content(content, mime_type)

        # Assert
        assert result is False

    def test_invalid_image_format_should_return_false(self):
        """无效的图片格式应返回 False"""
        # Arrange
        content = b"INVALID IMAGE DATA"
        mime_type = "image/png"

        # Act
        result = is_valid_content(content, mime_type)

        # Assert
        assert result is False

    def test_valid_non_image_content_should_return_true(self):
        """有效的非图片内容应返回 True"""
        # Arrange
        content = b"PDF file content or other binary data"
        mime_type = "application/pdf"

        # Act
        result = is_valid_content(content, mime_type)

        # Assert
        assert result is True

    def test_html_with_non_image_mime_should_return_false(self):
        """HTML 内容（即使 MIME 类型不是图片）应返回 False"""
        # Arrange
        content = b"<html><body>Login</body></html>"
        mime_type = "application/pdf"

        # Act
        result = is_valid_content(content, mime_type)

        # Assert
        assert result is False


@pytest.mark.asyncio
class TestDownloadAttachmentWithPlaywright:
    """测试 download_attachment_with_playwright 函数."""

    @pytest.fixture
    def mock_playwright(self):
        """创建 Playwright mock"""
        with patch("jira_mcp.attachment_downloader.async_playwright") as mock:
            # 创建 mock 对象链
            playwright_mock = MagicMock()
            browser_mock = MagicMock()
            context_mock = MagicMock()
            page_mock = MagicMock()
            request_mock = MagicMock()
            response_mock = MagicMock()

            # 设置异步上下文管理器
            mock.return_value.__aenter__.return_value = playwright_mock
            mock.return_value.__aexit__.return_value = AsyncMock(return_value=None)

            # 设置异步返回值
            playwright_mock.chromium.launch = AsyncMock(return_value=browser_mock)
            browser_mock.new_context = AsyncMock(return_value=context_mock)
            browser_mock.close = AsyncMock()
            context_mock.new_page = AsyncMock(return_value=page_mock)
            context_mock.request.get = AsyncMock(return_value=response_mock)
            context_mock.tracing.start = AsyncMock()
            context_mock.tracing.stop = AsyncMock()
            page_mock.goto = AsyncMock()
            page_mock.wait_for_load_state = AsyncMock()
            page_mock.get_by_label = MagicMock(return_value=MagicMock(fill=AsyncMock()))
            page_mock.get_by_role = MagicMock(return_value=MagicMock(click=AsyncMock()))
            response_mock.ok = True
            response_mock.body = AsyncMock(return_value=b"attachment content")

            yield {
                "async_playwright": mock,
                "playwright": playwright_mock,
                "browser": browser_mock,
                "context": context_mock,
                "page": page_mock,
                "response": response_mock,
            }

    @pytest.fixture
    def temp_file_path(self, tmp_path):
        """创建临时文件路径"""
        return str(tmp_path / "test_attachment.png")

    async def test_download_success_with_credentials(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """提供凭证时应成功下载附件"""
        # Arrange
        monkeypatch.setenv("JIRA_USERNAME", "test_user")
        monkeypatch.setenv("JIRA_PASSWORD", "test_pass")
        attachment_url = "http://jira.example.com/attachment/123"

        # Act
        result = await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        assert result is True
        assert os.path.exists(temp_file_path)
        with open(temp_file_path, "rb") as f:
            assert f.read() == b"attachment content"

    async def test_download_without_credentials_should_fail(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """缺少凭证时应失败"""
        # Arrange
        monkeypatch.delenv("JIRA_USERNAME", raising=False)
        monkeypatch.delenv("JIRA_PASSWORD", raising=False)
        attachment_url = "http://jira.example.com/attachment/123"

        # Act
        result = await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        assert result is False
        assert not os.path.exists(temp_file_path)

    async def test_download_with_explicit_credentials(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """显式传递凭证时应成功下载"""
        # Arrange
        monkeypatch.delenv("JIRA_USERNAME", raising=False)
        monkeypatch.delenv("JIRA_PASSWORD", raising=False)
        attachment_url = "http://jira.example.com/attachment/123"

        # Act
        result = await download_attachment_with_playwright(
            attachment_url,
            temp_file_path,
            jira_username="explicit_user",
            jira_password="explicit_pass",
        )

        # Assert
        assert result is True
        assert os.path.exists(temp_file_path)

    async def test_request_exception_should_fallback_to_page_download(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """直接请求失败时应回退到页面下载"""
        # Arrange
        monkeypatch.setenv("JIRA_USERNAME", "test_user")
        monkeypatch.setenv("JIRA_PASSWORD", "test_pass")
        attachment_url = "http://jira.example.com/attachment/123"

        # 模拟直接下载抛出异常，触发页面下载
        mock_playwright["context"].request.get.side_effect = Exception("Connection error")

        # Mock 页面下载成功
        download_mock = MagicMock()
        download_mock.save_as = AsyncMock()

        # 创建一个返回 download_mock 的 coroutine
        async def get_download():
            return download_mock

        download_info_mock = MagicMock()
        download_info_mock.value = get_download()

        # 创建异步 context manager mock
        expect_download_cm = MagicMock()
        expect_download_cm.__aenter__ = AsyncMock(return_value=download_info_mock)
        expect_download_cm.__aexit__ = AsyncMock(return_value=None)
        mock_playwright["page"].expect_download.return_value = expect_download_cm

        # Act
        result = await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        assert result is True
        download_mock.save_as.assert_called_once_with(temp_file_path)
        # 验证 page.goto 被调用了两次：首页 + 附件下载
        assert mock_playwright["page"].goto.call_count == 2
        # 验证最后一次调用是下载附件
        last_call = mock_playwright["page"].goto.call_args
        assert last_call[0][0] == attachment_url
        assert last_call[1]["timeout"] == 30000

    async def test_browser_exception_should_return_false(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """浏览器异常时应返回 False"""
        # Arrange
        monkeypatch.setenv("JIRA_USERNAME", "test_user")
        monkeypatch.setenv("JIRA_PASSWORD", "test_pass")
        attachment_url = "http://jira.example.com/attachment/123"

        # 模拟浏览器启动失败
        mock_playwright["playwright"].chromium.launch.side_effect = Exception(
            "Browser launch failed"
        )

        # Act
        result = await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        assert result is False

    async def test_chromium_launched_in_headless_mode(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """Chromium 应以 headless 模式启动"""
        # Arrange
        monkeypatch.setenv("JIRA_USERNAME", "test_user")
        monkeypatch.setenv("JIRA_PASSWORD", "test_pass")
        attachment_url = "http://jira.example.com/attachment/123"

        # Act
        await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        mock_playwright["playwright"].chromium.launch.assert_called_once()
        call_kwargs = mock_playwright["playwright"].chromium.launch.call_args[1]
        assert call_kwargs["headless"] is True

    async def test_browser_context_accepts_downloads(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """浏览器上下文应允许下载"""
        # Arrange
        monkeypatch.setenv("JIRA_USERNAME", "test_user")
        monkeypatch.setenv("JIRA_PASSWORD", "test_pass")
        attachment_url = "http://jira.example.com/attachment/123"

        # Act
        await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        mock_playwright["browser"].new_context.assert_called_once()
        call_kwargs = mock_playwright["browser"].new_context.call_args[1]
        assert call_kwargs["accept_downloads"] is True
        assert call_kwargs["ignore_https_errors"] is True

    async def test_browser_closed_after_download(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """下载完成后应关闭浏览器"""
        # Arrange
        monkeypatch.setenv("JIRA_USERNAME", "test_user")
        monkeypatch.setenv("JIRA_PASSWORD", "test_pass")
        attachment_url = "http://jira.example.com/attachment/123"

        # Act
        await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        mock_playwright["browser"].close.assert_called_once()

    async def test_browser_closed_even_on_exception(
        self, mock_playwright, temp_file_path, monkeypatch
    ):
        """即使发生异常，浏览器也应关闭"""
        # Arrange
        monkeypatch.setenv("JIRA_USERNAME", "test_user")
        monkeypatch.setenv("JIRA_PASSWORD", "test_pass")
        attachment_url = "http://jira.example.com/attachment/123"

        # 模拟异常
        mock_playwright["context"].request.get.side_effect = Exception("Download error")

        # Act
        await download_attachment_with_playwright(attachment_url, temp_file_path)

        # Assert
        mock_playwright["browser"].close.assert_called_once()
