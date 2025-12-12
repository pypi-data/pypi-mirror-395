"""
兼容性检测模块

提供 Python 版本检测和功能可用性检查，实现渐进式功能支持：
- Python 3.9：仅支持 Hooks 模式
- Python 3.10+：完整支持（Hooks + MCP Server）
"""

import sys
import warnings
from typing import Optional, Any

# 检测 Python 版本
PYTHON_VERSION = sys.version_info
HAS_MCP_SUPPORT = PYTHON_VERSION >= (3, 10)

# 尝试导入 fastmcp（仅在 Python 3.10+ 时）
MCP_AVAILABLE = False
FastMCP: Optional[Any] = None

if HAS_MCP_SUPPORT:
    try:
        from fastmcp import FastMCP
        MCP_AVAILABLE = True
    except ImportError:
        MCP_AVAILABLE = False
        warnings.warn(
            "fastmcp 未安装。MCP 功能已禁用。\n"
            "安装方式: pip install 'devlake-mcp[mcp]'",
            ImportWarning,
            stacklevel=2
        )


def get_version_info() -> dict:
    """
    获取版本和功能支持信息

    Returns:
        dict: {
            "python_version": "3.10.19",
            "python_version_tuple": (3, 10, 19),
            "mcp_supported": True,  # Python 版本是否支持 MCP
            "mcp_available": True,  # fastmcp 是否已安装
            "fastmcp_version": "2.13.0.2",  # fastmcp 版本（如果已安装）
            "features": {
                "hooks": True,  # Hooks 模式（所有版本都支持）
                "mcp_server": True  # MCP Server 模式
            },
            "recommended_action": "..."  # 推荐操作
        }
    """
    python_version_str = f"{PYTHON_VERSION.major}.{PYTHON_VERSION.minor}.{PYTHON_VERSION.micro}"

    # 获取 fastmcp 版本（如果可用）
    fastmcp_version = None
    if MCP_AVAILABLE:
        try:
            import fastmcp
            fastmcp_version = getattr(fastmcp, '__version__', 'unknown')
        except Exception:
            pass

    # 判断推荐操作
    if MCP_AVAILABLE:
        recommended_action = "✓ 所有功能可用"
    elif not HAS_MCP_SUPPORT:
        recommended_action = "升级到 Python 3.10+ 以使用 MCP 功能"
    else:
        recommended_action = "安装完整功能: pip install 'devlake-mcp[mcp]'"

    return {
        "python_version": python_version_str,
        "python_version_tuple": (PYTHON_VERSION.major, PYTHON_VERSION.minor, PYTHON_VERSION.micro),
        "mcp_supported": HAS_MCP_SUPPORT,
        "mcp_available": MCP_AVAILABLE,
        "fastmcp_version": fastmcp_version,
        "features": {
            "hooks": True,  # Hooks 模式所有版本都支持
            "mcp_server": MCP_AVAILABLE,  # MCP Server 需要 fastmcp
        },
        "recommended_action": recommended_action
    }


def check_mcp_available() -> bool:
    """
    检查 MCP 功能是否可用

    Returns:
        bool: MCP 功能是否可用（fastmcp 已安装且 Python >= 3.10）
    """
    return MCP_AVAILABLE


def get_compatibility_warnings() -> list[str]:
    """
    获取兼容性警告信息

    Returns:
        list[str]: 警告信息列表
    """
    warnings_list = []

    if not HAS_MCP_SUPPORT:
        warnings_list.append(
            f"⚠ Python {PYTHON_VERSION.major}.{PYTHON_VERSION.minor} detected. "
            f"MCP 功能需要 Python 3.10+"
        )
        warnings_list.append(
            "ℹ Hooks 模式可用于 Python 3.9"
        )

    elif not MCP_AVAILABLE:
        warnings_list.append(
            "⚠ fastmcp 未安装。MCP Server 功能不可用。"
        )
        warnings_list.append(
            "ℹ 安装完整功能: pip install 'devlake-mcp[mcp]'"
        )

    return warnings_list


def print_compatibility_info(verbose: bool = False):
    """
    打印兼容性信息

    Args:
        verbose: 是否显示详细信息
    """
    info = get_version_info()

    print("=" * 60)
    print("DevLake MCP - 版本信息")
    print("=" * 60)
    print(f"Python 版本: {info['python_version']}")

    if info['mcp_available']:
        print(f"✓ MCP Server: 已启用 (FastMCP {info['fastmcp_version']})")
    elif info['mcp_supported']:
        print("✗ MCP Server: 未安装 (需要 fastmcp)")
    else:
        print("✗ MCP Server: 不支持 (需要 Python 3.10+)")

    print(f"✓ Hooks 模式: 可用")
    print()

    # 显示警告
    warnings_list = get_compatibility_warnings()
    if warnings_list:
        print("注意事项:")
        for warning in warnings_list:
            print(f"  {warning}")
        print()

    # 显示推荐操作
    print(f"建议: {info['recommended_action']}")
    print("=" * 60)

    if verbose:
        print("\n功能详情:")
        print(f"  - Hooks 模式: {'✓' if info['features']['hooks'] else '✗'}")
        print(f"  - MCP Server: {'✓' if info['features']['mcp_server'] else '✗'}")
        print()
