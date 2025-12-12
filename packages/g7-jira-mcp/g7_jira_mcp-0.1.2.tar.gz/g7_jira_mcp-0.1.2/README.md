# G7 JIRA MCP

一个基于FastMCP框架的JIRA集成插件，用于查询JIRA问题详情、列表及进行基本操作，支持JIRA附件管理。

## 主要功能

- 查询JIRA问题详情和问题列表
- 创建和更新JIRA问题
- 获取项目列表和详情
- 管理和下载JIRA问题附件
  - 自动将附件保存到项目根目录的 `.jira-mcp/{issue_key}/` 子目录
  - 按问题ID组织的子目录结构
  - 支持下载单个或所有附件
  - 智能下载机制：自动检测无效内容并使用 Playwright 重新下载
- **评论管理功能**
  - 获取问题的所有评论
  - 添加新评论到问题
- **根据JIRA ID查询GitLab Merge Request**
  - 从DevLake服务获取与JIRA关联的MR信息
  - 支持完整ID或部分ID搜索
  - 返回MR详情、代码变更统计等信息
- **调试工具**
  - debug_issue_fields：查看JIRA问题的完整字段结构

## 配置

### 方式一：直接使用（推荐）

使用 `uvx` 方式，无需手动安装，自动下载和管理包：

```bash
claude mcp add jira-mcp -- uvx g7-jira-mcp --transport stdio \
  --env JIRA_USERNAME=your_username \
  --env JIRA_PASSWORD=your_password
```

### 方式二：先安装后使用

适合需要离线使用或希望固定版本的用户：

```bash
# 1. 安装包（推荐使用阿里云镜像加速）
pip install g7-jira-mcp -i https://mirrors.aliyun.com/pypi/simple

# 2. 添加到 Claude Code
claude mcp add jira-mcp -- g7-jira-mcp --transport stdio \
  --env JIRA_USERNAME=your_username \
  --env JIRA_PASSWORD=your_password
```

### 查看和管理

```bash
# 查看已添加的 MCP 服务器
claude mcp list

# 删除 MCP 服务器
claude mcp remove jira-mcp
```

### Cursor / 其他 IDE 配置

如果使用 Cursor 或其他支持 MCP 的 IDE，在配置文件（如 `.cursor/mcp.json`）中添加：

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

> **提示**: `JIRA_SERVER_URL` 已有默认值，无需配置。如需修改，添加到 `env` 中即可。

## 快速开始

配置完成后，即可在 Claude Code 或支持 MCP 的 IDE 中使用自然语言操作 JIRA：

**查询问题详情**
```
查看 JIRA 问题 ERP-161 的详情
```

**搜索问题**
```
搜索所有处于"进行中"状态的 JIRA 问题
```

**管理附件**
```
下载 JIRA 问题 ERP-161 的所有附件
```

**管理评论**
```
为 ERP-161 添加评论"已修复此问题"
```

**查询关联 MR**
```
查询 ERP-161 关联的 GitLab Merge Request
```

## MCP提供的工具

本MCP服务器提供以下工具：

| 工具名称 | 描述 | 示例 |
|---------|------|------|
| get_issue | 获取JIRA问题详情 | `ERP-123` |
| search_issues | 搜索JIRA问题列表 | `project = ERP AND status = "In Progress"` |
| create_issue | 创建JIRA问题 | 创建一个标题为"修复登录问题"的任务 |
| update_issue | 更新JIRA问题 | 将ERP-123的状态改为"已完成" |
| get_projects | 获取JIRA项目列表 | 列出所有可访问的项目 |
| get_project | 获取项目详情 | 获取ERP项目的详细信息 |
| get_issue_attachments | 获取问题的所有附件 | 列出ERP-123的所有附件 |
| download_all_attachments | 下载问题的所有附件 | 下载ERP-123的全部附件 |
| get_attachment_by_filename | 获取特定附件 | 从ERP-123获取名为"截图.png"的附件 |
| get_issue_comments | 获取问题的所有评论 | 列出ERP-123的所有评论 |
| add_comment | 添加评论到问题 | 为ERP-123添加评论"已修复" |
| get_merge_requests_by_jira_id | 根据JIRA ID查询GitLab MR | 查询ERP-123关联的所有MR |
| debug_issue_fields | 查看问题的完整字段结构 | 调试ERP-123的所有字段 |

## 许可证

MIT 