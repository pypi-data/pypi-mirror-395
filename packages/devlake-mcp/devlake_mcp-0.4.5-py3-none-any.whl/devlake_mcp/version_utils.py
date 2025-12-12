#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本检测工具模块

提供以下功能：
1. 获取 devlake-mcp 版本号
2. 检测 Claude Code 版本
3. 检测 Cursor 版本
4. 自动检测平台类型和版本信息
"""

import os
import logging
import subprocess
from typing import Optional, Dict, Union

from .enums import IDEType

logger = logging.getLogger(__name__)


# ============================================================================
# DevLake MCP 版本检测
# ============================================================================

def get_devlake_mcp_version() -> str:
    """
    获取 devlake-mcp 包的版本号

    Returns:
        版本号字符串，如 "0.3.1"，失败返回 "unknown"
    """
    try:
        from devlake_mcp import __version__
        return __version__
    except Exception as e:
        logger.warning(f'获取 devlake-mcp 版本失败: {e}')
        return 'unknown'


# ============================================================================
# Claude Code 版本检测
# ============================================================================

def get_claude_code_version() -> Optional[str]:
    """
    检测 Claude Code 版本号

    尝试以下方法：
    1. 从环境变量 CLAUDE_CODE_VERSION 读取
    2. 执行 claude --version 命令

    Returns:
        版本号字符串，如 "0.1.5"，未检测到返回 None
    """
    # 方法1: 环境变量（最快）
    version = os.getenv('CLAUDE_CODE_VERSION')
    if version:
        logger.debug(f'从环境变量检测到 Claude Code 版本: {version}')
        return version

    # 方法2: 执行 claude --version 命令
    try:
        result = subprocess.run(
            ['claude', '--version'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            # 直接使用命令输出，不做任何解析
            version = result.stdout.strip()
            logger.debug(f'从命令行检测到 Claude Code 版本: {version}')
            return version
    except Exception as e:
        logger.debug(f'执行 claude --version 失败: {e}')

    logger.debug('未能检测到 Claude Code 版本')
    return None


# ============================================================================
# Cursor 版本检测
# ============================================================================

def get_cursor_version() -> Optional[str]:
    """
    检测 Cursor 版本号

    尝试以下方法：
    1. 从环境变量 CURSOR_VERSION 读取
    2. 执行 cursor-agent -v 命令

    Returns:
        版本号字符串，如 "0.40.1"，未检测到返回 None
    """
    # 方法1: 环境变量
    version = os.getenv('CURSOR_VERSION')
    if version:
        logger.debug(f'从环境变量检测到 Cursor 版本: {version}')
        return version

    # 方法2: 执行 cursor-agent -v 命令
    try:
        result = subprocess.run(
            ['cursor-agent', '-v'],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            # 提取版本号
            output = result.stdout.strip()
            # 可能的输出格式：0.40.1 或 cursor-agent version 0.40.1
            parts = output.split()
            version = parts[-1]  # 取最后一个单词作为版本号
            logger.debug(f'从命令行检测到 Cursor 版本: {version}')
            return version
    except Exception as e:
        logger.debug(f'执行 cursor-agent -v 失败: {e}')

    logger.debug('未能检测到 Cursor 版本')
    return None


# ============================================================================
# 统一检测接口
# ============================================================================

def detect_platform_info(ide_type: IDEType) -> Dict[str, Optional[str]]:
    """
    检测平台类型和版本信息

    Args:
        ide_type: IDE 类型枚举
                 应该从调用 hook 的上下文中获取，因为不同 IDE 使用不同的 hook

    Returns:
        包含以下字段的字典：
        - devlake_mcp_version: DevLake MCP 版本（字符串）
        - ide_version: IDE 版本号（可能为 None）
        - data_source: 数据来源（固定为 'hook'）

    注意：
        - 不返回 ide_type，因为调用方已经知道（避免字段重复）
        - 因为 Claude Code 和 Cursor 使用不同的 hook，所以调用时就知道平台类型
        - 不需要通过环境变量、进程名或目录来检测平台
    """
    # 获取字符串值并规范化
    ide_type_str = ide_type.value
    normalized_ide_type = ide_type_str.lower()

    result = {
        'devlake_mcp_version': get_devlake_mcp_version(),
        'ide_version': None,
        'data_source': 'hook'
    }

    # 根据 IDE 类型获取版本
    if normalized_ide_type == IDEType.CLAUDE_CODE.value:
        result['ide_version'] = get_claude_code_version()
    elif normalized_ide_type == IDEType.CURSOR.value:
        result['ide_version'] = get_cursor_version()
    # qoder 和其他平台：暂不支持版本检测

    logger.info(
        f'平台检测完成: '
        f'ide_type={ide_type_str}, '
        f'devlake-mcp={result["devlake_mcp_version"]}, '
        f'ide_version={result["ide_version"] or "unknown"}'
    )

    return result
