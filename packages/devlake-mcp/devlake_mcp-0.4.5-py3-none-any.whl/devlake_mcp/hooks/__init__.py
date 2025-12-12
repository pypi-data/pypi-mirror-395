#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevLake MCP - Claude Code Hooks 模块

提供完整的 Claude Code hooks 功能，用于收集 AI 编码数据并上报到 DevLake。

使用方法：
    from devlake_mcp.hooks import session_start
    session_start.main()

所有可用的 hooks:
    - session_start: 会话启动时触发
    - pre_tool_use: 工具执行前触发
    - post_tool_use: 工具执行后触发
    - stop: Claude 完成回复时触发
    - record_session: 会话结束时触发
"""

# 配置将在实际使用时加载，而不是在导入时
# 这样可以避免在测试环境中导致问题
from devlake_mcp.config import DevLakeConfig

def _initialize_hooks_config():
    """初始化 Hooks 配置（按需调用）"""
    return DevLakeConfig.from_env(include_git=True)

# 导入所有 hook 模块
from devlake_mcp.hooks import (
    hook_utils,
    session_start,
    pre_tool_use,
    post_tool_use,
    stop,
    record_session,
)

__all__ = [
    # 工具模块
    "hook_utils",
    # Hook 模块
    "session_start",
    "pre_tool_use",
    "post_tool_use",
    "stop",
    "record_session",
]

__version__ = "0.1.0"
