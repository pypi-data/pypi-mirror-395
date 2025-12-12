"""
MCP 服务器入口点

当使用 python -m devlake_mcp 或通过 pipx 安装后运行时会调用此文件。
"""

from devlake_mcp.server import main

if __name__ == "__main__":
    main()
