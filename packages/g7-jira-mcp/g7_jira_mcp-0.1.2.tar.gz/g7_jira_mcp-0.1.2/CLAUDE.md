# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 FastMCP 框架的 JIRA MCP (Model Context Protocol) 服务器，为 AI 助手提供标准化的 JIRA 集成接口。项目允许通过 MCP 协议查询、创建、更新 JIRA 问题，以及管理附件。

## 核心架构

### 主要模块

- **src/jira_mcp/server.py** - MCP 服务器主程序
  - 使用 FastMCP 框架创建 MCP 服务器
  - 通过 `@mcp.tool()` 装饰器定义所有工具函数
  - 管理 JIRA 客户端连接和附件存储
  - 附件默认保存在项目根目录的 `.jira-mcp/{issue_key}/` 子目录下

- **src/jira_mcp/config.py** - 配置管理
  - 从环境变量或配置文件加载 JIRA 连接信息
  - 使用 `python-dotenv` 加载 `.env` 文件
  - 必需的环境变量：`JIRA_SERVER_URL`, `JIRA_USERNAME`, `JIRA_PASSWORD` 或 `JIRA_API_TOKEN`

- **src/jira_mcp/attachment_downloader.py** - 智能附件下载模块
  - 使用 Playwright 模拟浏览器登录并下载附件
  - 提供内容验证函数（`is_valid_content`, `is_html_content`, `is_valid_image`）
  - 当 REST API 下载失败时自动降级使用

