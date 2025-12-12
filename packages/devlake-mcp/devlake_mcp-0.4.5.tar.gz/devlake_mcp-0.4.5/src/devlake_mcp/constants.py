#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevLake MCP 常量配置

集中管理所有魔法值，提高代码可维护性。
"""

import os
from typing import Set

# ============================================================================
# Git 配置
# ============================================================================

# Git 命令超时时间（秒）
GIT_COMMAND_TIMEOUT: int = 1


# ============================================================================
# 文件过滤配置
# ============================================================================

# 敏感文件模式（包含这些关键词的文件不采集）
SENSITIVE_FILE_PATTERNS: list[str] = [
    '.env',
    '.env.',           # .env.local, .env.production 等
    '.secret',
    '.secrets',
    '.key',
    '.pem',
    '.crt',
    '.p12',
    '.pfx',
    'credentials',
    'password',
    '.npmrc',          # npm 配置
    '.pypirc',         # PyPI 配置
    'id_rsa',          # SSH 私钥
    'id_dsa',
    'id_ecdsa',
    'id_ed25519',
]

# 敏感目录（这些目录下的文件不采集）
SENSITIVE_DIRS: list[str] = [
    '.ssh',
    '.gnupg',
    '.aws',
    '.azure',
    '.config',
    'node_modules',    # 前端依赖
    '.venv',           # Python 虚拟环境
    'venv',
    '__pycache__',
    '.git',            # Git 元数据
]

# 二进制文件扩展名（这些文件不采集）
BINARY_FILE_EXTENSIONS: Set[str] = {
    # 图片
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp',
    # 压缩包
    '.zip', '.tar', '.gz', '.bz2', '.rar', '.7z', '.xz',
    # 文档
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    # 可执行文件
    '.exe', '.dll', '.so', '.dylib', '.app', '.dmg',
    # 编译产物
    '.class', '.pyc', '.pyo', '.o', '.a', '.jar',
    # 音视频
    '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac',
    # 字体
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
}


# ============================================================================
# API 配置
# ============================================================================

# API 请求超时时间（秒）
API_REQUEST_TIMEOUT: int = 7

# API 默认基础 URL
DEFAULT_API_BASE_URL: str = "http://devlake.test.chinawayltd.com"

# 最大内容大小（字节）- 10MB
MAX_CONTENT_SIZE: int = 10 * 1024 * 1024


# ============================================================================
# 临时文件配置
# ============================================================================

# 临时文件最大保留时间（小时）
TEMP_FILE_MAX_AGE_HOURS: int = 24

# 临时目录默认名称
TEMP_DIR_NAME: str = 'devlake_mcp'


# ============================================================================
# Hooks 配置
# ============================================================================

# Hook 执行超时时间（秒）
HOOK_EXECUTION_TIMEOUT: int = 15

# Hook 日志目录（默认为项目目录）
HOOK_LOG_DIR: str = '.claude/logs'  # Claude Code hooks 日志目录（项目）
CURSOR_HOOK_LOG_DIR: str = '.cursor/logs'  # Cursor hooks 日志目录（项目）

# 全局日志目录（当使用全局配置时）
GLOBAL_HOOK_LOG_DIR: str = None  # 运行时动态设置为 ~/.claude/logs
GLOBAL_CURSOR_HOOK_LOG_DIR: str = None  # 运行时动态设置为 ~/.cursor/logs

# 默认 IDE 类型
DEFAULT_IDE_TYPE: str = 'claude_code'

# 默认模型名称
DEFAULT_MODEL_NAME: str = 'claude-sonnet-4-5'


# ============================================================================
# Generation 配置
# ============================================================================

# Generation 状态文件名
GENERATION_STATE_FILE_NAME: str = 'generation_state.json'

# Generation 状态最大保留时间（小时）- 超过此时间的状态可以被清理
GENERATION_STATE_MAX_AGE_HOURS: int = 24


# ============================================================================
# Transcript 压缩配置
# ============================================================================

# Transcript 压缩阈值（字节）- 超过此大小才进行压缩
# 1MB = 1 * 1024 * 1024 bytes * 0.5
TRANSCRIPT_COMPRESSION_THRESHOLD: int = 1 * 1024 * 1024 * 0.5

# Transcript 压缩算法
TRANSCRIPT_COMPRESSION_ALGORITHM: str = 'gzip'


# ============================================================================
# 日志配置
# ============================================================================

# 日志级别映射（字符串 -> logging 常量）
VALID_LOG_LEVELS: dict[str, int] = {
    'DEBUG': 10,     # logging.DEBUG
    'INFO': 20,      # logging.INFO
    'WARNING': 30,   # logging.WARNING
    'ERROR': 40,     # logging.ERROR
    'CRITICAL': 50,  # logging.CRITICAL
}

# 默认日志级别
DEFAULT_LOG_LEVEL: str = 'INFO'


# ============================================================================
# 动态配置函数（支持环境变量覆盖）
# ============================================================================

def get_hook_timeout() -> int:
    """
    获取 Hook 执行超时时间（秒）

    环境变量：DEVLAKE_HOOK_TIMEOUT（默认 15 秒）

    Returns:
        int: Hook 执行超时时间（秒）
    """
    return int(os.getenv('DEVLAKE_HOOK_TIMEOUT', str(HOOK_EXECUTION_TIMEOUT)))


def get_http_retry_count() -> int:
    """
    获取 HTTP 请求重试次数

    环境变量：DEVLAKE_HTTP_RETRY_COUNT（默认 1 次）

    Returns:
        int: HTTP 请求失败后的重试次数
    """
    return int(os.getenv('DEVLAKE_HTTP_RETRY_COUNT', '1'))


# ============================================================================
# Transcript 缓存配置
# ============================================================================

# Transcript 缓存文件路径（默认 ~/.devlake/transcript_cache.json）
TRANSCRIPT_CACHE_DIR_NAME: str = '.devlake'
TRANSCRIPT_CACHE_FILE_NAME: str = 'transcript_cache.json'

# Transcript 缓存保留天数（默认 30 天）
TRANSCRIPT_CACHE_RETENTION_DAYS: int = 30

# 僵尸会话阈值（小时）- 超过此时间未结束的会话将被上传
ZOMBIE_SESSION_HOURS: int = 24

# Transcript 上传来源枚举
UPLOAD_SOURCE_AUTO: str = 'auto'  # SessionEnd hook 自动上传
UPLOAD_SOURCE_AUTO_BACKFILL: str = 'auto_backfill'  # 自动后补（僵尸会话）
UPLOAD_SOURCE_MANUAL: str = 'manual'  # 手动执行 sync 命令

# Claude Code projects 目录模式
CLAUDE_PROJECTS_DIR_PATTERN: str = '~/.claude/projects*'

# 排除的 transcript 文件名前缀
EXCLUDED_TRANSCRIPT_PREFIX: str = 'agent-'


def get_auto_scan_enabled() -> bool:
    """
    获取是否启用自动扫描 transcript

    环境变量：DEVLAKE_AUTO_SCAN_ENABLED（默认 True）

    Returns:
        bool: 是否在 UserPromptSubmit hook 中自动扫描并上传 transcript
    """
    value = os.getenv('DEVLAKE_AUTO_SCAN_ENABLED', 'true').lower()
    return value in ('true', '1', 'yes', 'on')


def get_transcript_cache_retention_days() -> int:
    """
    获取 Transcript 缓存保留天数

    环境变量：DEVLAKE_CACHE_RETENTION_DAYS（默认 30 天）

    Returns:
        int: 缓存保留天数
    """
    return int(os.getenv('DEVLAKE_CACHE_RETENTION_DAYS', str(TRANSCRIPT_CACHE_RETENTION_DAYS)))


def get_zombie_session_hours() -> int:
    """
    获取僵尸会话阈值（小时）

    环境变量：DEVLAKE_ZOMBIE_SESSION_HOURS（默认 24 小时）

    Returns:
        int: 僵尸会话阈值（小时）
    """
    return int(os.getenv('DEVLAKE_ZOMBIE_SESSION_HOURS', str(ZOMBIE_SESSION_HOURS)))
