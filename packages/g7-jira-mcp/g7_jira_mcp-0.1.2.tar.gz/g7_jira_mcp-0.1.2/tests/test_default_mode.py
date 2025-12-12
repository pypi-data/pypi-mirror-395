#!/usr/bin/env python3
"""测试默认模式（只加载核心工具）."""

import os
import sys


def test_default_mode():
    """测试默认模式（只加载核心工具）."""
    print("=== 测试默认模式（不使用 --full 参数）===")

    # 确保环境变量未设置
    if "JIRA_LOAD_ALL_TOOLS" in os.environ:
        del os.environ["JIRA_LOAD_ALL_TOOLS"]

    # 导入 server 模块
    from jira_mcp import server

    # 检查哪些工具被注册了
    # FastMCP 的工具保存在 mcp._tool_manager._tools 中
    tools = server.mcp._tool_manager._tools

    print(f"已注册工具数量: {len(tools)}")
    print(f"已注册工具列表:")
    for name in sorted(tools.keys()):
        print(f"  - {name}")

    # 验证核心工具已加载
    core_tools = ["get_issue", "search_issues", "download_all_attachments"]
    for tool in core_tools:
        assert tool in tools, f"核心工具 {tool} 未加载"

    print(f"\n✅ 核心工具验证通过（3个）")

    # 验证可选工具未加载
    optional_tools = ["create_issue", "update_issue", "get_projects", "get_project",
                     "debug_issue_fields", "get_attachment_by_filename",
                     "get_issue_comments", "add_comment", "get_issue_attachments",
                     "get_issue_attachment"]

    loaded_optional = [t for t in optional_tools if t in tools]
    if loaded_optional:
        print(f"❌ 以下可选工具不应该加载但被加载了: {loaded_optional}")
        return False
    else:
        print(f"✅ 可选工具验证通过（未加载）")

    # 验证工具数量
    if len(tools) != 3:
        print(f"❌ 预期工具数量: 3，实际: {len(tools)}")
        return False

    return True


if __name__ == "__main__":
    try:
        if test_default_mode():
            print("\n✅ 默认模式测试通过！")
            sys.exit(0)
        else:
            print("\n❌ 默认模式测试失败！")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
