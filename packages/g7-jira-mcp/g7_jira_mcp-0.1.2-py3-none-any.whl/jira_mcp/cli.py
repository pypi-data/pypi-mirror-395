#!/usr/bin/env python3
"""CLI入口点 - 在导入server模块前处理参数和环境变量."""

import argparse
import os
import sys


def main():
    """CLI主函数."""
    # 解析参数（在导入server之前）
    parser = argparse.ArgumentParser(description="Run the JIRA MCP Server")
    parser.add_argument("--config", "-c", help="Path to config file")
    parser.add_argument("--transport", "-t", choices=["sse", "stdio"], default="stdio")
    parser.add_argument("--full", action="store_true", help="加载所有工具（默认仅加载核心工具）")

    args = parser.parse_args()

    # 在导入server模块前设置环境变量
    if args.full:
        os.environ["JIRA_LOAD_ALL_TOOLS"] = "true"

    # 现在导入server模块（装饰器会读取环境变量）
    from jira_mcp.server import run_server

    # 调用服务器运行函数
    run_server(args.transport)


if __name__ == "__main__":
    main()
