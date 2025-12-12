#!/usr/bin/env python3
"""测试 get_issue 的 include_comments 参数."""

import os


def test_get_issue_signature():
    """测试 get_issue 函数签名."""
    print("=== 测试 get_issue 函数签名 ===")

    # 确保环境变量未设置
    if "JIRA_LOAD_ALL_TOOLS" in os.environ:
        del os.environ["JIRA_LOAD_ALL_TOOLS"]

    # 导入 server 模块
    from jira_mcp import server
    import inspect

    # 获取 get_issue 函数签名
    sig = inspect.signature(server.get_issue)
    params = sig.parameters

    print(f"get_issue 参数列表:")
    for name, param in params.items():
        default = param.default
        if default == inspect.Parameter.empty:
            default_str = "无默认值"
        else:
            default_str = f"默认值: {default}"
        print(f"  - {name}: {default_str}")

    # 验证参数
    assert "issue_key" in params, "缺少 issue_key 参数"
    assert "include_comments" in params, "缺少 include_comments 参数"

    # 验证 include_comments 默认值为 True
    include_comments_param = params["include_comments"]
    assert include_comments_param.default == True, f"include_comments 默认值应该是 True，实际是 {include_comments_param.default}"

    print(f"\n✅ get_issue 函数签名验证通过")
    print(f"  - issue_key 参数存在")
    print(f"  - include_comments 参数存在且默认值为 True")

    return True


if __name__ == "__main__":
    try:
        if test_get_issue_signature():
            print("\n✅ 测试通过！")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
