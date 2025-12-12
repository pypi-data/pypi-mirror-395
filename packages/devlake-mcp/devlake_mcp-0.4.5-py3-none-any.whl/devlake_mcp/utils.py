#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP 工具函数模块

提供跨工具的通用功能：
- 临时目录和文件管理
- 内容压缩（gzip + base64）
- 文件过滤（排除敏感文件和二进制文件）

改进：
- 完整的类型注解
- 使用常量配置
- 更好的文档说明
- 完善的日志记录
"""

import os
import gzip
import base64
import hashlib
import tempfile
import logging
from pathlib import Path
from typing import Optional

from .constants import (
    SENSITIVE_FILE_PATTERNS,
    BINARY_FILE_EXTENSIONS,
    TEMP_DIR_NAME,
)

# 配置日志
logger = logging.getLogger(__name__)

# 持久化数据目录名称
DATA_DIR_NAME = '.devlake'


def get_data_dir(persistent: bool = False) -> Path:
    """
    获取跨平台的数据存储目录

    优先级：
    1. 环境变量 DEVLAKE_MCP_DATA_DIR (优先级最高,覆盖 persistent 参数)
    2. persistent=True: 用户主目录 ~/.devlake (持久化存储)
    3. persistent=False: 系统临时目录/devlake_mcp (临时存储)

    Args:
        persistent: True 使用持久化目录 (~/.devlake),
                   False 使用临时目录 (系统temp/devlake_mcp)

    Returns:
        数据存储目录路径

        持久化目录 (persistent=True):
        - Windows: C:\\Users\\xxx\\.devlake
        - macOS:   /Users/xxx/.devlake
        - Linux:   /home/xxx/.devlake

        临时目录 (persistent=False):
        - Windows: C:\\Users\\xxx\\AppData\\Local\\Temp\\devlake_mcp
        - macOS:   /var/folders/xxx/T/devlake_mcp
        - Linux:   /tmp/devlake_mcp

    Examples:
        >>> # 持久化存储(session state, generation state, retry queue)
        >>> data_dir = get_data_dir(persistent=True)
        >>> # 临时存储(before_content 快照文件)
        >>> temp_dir = get_data_dir(persistent=False)
        >>> # 自定义路径
        >>> os.environ['DEVLAKE_MCP_DATA_DIR'] = '/custom/path'
        >>> data_dir = get_data_dir()  # 返回 /custom/path
    """
    # 优先使用环境变量
    custom_dir = os.getenv('DEVLAKE_MCP_DATA_DIR')
    if custom_dir:
        data_dir = Path(custom_dir)
    elif persistent:
        # 持久化目录: ~/.devlake
        data_dir = Path.home() / DATA_DIR_NAME
    else:
        # 临时目录: /tmp/devlake_mcp (跨平台兼容)
        data_dir = Path(tempfile.gettempdir()) / TEMP_DIR_NAME

    # 确保目录存在
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_temp_file_path(session_id: str, file_path: str) -> str:
    """
    生成临时文件路径（用于存储 before_content）

    Args:
        session_id: 会话ID
        file_path: 文件路径

    Returns:
        临时文件路径（格式：{temp_dir}/{session_id}_{file_hash}.before）
    """
    # 使用文件路径的 hash 作为文件名（避免路径过长）
    file_hash = hashlib.md5(file_path.encode()).hexdigest()[:16]

    # 获取跨平台临时目录（使用临时存储模式）
    temp_dir = get_data_dir(persistent=False)

    # 临时文件名：{session_id}_{file_hash}.before
    temp_file = temp_dir / f"{session_id}_{file_hash}.before"

    return str(temp_file)


def compress_content(content: str) -> str:
    """
    压缩内容（gzip + base64）

    Args:
        content: 原始内容

    Returns:
        base64 编码的 gzip 压缩内容

    注意：
        如果压缩失败，会记录错误日志并返回空字符串
    """
    try:
        if not content:
            return ''

        # 压缩内容
        compressed = gzip.compress(content.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('ascii')

        # 记录压缩效果（仅在调试模式下）
        original_size = len(content.encode('utf-8'))
        compressed_size = len(encoded)
        compression_ratio = compressed_size / original_size if original_size > 0 else 0

        logger.debug(
            f"内容压缩完成: {original_size}B -> {compressed_size}B "
            f"(压缩率: {compression_ratio:.1%})"
        )

        return encoded

    except Exception as e:
        logger.error(f"压缩内容失败: {e}", exc_info=True)
        return ''


def should_collect_file(file_path: str) -> bool:
    """
    判断是否应该采集该文件

    排除规则：
    1. 敏感文件：.env, .secret, .key 等
    2. 二进制文件：图片、压缩包、可执行文件等

    Args:
        file_path: 文件路径

    Returns:
        True 表示应该采集，False 表示跳过
    """
    # 排除敏感文件（使用常量配置）
    file_path_lower = file_path.lower()

    for pattern in SENSITIVE_FILE_PATTERNS:
        if pattern in file_path_lower:
            return False

    # 排除二进制文件（通过后缀判断，使用常量配置）
    file_ext = Path(file_path).suffix.lower()
    if file_ext in BINARY_FILE_EXTENSIONS:
        return False

    return True


def get_file_type(file_path: str) -> str:
    """
    获取文件类型（扩展名）

    Args:
        file_path: 文件路径

    Returns:
        文件扩展名（不含点），如果没有扩展名返回 'unknown'
    """
    return Path(file_path).suffix.lstrip('.') or 'unknown'


def read_file_content(file_path: str) -> str:
    """
    读取文件内容

    Args:
        file_path: 文件路径

    Returns:
        文件内容，读取失败返回空字符串

    注意：
        如果文件不存在或读取失败，会记录警告日志并返回空字符串
    """
    try:
        if not os.path.exists(file_path):
            logger.debug(f"文件不存在: {file_path}")
            return ''

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.debug(f"成功读取文件: {file_path} ({len(content)} 字符)")
            return content

    except UnicodeDecodeError as e:
        logger.warning(f"文件编码错误 (可能是二进制文件): {file_path} - {e}")
        return ''
    except PermissionError as e:
        logger.warning(f"无权限读取文件: {file_path} - {e}")
        return ''
    except Exception as e:
        logger.error(f"读取文件失败: {file_path} - {e}", exc_info=True)
        return ''
