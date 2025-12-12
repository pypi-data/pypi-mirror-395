#!/usr/bin/env python3
import argparse
import logging
import os
import base64
import pathlib
import requests
from typing import Dict, List, Any, Optional

from jira import JIRA
from mcp.server.fastmcp import FastMCP
from .config import get_jira_auth, jira_settings, devlake_settings
from .attachment_downloader import (
    is_valid_content,
    download_attachment_with_playwright,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 创建MCP服务器
mcp = FastMCP("JIRA MCP Server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))

# 工具加载控制
def conditional_tool(description: str, always_load: bool = False):
    """条件工具装饰器

    Args:
        description: 工具描述
        always_load: 是否总是加载（核心工具）
    """
    def decorator(func):
        # 延迟检查环境变量，而不是在模块导入时读取
        load_all_tools = os.getenv("JIRA_LOAD_ALL_TOOLS", "false").lower() == "true"
        if always_load or load_all_tools:
            return mcp.tool(description=description)(func)
        return func
    return decorator

# JIRA客户端
jira_client = None

# JIRA附件保存目录（保存到当前工作目录的 .jira-mcp 子目录）
ATTACHMENTS_DIR = os.path.join(os.getcwd(), ".jira-mcp")
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

# 字段黑名单 - 这些字段不会在format_issue中返回
FIELD_BLACKLIST = {
    "customfield_10009",
    "customfield_11314",  # 是否有子任务
    "customfield_11315",  # 设计支持方式
    "customfield_11316",  # 开发支持方式
    "customfield_11604",  # 公告范围
    "customfield_11608",  # 解决进度
    "customfield_11612",  # 优化进度
    "customfield_12000",  # 开发
    "customfield_12411",
    "customfield_12436",  # 需求是否变更
    "customfield_12446",  # 提测是否延期
    "customfield_12451",
    "customfield_12538",
    "customfield_12539",
    "customfield_12610",  # Resolution Time Custom Field
    "customfield_12612",
    "customfield_12527",  # 业务方是否确认
    "customfield_12640",  # 否
    "customfield_12641",  # 否
    "customfield_12646",
    "customfield_12651",
    "customfield_12652",
    "customfield_12613", # 线上问题分类
}


def get_attachment_path(issue_key: str, filename: str) -> str:
    """获取附件在本地文件系统中的保存路径."""
    # 创建问题专属目录
    issue_dir = os.path.join(ATTACHMENTS_DIR, issue_key)
    os.makedirs(issue_dir, exist_ok=True)
    return os.path.join(issue_dir, filename)


def get_jira_client() -> JIRA:
    """获取JIRA客户端实例."""
    global jira_client
    if jira_client is None:
        auth = get_jira_auth()
        jira_client = JIRA(server=jira_settings.server_url, basic_auth=auth)
    return jira_client


def format_issue(issue, client: JIRA = None) -> Dict[str, Any]:
    """格式化JIRA问题为JSON友好格式.

    Args:
        issue: JIRA问题对象
        client: JIRA客户端，用于获取字段定义
    """
    fields = issue.fields

    result = {
        "id": issue.id,
        "key": issue.key,
        "self": issue.self,
        "summary": fields.summary,
        "description": fields.description or "",
        "status": {
            "id": fields.status.id,
            "name": fields.status.name,
            "description": fields.status.description,
        },
        "project": {
            "id": fields.project.id,
            "key": fields.project.key,
            "name": fields.project.name,
        },
        "created": fields.created,
        "updated": fields.updated,
    }

    # 添加可选字段
    if hasattr(fields, "assignee") and fields.assignee:
        result["assignee"] = {
            "name": fields.assignee.name,
            "display_name": fields.assignee.displayName,
            "email": getattr(fields.assignee, "emailAddress", ""),
        }

    if hasattr(fields, "reporter") and fields.reporter:
        result["reporter"] = {
            "name": fields.reporter.name,
            "display_name": fields.reporter.displayName,
            "email": getattr(fields.reporter, "emailAddress", ""),
        }

    if hasattr(fields, "issuetype") and fields.issuetype:
        result["issue_type"] = {
            "id": fields.issuetype.id,
            "name": fields.issuetype.name,
            "description": fields.issuetype.description,
        }

    if hasattr(fields, "priority") and fields.priority:
        result["priority"] = {
            "id": fields.priority.id,
            "name": fields.priority.name,
        }

    if hasattr(fields, "components") and fields.components:
        result["components"] = [
            {"id": c.id, "name": c.name} for c in fields.components
        ]

    if hasattr(fields, "labels") and fields.labels:
        result["labels"] = fields.labels

    # 处理附件 - JIRA API 使用 "attachment" 字段
    if hasattr(fields, "attachment") and fields.attachment:
        result["attachments"] = [
            {
                "id": attachment.id,
                "filename": attachment.filename,
                "size": attachment.size,
                "content_type": attachment.mimeType,
                "created": attachment.created,
                "url": attachment.content
            }
            for attachment in fields.attachment
        ]

    # 获取自定义字段
    def serialize_value(value):
        """将 JIRA 对象转换为可 JSON 序列化的格式."""
        if value is None:
            return None
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, list):
            return [serialize_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: serialize_value(v) for k, v in value.items()}
        elif hasattr(value, 'value'):
            # CustomFieldOption 等对象通常有 value 属性
            return value.value
        elif hasattr(value, 'name'):
            # 很多 JIRA 对象有 name 属性
            return value.name
        elif hasattr(value, '__dict__'):
            # 其他对象转为字符串
            return str(value)
        else:
            return str(value)

    # 获取自定义字段，排除黑名单中的字段
    for field_name in dir(fields):
        if field_name.startswith("customfield_") and field_name not in FIELD_BLACKLIST:
            value = getattr(fields, field_name)
            if value is not None:
                result[field_name] = serialize_value(value)

    # 获取字段名称映射 - 只返回自定义字段(customfield_*)
    if client:
        try:
            # 获取所有字段定义
            all_fields = client.fields()
            field_name_map = {f["id"]: f["name"] for f in all_fields}

            # 只保留当前 issue 有值的自定义字段，排除黑名单
            custom_field_names = {}
            for field_name in dir(fields):
                if not field_name.startswith('customfield_'):
                    continue
                if field_name in FIELD_BLACKLIST:
                    continue
                value = getattr(fields, field_name, None)
                if value is not None and field_name in field_name_map:
                    custom_field_names[field_name] = field_name_map[field_name]

            result["custom_field_names"] = custom_field_names
        except Exception as e:
            logger.warning(f"获取字段名称映射失败: {str(e)}")

    return result


def format_comment(comment) -> Dict[str, Any]:
    """格式化JIRA评论对象为JSON友好格式.

    Args:
        comment: JIRA评论对象

    Returns:
        Dict[str, Any]: 格式化后的评论数据
    """
    result = {
        "id": comment.id,
        "body": comment.body or "",
        "created": comment.created,
        "updated": comment.updated,
    }

    # 添加作者信息
    if hasattr(comment, "author") and comment.author:
        result["author"] = {
            "name": getattr(comment.author, "name", ""),
            "display_name": getattr(comment.author, "displayName", ""),
            "email": getattr(comment.author, "emailAddress", ""),
        }

    # 添加更新者信息
    if hasattr(comment, "updateAuthor") and comment.updateAuthor:
        result["update_author"] = {
            "name": getattr(comment.updateAuthor, "name", ""),
            "display_name": getattr(comment.updateAuthor, "displayName", ""),
            "email": getattr(comment.updateAuthor, "emailAddress", ""),
        }

    # 添加可见性信息
    if hasattr(comment, "visibility") and comment.visibility:
        result["visibility"] = {
            "type": getattr(comment.visibility, "type", ""),
            "value": getattr(comment.visibility, "value", ""),
        }

    return result


@conditional_tool(description="获取JIRA问题详情", always_load=True)
def get_issue(
    issue_key: str,
    include_comments: bool = True,
) -> Dict[str, Any]:
    """获取JIRA问题详情.

    Args:
        issue_key: JIRA问题键
        include_comments: 是否包含评论（默认True）

    Returns:
        Dict[str, Any]: 问题详情（可选包含评论）
    """
    logger.info(f"获取问题: {issue_key}, include_comments={include_comments}")
    try:
        client = get_jira_client()
        issue = client.issue(issue_key)
        result = format_issue(issue, client)

        # 可选获取评论
        if include_comments:
            try:
                comments = client.comments(issue_key)
                result["comments"] = [format_comment(comment) for comment in comments]
            except Exception as e:
                logger.warning(f"获取评论失败: {str(e)}")
                result["comments"] = []

        return result
    except Exception as e:
        logger.error(f"获取问题 {issue_key} 失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="获取JIRA问题附件")
def get_issue_attachment(
    issue_key: str,
    attachment_id: str,
) -> Dict[str, Any]:
    """获取JIRA问题附件内容.
    
    Args:
        issue_key: JIRA问题键
        attachment_id: 附件ID
    
    Returns:
        Dict[str, Any]: 附件内容
    """
    logger.info(f"获取问题附件: issue={issue_key}, attachment_id={attachment_id}")
    try:
        client = get_jira_client()
        issue = client.issue(issue_key)
        
        # 查找指定ID的附件
        attachment = None
        
        # 检查attachments字段
        attachments = []
        if hasattr(issue.fields, "attachments") and issue.fields.attachments:
            attachments = issue.fields.attachments
        elif hasattr(issue.fields, "attachment") and issue.fields.attachment:
            attachments = issue.fields.attachment
            
        for att in attachments:
            if att.id == attachment_id:
                attachment = att
                break
        
        if not attachment:
            return {"error": f"未找到ID为 {attachment_id} 的附件"}
        
        # 获取附件内容
        content = attachment.get()
        
        # 确定返回类型：对于图片类型，返回Base64编码；对于文本类型，返回文本内容
        mime_type = attachment.mimeType
        filename = attachment.filename
        
        result = {
            "id": attachment.id,
            "filename": filename,
            "size": attachment.size,
            "content_type": mime_type,
            "created": attachment.created,
        }
        
        # 处理不同的内容类型
        if mime_type.startswith("image/"):
            # 对于图片，返回Base64编码
            result["content"] = base64.b64encode(content).decode('utf-8')
            result["encoding"] = "base64"
        elif mime_type.startswith("text/"):
            # 对于文本文件，直接返回文本内容
            try:
                result["content"] = content.decode('utf-8')
                result["encoding"] = "text"
            except UnicodeDecodeError:
                # 如果解码失败，回退到Base64
                result["content"] = base64.b64encode(content).decode('utf-8')
                result["encoding"] = "base64"
        else:
            # 对于其他类型，返回Base64编码
            result["content"] = base64.b64encode(content).decode('utf-8')
            result["encoding"] = "base64"
        
        return result
    except Exception as e:
        logger.error(f"获取问题 {issue_key} 的附件 {attachment_id} 失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="搜索JIRA问题列表", always_load=True)
def search_issues(
    jql: str,
    max_results: int = 50,
    start_at: int = 0
) -> Dict[str, Any]:
    """搜索JIRA问题.
    
    Args:
        jql: JQL查询字符串
        max_results: 最大返回结果数
        start_at: 起始索引
    
    Returns:
        Dict[str, Any]: 搜索结果
    """
    logger.info(f"搜索问题: JQL={jql}, max_results={max_results}, start_at={start_at}")
    try:
        client = get_jira_client()
        issues = client.search_issues(jql_str=jql, maxResults=max_results, startAt=start_at)

        return {
            "total": issues.total,
            "issues": [format_issue(issue, client) for issue in issues],
            "start_at": start_at,
            "max_results": max_results,
        }
    except Exception as e:
        logger.error(f"搜索问题失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="创建JIRA问题")
def create_issue(
    project_key: str,
    summary: str,
    description: str = "",
    issue_type: str = "Task",
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    labels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """创建JIRA问题.
    
    Args:
        project_key: 项目键
        summary: 问题概要
        description: 问题描述
        issue_type: 问题类型
        priority: 优先级
        assignee: 经办人
        labels: 标签列表
    
    Returns:
        Dict[str, Any]: 创建的问题详情
    """
    logger.info(f"创建问题: project={project_key}, summary={summary}")
    
    try:
        # 构建问题字段
        fields = {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
        }
        
        if description:
            fields["description"] = description
            
        if priority:
            fields["priority"] = {"name": priority}
            
        if assignee:
            fields["assignee"] = {"name": assignee}
            
        if labels:
            fields["labels"] = labels
        
        # 创建问题
        client = get_jira_client()
        issue = client.create_issue(fields=fields)
        return format_issue(issue, client)
    except Exception as e:
        logger.error(f"创建问题失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="更新JIRA问题")
def update_issue(
    issue_key: str,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    issue_type: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    labels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """更新JIRA问题.
    
    Args:
        issue_key: 问题键
        summary: 问题概要
        description: 问题描述
        issue_type: 问题类型
        priority: 优先级
        assignee: 经办人
        labels: 标签列表
    
    Returns:
        Dict[str, Any]: 更新后的问题详情
    """
    logger.info(f"更新问题 {issue_key}")
    
    try:
        # 构建更新字段
        fields = {}
        
        if summary:
            fields["summary"] = summary
            
        if description:
            fields["description"] = description
            
        if issue_type:
            fields["issuetype"] = {"name": issue_type}
            
        if priority:
            fields["priority"] = {"name": priority}
            
        if assignee:
            fields["assignee"] = {"name": assignee}
            
        if labels:
            fields["labels"] = labels
        
        if not fields:
            return {"error": "未提供任何更新字段"}
        
        # 更新问题
        client = get_jira_client()
        issue = client.issue(issue_key)
        issue.update(fields=fields)

        # 获取更新后的问题
        updated_issue = client.issue(issue_key)
        return format_issue(updated_issue, client)
    except Exception as e:
        logger.error(f"更新问题 {issue_key} 失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="获取JIRA项目列表")
def get_projects() -> Dict[str, Any]:
    """获取所有项目列表.
    
    Returns:
        Dict[str, Any]: 项目列表
    """
    logger.info("获取项目列表")
    try:
        client = get_jira_client()
        projects = client.projects()
        
        result = [
            {
                "id": project.id,
                "key": project.key,
                "name": project.name,
                "lead": getattr(project, "lead", {}).get("displayName", ""),
            }
            for project in projects
        ]
        
        return {"projects": result}
    except Exception as e:
        logger.error(f"获取项目列表失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="获取JIRA项目详情")
def get_project(
    project_key: str
) -> Dict[str, Any]:
    """获取项目详情.
    
    Args:
        project_key: 项目键
    
    Returns:
        Dict[str, Any]: 项目详情
    """
    logger.info(f"获取项目: {project_key}")
    try:
        client = get_jira_client()
        project = client.project(project_key)
        
        return {
            "id": project.id,
            "key": project.key,
            "name": project.name,
            "lead": getattr(project, "lead", {}).get("displayName", ""),
            "description": getattr(project, "description", ""),
            "url": project.self,
        }
    except Exception as e:
        logger.error(f"获取项目 {project_key} 失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="调试JIRA问题字段")
def debug_issue_fields(
    issue_key: str,
) -> Dict[str, Any]:
    """查看JIRA问题的字段结构，用于调试.
    
    Args:
        issue_key: JIRA问题键
    
    Returns:
        Dict[str, Any]: 字段结构信息
    """
    logger.info(f"调试问题字段: {issue_key}")
    try:
        client = get_jira_client()
        issue = client.issue(issue_key)
        
        fields = []
        for field_name in dir(issue.fields):
            if field_name.startswith('_') or callable(getattr(issue.fields, field_name)):
                continue
                
            value = getattr(issue.fields, field_name)
            field_type = type(value).__name__
            
            if field_name in ('attachment', 'attachments'):
                if value:
                    attachment_info = []
                    for att in value:
                        attachment_info.append({
                            "id": getattr(att, "id", None),
                            "filename": getattr(att, "filename", None),
                            "size": getattr(att, "size", None),
                            "content_type": getattr(att, "mimeType", None),
                            "created": getattr(att, "created", None),
                        })
                    fields.append({"name": field_name, "type": field_type, "value": attachment_info})
                else:
                    fields.append({"name": field_name, "type": field_type, "value": None})
            else:
                # 对于其他字段，仅显示类型信息和简单值
                simple_value = str(value)[:100] if value is not None else None
                fields.append({"name": field_name, "type": field_type, "preview": simple_value})
        
        return {
            "id": issue.id,
            "key": issue.key,
            "fields": sorted(fields, key=lambda x: x["name"])
        }
    except Exception as e:
        logger.error(f"调试问题 {issue_key} 字段失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="根据问题ID和文件名获取JIRA附件")
async def get_attachment_by_filename(
    issue_key: str,
    filename: str,
    save_to_disk: bool = True,
) -> Dict[str, Any]:
    """根据问题ID和文件名获取JIRA附件.
    
    Args:
        issue_key: JIRA问题键
        filename: 附件文件名
        save_to_disk: 是否保存到本地磁盘
    
    Returns:
        Dict[str, Any]: 附件内容
    """
    logger.info(f"根据文件名获取附件: issue={issue_key}, filename={filename}")
    try:
        # 使用JIRA REST API直接获取问题附件
        client = get_jira_client()
        
        # 获取问题详情
        issue_url = f"{jira_settings.server_url}/rest/api/2/issue/{issue_key}"
        response = client._session.get(issue_url)
        if response.status_code != 200:
            return {"error": f"获取问题失败: {response.text}"}
            
        issue_data = response.json()
        
        # 检查附件
        attachments = issue_data.get("fields", {}).get("attachment", [])
        if not attachments:
            return {"error": f"问题 {issue_key} 没有附件"}
            
        # 查找指定文件名的附件
        attachment = None
        for att in attachments:
            if att.get("filename") == filename:
                attachment = att
                break
                
        if not attachment:
            return {"error": f"未找到名为 {filename} 的附件"}
            
        # 获取附件内容
        attachment_url = attachment.get("content")
        if not attachment_url:
            return {"error": "附件URL不存在"}
            
        # 下载附件
        response = client._session.get(attachment_url)
        if response.status_code != 200:
            return {"error": f"下载附件失败: {response.text}"}

        content = response.content
        mime_type = attachment.get("mimeType", "application/octet-stream")

        # 验证下载的内容是否有效（不是HTML登录页面）
        if not is_valid_content(content, mime_type):
            logger.warning(
                f"检测到无效内容（可能是HTML登录页面），使用 Playwright 重新下载: {filename}"
            )
            # 使用 Playwright 重新下载
            file_path = get_attachment_path(issue_key, filename)
            success = await download_attachment_with_playwright(
                attachment_url, file_path
            )

            if not success:
                return {"error": "使用 Playwright 下载失败，请检查 JIRA 登录凭证"}

            # 读取 Playwright 下载的文件
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                logger.info(f"Playwright 下载成功: {filename}")
            except Exception as e:
                return {"error": f"读取 Playwright 下载的文件失败: {e}"}

        result = {
            "id": attachment.get("id"),
            "filename": filename,
            "size": len(content),
            "content_type": mime_type,
            "created": attachment.get("created"),
        }

        # 如果要保存到磁盘且还没保存
        if save_to_disk:
            file_path = get_attachment_path(issue_key, filename)
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(content)
            result["local_path"] = file_path
        
        # 处理不同的内容类型
        if mime_type.startswith("image/"):
            # 对于图片，返回Base64编码
            result["content"] = base64.b64encode(content).decode('utf-8')
            result["encoding"] = "base64"
        elif mime_type.startswith("text/"):
            # 对于文本文件，直接返回文本内容
            try:
                result["content"] = content.decode('utf-8')
                result["encoding"] = "text"
            except UnicodeDecodeError:
                # 如果解码失败，回退到Base64
                result["content"] = base64.b64encode(content).decode('utf-8')
                result["encoding"] = "base64"
        else:
            # 对于其他类型，返回Base64编码
            result["content"] = base64.b64encode(content).decode('utf-8')
            result["encoding"] = "base64"
        
        return result
    except Exception as e:
        logger.error(f"获取问题 {issue_key} 的附件 {filename} 失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="下载JIRA问题的所有附件到本地", always_load=True)
async def download_all_attachments(
    issue_key: str,
) -> Dict[str, Any]:
    """下载JIRA问题的所有附件到本地.
    
    Args:
        issue_key: JIRA问题键
    
    Returns:
        Dict[str, Any]: 下载结果
    """
    logger.info(f"下载问题所有附件: {issue_key}")
    try:
        client = get_jira_client()
        issue = client.issue(issue_key)
        
        downloads = []
        failed = []
        
        # 获取附件列表
        attachments = []
        if hasattr(issue.fields, "attachment") and issue.fields.attachment:
            attachments = issue.fields.attachment
        
        if not attachments:
            return {
                "issue_key": issue_key,
                "message": "此问题没有附件",
                "total": 0,
                "downloads": []
            }
        
        # 为此问题创建目录
        issue_dir = os.path.join(ATTACHMENTS_DIR, issue_key)
        os.makedirs(issue_dir, exist_ok=True)
        
        # 下载每个附件
        for attachment in attachments:
            try:
                file_path = os.path.join(issue_dir, attachment.filename)

                # 使用 session 下载内容，以便可以验证
                attachment_url = str(attachment.content)
                response = client._session.get(attachment_url)

                if response.status_code != 200:
                    raise Exception(f"下载失败，状态码: {response.status_code}")

                content = response.content
                mime_type = attachment.mimeType

                # 验证下载的内容是否有效（不是HTML登录页面）
                if not is_valid_content(content, mime_type):
                    logger.warning(
                        f"检测到无效内容（可能是HTML登录页面），使用 Playwright 重新下载: {attachment.filename}"
                    )
                    # 使用 Playwright 重新下载
                    success = await download_attachment_with_playwright(
                        attachment_url, file_path
                    )

                    if not success:
                        raise Exception("Playwright 下载失败，请检查 JIRA 登录凭证")

                    # 读取 Playwright 下载的文件
                    with open(file_path, "rb") as f:
                        content = f.read()
                    logger.info(f"Playwright 下载成功: {attachment.filename}")

                # 保存到文件（如果还没保存）
                if not os.path.exists(file_path):
                    with open(file_path, "wb") as f:
                        f.write(content)

                downloads.append({
                    "id": attachment.id,
                    "filename": attachment.filename,
                    "size": os.path.getsize(file_path),
                    "content_type": mime_type,
                    "local_path": file_path
                })
            except Exception as e:
                logger.error(f"下载附件 {attachment.filename} 失败: {str(e)}")
                failed.append({
                    "filename": attachment.filename,
                    "error": str(e)
                })
        
        return {
            "issue_key": issue_key,
            "total": len(attachments),
            "success": len(downloads),
            "failed": len(failed),
            "download_dir": issue_dir,
            "downloads": downloads,
            "failures": failed if failed else None
        }
    except Exception as e:
        logger.error(f"下载问题 {issue_key} 的所有附件失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="获取JIRA问题的所有评论")
def get_issue_comments(
    issue_key: str,
) -> Dict[str, Any]:
    """获取JIRA问题的所有评论.

    Args:
        issue_key: JIRA问题键

    Returns:
        Dict[str, Any]: 评论列表和统计信息
    """
    logger.info(f"获取问题评论: {issue_key}")
    try:
        client = get_jira_client()
        # 使用JIRA客户端的comments方法获取所有评论
        comments = client.comments(issue_key)

        # 格式化所有评论
        formatted_comments = [format_comment(comment) for comment in comments]

        return {
            "issue_key": issue_key,
            "total": len(formatted_comments),
            "comments": formatted_comments,
        }
    except Exception as e:
        logger.error(f"获取问题 {issue_key} 评论失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="为JIRA问题添加评论")
def add_comment(
    issue_key: str,
    body: str,
    visibility_type: Optional[str] = None,
    visibility_value: Optional[str] = None,
) -> Dict[str, Any]:
    """为JIRA问题添加评论.

    Args:
        issue_key: JIRA问题键
        body: 评论内容
        visibility_type: 可见性类型，可选值：'role'（角色）或 'group'（组）
        visibility_value: 可见性值，角色名或组名

    Returns:
        Dict[str, Any]: 添加的评论详情
    """
    logger.info(f"添加评论到问题 {issue_key}")
    try:
        client = get_jira_client()

        # 构建可见性参数
        visibility = None
        if visibility_type and visibility_value:
            visibility = {"type": visibility_type, "value": visibility_value}

        # 添加评论
        comment = client.add_comment(issue_key, body, visibility=visibility)

        # 格式化并返回添加的评论
        return {
            "issue_key": issue_key,
            "success": True,
            "comment": format_comment(comment),
        }
    except Exception as e:
        logger.error(f"为问题 {issue_key} 添加评论失败: {str(e)}")
        return {"error": str(e)}


@conditional_tool(description="获取JIRA问题的所有附件")
async def get_issue_attachments(
    issue_key: str,
    download: bool = False
) -> Dict[str, Any]:
    """获取JIRA问题的所有附件信息.
    
    Args:
        issue_key: JIRA问题键
        download: 是否下载附件到本地
    
    Returns:
        Dict[str, Any]: 附件列表
    """
    logger.info(f"获取问题附件列表: {issue_key}, download={download}")

    if download:
        return await download_all_attachments(issue_key)
    
    try:
        client = get_jira_client()
        issue = client.issue(issue_key)
        
        attachments = []
        if hasattr(issue.fields, "attachment") and issue.fields.attachment:
            for attachment in issue.fields.attachment:
                # 检查附件是否已存在于本地
                local_path = get_attachment_path(issue_key, attachment.filename)
                exists_locally = os.path.exists(local_path)
                
                attachments.append({
                    "id": attachment.id,
                    "filename": attachment.filename,
                    "size": attachment.size,
                    "content_type": attachment.mimeType,
                    "created": str(attachment.created),  # 确保日期是字符串
                    "url": str(attachment.content),  # 确保URL是字符串
                    "local_path": local_path if exists_locally else None,
                    "exists_locally": exists_locally
                })
        
        return {
            "issue_key": issue_key,
            "attachments": attachments,
            "total": len(attachments),
            "attachments_dir": os.path.join(ATTACHMENTS_DIR, issue_key)
        }
    except Exception as e:
        logger.error(f"获取问题 {issue_key} 附件列表失败: {str(e)}")
        return {"error": str(e)}


def format_merge_request(mr_data: Dict) -> Dict[str, Any]:
    """格式化 MR 数据，过滤不必要的字段.

    Args:
        mr_data: 原始 MR 数据字典

    Returns:
        Dict[str, Any]: 格式化后的 MR 数据
    """
    return {
        "mr_iid": mr_data.get("mr_iid"),
        "project_name": mr_data.get("project_name"),
        "project_with_namespace": mr_data.get("project_with_namespace"),
        "title": mr_data.get("title"),
        "source_branch": mr_data.get("source_branch"),
        "target_branch": mr_data.get("target_branch"),
        "state": mr_data.get("state"),
        "web_url": mr_data.get("web_url"),
        "author": mr_data.get("author"),
        "created_time": mr_data.get("created_time"),
        "merged_time": mr_data.get("merged_time"),
        "merged_by": mr_data.get("merged_by"),
        "closed_time": mr_data.get("closed_time"),
        "commit_count": mr_data.get("commit_count"),
        "additions": mr_data.get("additions"),
        "deletions": mr_data.get("deletions"),
    }


@conditional_tool(
    description="根据 JIRA ID 从 DevLake 获取相关的 GitLab Merge Request 信息",
    always_load=True
)
def get_merge_requests_by_jira_id(
    jira_id: str,
    limit: int = 50
) -> Dict[str, Any]:
    """根据 JIRA ID 获取 Merge Request 信息.

    Args:
        jira_id: JIRA ID（如 CYTRD-22680 或 22680）
        limit: 限制返回数量（1-200，默认50）

    Returns:
        Dict[str, Any]: 包含 MR 列表的字典
    """
    logger.info(f"查询 JIRA ID: {jira_id}, limit: {limit}")

    # 参数验证
    if not jira_id or not jira_id.strip():
        return {"error": "jira_id cannot be empty"}

    if limit < 1 or limit > 200:
        return {"error": "limit must be between 1 and 200"}

    try:
        # 调用 DevLake API
        response = requests.get(
            f"{devlake_settings.url}/api/merge-requests/search",
            params={"jira_id": jira_id, "limit": limit},
            timeout=30
        )

        # 检查 HTTP 状态
        if response.status_code != 200:
            logger.error(f"DevLake API error: {response.status_code}")
            return {"error": f"DevLake API error: {response.status_code}"}

        # 解析响应
        data = response.json()

        if not data.get("success"):
            return {"error": data.get("error", "Unknown error")}

        # 格式化返回数据
        merge_requests = [
            format_merge_request(mr)
            for mr in data.get("data", [])
        ]

        return {
            "success": True,
            "total": data.get("total", 0),
            "query": data.get("query", jira_id),
            "merge_requests": merge_requests
        }

    except requests.exceptions.Timeout:
        logger.error("DevLake service timeout")
        return {"error": "DevLake service timeout"}
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to DevLake at {devlake_settings.url}")
        return {"error": f"Cannot connect to DevLake service at {devlake_settings.url}"}
    except Exception as e:
        logger.error(f"获取 MR 失败: {str(e)}")
        return {"error": str(e)}


def run_server(transport: str = "stdio"):
    """运行MCP服务器.

    Args:
        transport: 传输模式，可选 "stdio" 或 "sse"
    """
    try:
        # 检查工具加载模式
        load_all_tools = os.getenv("JIRA_LOAD_ALL_TOOLS", "false").lower() == "true"
        if load_all_tools:
            logger.info("加载所有工具（13个）")
        else:
            logger.info("加载核心工具（4个：get_issue, search_issues, download_all_attachments, get_merge_requests_by_jira_id）")

        # 检查环境变量
        if not jira_settings.server_url:
            logger.warning("未设置JIRA_SERVER_URL环境变量")

        if not jira_settings.username:
            logger.warning("未设置JIRA_USERNAME环境变量")

        if not jira_settings.password and not jira_settings.api_token:
            logger.warning("未设置JIRA_PASSWORD或JIRA_API_TOKEN环境变量")

        # 运行MCP服务器
        logger.info(f"Starting JIRA MCP Server with {transport} transport")
        mcp.run(transport=transport)
    except Exception as e:
        logger.error(f"Error starting JIRA MCP Server: {str(e)}")
        raise


def main():
    """主函数（向后兼容）."""
    import argparse
    parser = argparse.ArgumentParser(description="Run the JIRA MCP Server")
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--transport", "-t", choices=["sse", "stdio"], default="stdio")
    parser.add_argument("--full", action="store_true", help="加载所有工具（默认仅加载核心工具）")

    args = parser.parse_args()

    # 设置工具加载模式
    if args.full:
        os.environ["JIRA_LOAD_ALL_TOOLS"] = "true"

    run_server(args.transport)


if __name__ == "__main__":
    main() 