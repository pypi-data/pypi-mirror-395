"""
DevLake MCP Server

一个用于 DevLake 的 Model Context Protocol 服务器。
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("devlake-mcp")
except PackageNotFoundError:
    # 开发模式下未安装包时的 fallback
    __version__ = "0.0.0.dev"
