#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志配置模块（简化版）

提供符合 Python logging 最佳实践的配置函数。

使用方法：
    # 在应用/hook 启动时调用一次
    from devlake_mcp.logging_config import configure_logging, get_log_dir
    configure_logging(log_dir=get_log_dir('.claude/logs'), log_file='hook.log')

    # 之后各个模块直接用标准方式
    import logging
    logger = logging.getLogger(__name__)
    logger.info('message')
"""

import os
import logging
from pathlib import Path
from typing import Optional

from .constants import VALID_LOG_LEVELS, DEFAULT_LOG_LEVEL


def get_log_dir(default_dir: str) -> str:
    """
    获取日志目录路径

    根据配置文件的位置和内容,自动选择项目目录或全局目录。

    Args:
        default_dir: 默认日志目录（相对于项目根目录）,如 '.claude/logs' 或 '.cursor/logs'

    Returns:
        str: 日志目录路径

    优先级逻辑：
        1. 优先检查项目配置（./.claude/settings.json 或 ./.cursor/hooks.json）
           - Claude Code: 检查 settings.json 中是否有 "hooks" 配置
           - Cursor: 检查 hooks.json 是否存在且有效
        2. 如果项目配置存在且有效,使用项目日志目录
        3. 否则检查全局配置（~/.claude/settings.json 或 ~/.cursor/hooks.json）
        4. 如果全局配置存在且有效,使用全局日志目录
        5. 最后使用项目日志目录作为默认值
    """
    import json

    home = Path.home()
    cwd = Path.cwd()

    # 根据 default_dir 判断是 Claude Code 还是 Cursor
    if '.claude' in default_dir:
        project_config = cwd / ".claude" / "settings.json"
        global_config = home / ".claude" / "settings.json"
        project_log_dir = str(cwd / ".claude" / "logs")
        global_log_dir = str(home / ".claude" / "logs")

        # 1. 优先检查项目配置
        if project_config.exists():
            try:
                with open(project_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 检查是否有 hooks 配置
                    if 'hooks' in config and config['hooks']:
                        return project_log_dir
            except Exception:
                pass

        # 2. 检查全局配置
        if global_config.exists():
            try:
                with open(global_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 检查是否有 hooks 配置
                    if 'hooks' in config and config['hooks']:
                        return global_log_dir
            except Exception:
                pass

    elif '.cursor' in default_dir:
        project_config = cwd / ".cursor" / "hooks.json"
        global_config = home / ".cursor" / "hooks.json"
        project_log_dir = str(cwd / ".cursor" / "logs")
        global_log_dir = str(home / ".cursor" / "logs")

        # 1. 优先检查项目配置
        if project_config.exists():
            try:
                with open(project_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 检查是否有有效的 hooks 配置
                    if config.get('version') and 'hooks' in config and config['hooks']:
                        return project_log_dir
            except Exception:
                pass

        # 2. 检查全局配置
        if global_config.exists():
            try:
                with open(global_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 检查是否有有效的 hooks 配置
                    if config.get('version') and 'hooks' in config and config['hooks']:
                        return global_log_dir
            except Exception:
                pass

    # 3. 默认使用项目日志目录
    return default_dir


def configure_logging(
    log_dir: Optional[str] = None,
    log_file: Optional[str] = None
):
    """
    配置全局 logging（在应用启动时调用一次）

    根据环境变量配置日志行为：
    - DEVLAKE_MCP_LOGGING_ENABLED: 是否启用（默认 true）
    - DEVLAKE_MCP_LOG_LEVEL: 日志级别（默认 INFO）
    - DEVLAKE_MCP_CONSOLE_LOG: 是否输出到控制台（默认 false，仅在开发调试时启用）

    Args:
        log_dir: 日志文件目录（可选）
        log_file: 日志文件名（可选）

    示例：
        >>> from devlake_mcp.logging_config import configure_logging
        >>> configure_logging(log_dir='.claude/logs', log_file='hook.log')
        >>>
        >>> import logging
        >>> logger = logging.getLogger(__name__)
        >>> logger.info('Hello')

    注意：
        - 默认情况下，日志只写入文件，不输出到控制台
        - 控制台输出会在 IDE hook 界面显示为 Error Output（stderr）
        - 如需调试，可设置环境变量 DEVLAKE_MCP_CONSOLE_LOG=true 启用控制台输出
    """
    # 读取环境变量
    enabled = os.getenv('DEVLAKE_MCP_LOGGING_ENABLED', 'true').lower() in ('true', '1', 'yes')
    level_str = os.getenv('DEVLAKE_MCP_LOG_LEVEL', DEFAULT_LOG_LEVEL).upper()

    # 获取日志级别
    level = VALID_LOG_LEVELS.get(level_str, VALID_LOG_LEVELS[DEFAULT_LOG_LEVEL])

    # 如果禁用，使用 NullHandler
    if not enabled:
        logging.basicConfig(
            level=level,
            handlers=[logging.NullHandler()]
        )
        return

    # 准备 handlers
    handlers = []
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 文件 handler（如果提供了 log_dir 和 log_file）
    if log_dir and log_file:
        try:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(
                Path(log_dir) / log_file,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            handlers.append(file_handler)
        except Exception as e:
            # 创建文件 handler 失败，只用控制台
            print(f"警告：无法创建日志文件 {log_dir}/{log_file}: {e}")

    # 控制台 handler（仅在开发调试时启用）
    # 通过环境变量 DEVLAKE_MCP_CONSOLE_LOG=true 启用
    if os.getenv('DEVLAKE_MCP_CONSOLE_LOG', 'false').lower() in ('true', '1', 'yes'):
        import sys
        console_handler = logging.StreamHandler(sys.stdout)  # 使用 stdout 而不是 stderr
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        handlers.append(console_handler)

    # 如果没有任何 handler，添加 NullHandler（避免 logging 警告）
    if not handlers:
        handlers.append(logging.NullHandler())

    # 配置全局 logging
    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True  # 覆盖已有配置
    )

    # 抑制第三方库的 DEBUG 日志
    for lib in ['urllib3', 'urllib3.connectionpool', 'requests']:
        logging.getLogger(lib).setLevel(logging.WARNING)