- **src/jira_mcp/scripts/** - 命令行工具
  - `download_all_attachments.py` - 批量下载附件
  - `extract_attachment.py` - 下载单个附件

### MCP 工具函数

所有工具函数都在 `server.py` 中定义，主要包括：

- **问题管理**: `get_issue`, `search_issues`, `create_issue`, `update_issue`
- **项目管理**: `get_projects`, `get_project`
- **附件管理**: `get_issue_attachments` (async), `download_all_attachments` (async), `get_attachment_by_filename` (async)
- **评论管理**: `get_issue_comments`, `add_comment` - 获取和添加问题评论
- **调试工具**: `debug_issue_fields` - 用于查看 JIRA 问题的完整字段结构

**异步工具**（使用 `async def` 定义，需要在异步上下文中调用）：
- `get_issue_attachments` - 获取并可选下载附件
- `download_all_attachments` - 下载所有附件到本地
- `get_attachment_by_filename` - 根据文件名获取指定附件

### 数据格式化

`format_issue()` 函数负责将 JIRA API 返回的问题对象转换为 JSON 友好的字典格式，包括：
- 基本字段（summary, description, status, project 等）
- 可选字段（assignee, reporter, priority, labels 等）
- 附件信息（从 `fields.attachment` 字段获取）
- 自定义字段（以 `customfield_` 开头）

`format_comment()` 函数负责将 JIRA 评论对象转换为 JSON 友好的字典格式，包括：
- 基本字段（id, body, created, updated）
- 作者信息（author.name, author.displayName, author.emailAddress）
- 更新者信息（updateAuthor）
- 可见性设置（visibility.type, visibility.value）

## 常用开发命令

### 环境设置

```bash
# 安装开发依赖（推荐使用阿里云镜像源加速）
pip install -e ".[dev]" -i https://mirrors.aliyun.com/pypi/simple

# 安装 Playwright 浏览器驱动（用于附件下载降级）
playwright install chromium
```

### 代码格式化

```bash
# 使用 black 格式化代码
black src/

# 使用 isort 排序导入
isort src/
```

### 构建和发布

```bash
# 使用自动化脚本
./scripts/publish.sh

# 手动构建
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

## 开发注意事项

### Python 版本支持

- 项目支持 Python 3.10、3.11 和 3.12
- 所有主要依赖包（jira, mcp, pydantic, playwright 等）均已兼容 Python 3.11+

### JIRA API 字段差异

- JIRA API 中附件字段名为 `attachment`（不是 `attachments`）
- 在处理附件时需要检查 `fields.attachment` 字段
- 使用 `debug_issue_fields` 工具可以查看任何问题的完整字段结构

### 附件处理

- 附件内容根据 MIME 类型返回不同格式：
  - 图片：Base64 编码
  - 文本：UTF-8 文本（解码失败则回退到 Base64）
  - 其他：Base64 编码
- 下载的附件自动保存到项目根目录的 `.jira-mcp/{issue_key}/` 子目录下

#### 智能附件下载（Playwright 降级）

项目实现了智能附件下载机制，自动处理 JIRA 认证问题：

1. **首次尝试**：使用 JIRA REST API session 直接下载
2. **内容验证**：检查下载内容是否有效
   - 检测是否是 HTML 登录页面
   - 对于图片文件，验证文件头格式
3. **自动降级**：如果检测到无效内容，自动使用 Playwright 登录后重新下载

**Playwright 要求**：
- 首次使用需要安装浏览器驱动：`playwright install chromium`
- 需要在环境变量中配置 `JIRA_USERNAME` 和 `JIRA_PASSWORD`
- 自动在 headless 模式下运行，不会弹出浏览器窗口
- **追踪功能**：默认禁用 Playwright 追踪，不会生成 `trace.zip` 文件
  - 如需启用追踪（用于调试），设置环境变量 `JIRA_ENABLE_TRACING=true`

**触发条件**：
- 下载的内容是 HTML 页面（包含 `<!DOCTYPE` 或 `<html>` 标签）
- 图片文件的文件头不匹配（如 PNG 文件不是以 `\x89PNG` 开头）

### MCP 传输模式

- **stdio**: 标准输入/输出，适合作为子进程运行（IDE 集成）
- **sse**: Server-Sent Events，适合 Web 应用
- **streamable-http**: HTTP 模式，需要指定端口

## 配置示例

### Claude Code CLI 配置（推荐）

使用 `claude mcp add` 命令快速配置：

```bash
# 使用默认 JIRA_SERVER_URL (https://issues.chinawayltd.com)
claude mcp add jira-mcp -- g7-jira-mcp --transport stdio \
  --env JIRA_USERNAME=your_username \
  --env JIRA_PASSWORD=your_password

# 或使用 API Token
claude mcp add jira-mcp -- g7-jira-mcp --transport stdio \
  --env JIRA_USERNAME=your_username \
  --env JIRA_API_TOKEN=your_api_token
```

查看已添加的 MCP 服务器：
```bash
claude mcp list
```

### Cursor / 其他 IDE 配置

在配置文件（如 `.cursor/mcp.json`）中添加：

```json
{
  "mcpServers": {
    "g7-jira-mcp": {
      "command": "uvx",
      "args": [
        "--from=g7-jira-mcp",
        "g7-jira-mcp",
        "--transport",
        "stdio"
      ],
      "env": {
        "JIRA_USERNAME": "your_username",
        "JIRA_PASSWORD": "your_password"
      }
    }
  }
}
```

> **提示**: `JIRA_SERVER_URL` 默认为 `https://issues.chinawayltd.com`，无需配置。

### 环境变量配置（开发调试）

创建 `.env` 文件：

```
# JIRA 服务器配置（可选，默认为 https://issues.chinawayltd.com）
JIRA_SERVER_URL=https://issues.chinawayltd.com
JIRA_USERNAME=your_username
JIRA_PASSWORD=your_password
# 或使用 API Token
JIRA_API_TOKEN=your_api_token

# DevLake 服务配置（可选，默认为测试环境）
DEVLAKE_URL=http://devlake.test.chinawayltd.com

# 可选：启用 Playwright 追踪（用于调试附件下载，默认禁用）
# JIRA_ENABLE_TRACING=true
```

## 单元测试

### 测试框架

项目使用 pytest 作为测试框架，配置如下：

- **测试框架**: pytest 7+
- **Mock 框架**: pytest-mock 3.10+ (基于 unittest.mock)
- **覆盖率工具**: pytest-cov 4.0+
- **测试目录**: `tests/`
- **覆盖率要求**: ≥ 50%（当前 `attachment_downloader.py` 已达到 89.47%）

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_attachment_downloader.py
pytest tests/test_comments.py

# 运行测试并显示覆盖率
pytest --cov=src/jira_mcp --cov-report=term-missing

# 生成 HTML 覆盖率报告
pytest --cov=src/jira_mcp --cov-report=html
open htmlcov/index.html
```

### 测试结构

- **tests/test_attachment_downloader.py**: attachment_downloader 模块测试（37 个测试用例）
  - `TestIsHtmlContent`: HTML 内容检测测试（10 个测试）
  - `TestIsValidImage`: 图片格式验证测试（13 个测试）
  - `TestIsValidContent`: 内容综合验证测试（5 个测试）
  - `TestDownloadAttachmentWithPlaywright`: Playwright 下载测试（9 个测试）

- **tests/test_comments.py**: 评论功能测试（27 个测试用例）
  - `TestFormatComment`: 评论格式化测试（9 个测试）
  - `TestGetIssueComments`: 获取评论工具测试（8 个测试）
  - `TestAddComment`: 添加评论工具测试（10 个测试）

### 测试规范

所有测试遵循 G7E6 标准：

- ✅ **AAA 模式**: Arrange（准备）、Act（执行）、Assert（断言）
- ✅ **命名规范**: `test_method_scenario_expected`
- ✅ **Mock 策略**: 只 Mock 外部依赖（Playwright、文件系统）
- ✅ **参数化测试**: 使用 `@pytest.mark.parametrize` 覆盖多种场景
- ✅ **Fixture 使用**: 复用测试数据和 Mock 对象

## 项目仓库

- GitHub: https://github.com/YOUR_USERNAME/g7-jira-mcp
- PyPI: https://pypi.org/project/g7-jira-mcp/
