#!/usr/bin/env python3
"""测试完整模式（加载所有工具）."""

import os
import sys


def test_full_mode():
    """测试完整模式（使用 --full 参数）."""
    print("=== 测试完整模式（使用 --full 参数）===")

    # 设置环境变量
    os.environ["JIRA_LOAD_ALL_TOOLS"] = "true"

    # 导入 server 模块
    from jira_mcp import server

    # 检查哪些工具被注册了
    tools = server.mcp._tool_manager._tools

    print(f"已注册工具数量: {len(tools)}")
    print(f"已注册工具列表:")
    for name in sorted(tools.keys()):
        print(f"  - {name}")

    # 验证所有工具都已加载
    all_tools = ["get_issue", "search_issues", "download_all_attachments",
                "create_issue", "update_issue", "get_projects", "get_project",
                "debug_issue_fields", "get_attachment_by_filename",
                "get_issue_comments", "add_comment", "get_issue_attachments",
                "get_issue_attachment"]

    missing_tools = []
    for tool in all_tools:
        if tool not in tools:
            missing_tools.append(tool)

    if missing_tools:
        print(f"\n❌ 以下工具未加载: {missing_tools}")
        return False

    print(f"\n✅ 所有工具验证通过（{len(tools)}个）")

    # 验证工具数量（应该是 13 个：3 个核心 + 10 个可选）
    expected_count = len(all_tools)
    if len(tools) != expected_count:
        print(f"⚠️ 预期工具数量: {expected_count}，实际: {len(tools)}")
        # 不算失败，因为可能有额外的工具

    return True


if __name__ == "__main__":
    try:
        if test_full_mode():
            print("\n✅ 完整模式测试通过！")
            sys.exit(0)
        else:
            print("\n❌ 完整模式测试失败！")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
