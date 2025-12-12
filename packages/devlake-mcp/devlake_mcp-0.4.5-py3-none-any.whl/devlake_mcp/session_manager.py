#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话生命周期管理模块

功能：
1. 创建新会话（调用 API）
2. 结束会话（调用 API 更新 session_end_time）
3. 支持 Cursor 和 Claude Code 两种模式

设计原则：
- 无本地状态管理（移除基于 PID 的状态文件）
- 依赖后端 API 的幂等性保证数据一致性
- 每次调用都直接与后端交互

使用方式：
    from devlake_mcp.session_manager import start_new_session

    # SessionStart/UserPromptSubmit hook：创建或确保 session 存在
    start_new_session(
        session_id=session_id,
        cwd=cwd,
        ide_type='claude_code'
    )
    # 直接调用 API 创建 session，后端通过幂等性处理重复请求
"""

import json
import logging
from datetime import datetime
from typing import Union
import os

from .client import DevLakeClient
from .retry_queue import save_failed_upload
from .git_utils import get_git_info, get_git_repo_path
from .version_utils import detect_platform_info
from .enums import IDEType

# 配置日志
logger = logging.getLogger(__name__)


# ============================================================================
# 核心 API
# ============================================================================


def _create_session_record(session_id: str, cwd: str, ide_type: Union[IDEType, str] = IDEType.CLAUDE_CODE):
    """
    创建 session 记录（上传到 DevLake API）

    Args:
        session_id: Session ID
        cwd: 当前工作目录
        ide_type: IDE 类型枚举
    """
    session_data = None
    try:
        ide_type_str = ide_type.value if isinstance(ide_type, IDEType) else str(ide_type)

        # 1. 获取 Git 信息（动态 + 静态）
        git_info = get_git_info(cwd, timeout=1, include_user_info=True)
        git_branch = git_info.get('git_branch', 'unknown')
        git_commit = git_info.get('git_commit', 'unknown')
        git_author = git_info.get('git_author', 'unknown')
        git_email = git_info.get('git_email', 'unknown')

        # 2. 获取 Git 仓库路径（namespace/name）
        git_repo_path = get_git_repo_path(cwd)

        # 3. 从 git_repo_path 提取 project_name
        project_name = git_repo_path.split('/')[-1] if '/' in git_repo_path else git_repo_path

        # 4. 检测平台信息和版本
        platform_info = detect_platform_info(ide_type=ide_type)

        # 5. 构造 session 数据
        session_data = {
            'session_id': session_id,
            'user_name': git_author,
            'ide_type': ide_type_str,
            'model_name': os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5'),
            'git_repo_path': git_repo_path,
            'project_name': project_name,
            'cwd': cwd,
            'session_start_time': datetime.now().isoformat(),
            'conversation_rounds': 0,
            'is_adopted': 0,
            'git_branch': git_branch,
            'git_commit': git_commit,
            'git_author': git_author,
            'git_email': git_email,
            # 新增：版本信息
            'devlake_mcp_version': platform_info['devlake_mcp_version'],
            'ide_version': platform_info['ide_version'],
            'data_source': platform_info['data_source']
        }

        logger.info(
            f'准备创建 Session: {session_id}, '
            f'repo: {git_repo_path}, branch: {git_branch}, '
            f'ide: {ide_type_str} {platform_info["ide_version"] or "unknown"}, '
            f'devlake-mcp: {platform_info["devlake_mcp_version"]}'
        )
        logger.debug(f'session_data 内容: {json.dumps(session_data, ensure_ascii=False, indent=2)}')

        # 5. 调用 DevLake API 创建 session
        with DevLakeClient() as client:
            client.post('/api/ai-coding/sessions', session_data)

        logger.info(f'成功创建 Session: {session_id}')

    except Exception as e:
        # API 调用失败，记录错误但不阻塞
        logger.error(f'创建 Session 失败 ({session_id}): {e}')
        # 保存到本地队列（支持自动重试）
        if session_data:
            save_failed_upload(
                queue_type='session',
                data=session_data,
                error=str(e)
            )


def start_new_session(session_id: str, cwd: str, ide_type: Union[IDEType, str] = IDEType.CLAUDE_CODE):
    """
    开始新会话（SessionStart 专用）

    Args:
        session_id: 会话 ID
        cwd: 当前工作目录（用于获取 Git 信息）
        ide_type: IDE 类型 (IDEType 枚举或字符串，默认 Claude Code)

    行为:
        直接调用 API 创建会话，后端通过幂等性处理重复请求

    用途:
        SessionStart hook 调用，确保会话存在
    """
    # 参数验证
    if not session_id:
        logger.warning('session_id 为空，跳过')
        return

    # 转换为枚举类型（如果是字符串）
    ide_type_enum = IDEType.from_string(ide_type) if isinstance(ide_type, str) else ide_type

    # 创建会话（后端处理幂等性）
    logger.info(f'确保会话存在: {session_id} ({ide_type_enum.value})')
    _create_session_record(session_id, cwd, ide_type_enum)


def end_session(session_id: str, ide_type: Union[IDEType, str] = IDEType.CLAUDE_CODE):
    """
    结束指定会话（更新 session_end_time）

    Args:
        session_id: 要结束的会话 ID
        ide_type: IDE 类型 (IDEType 枚举或字符串，默认 Claude Code)

    行为:
        1. 调用 DevLake API 更新 session_end_time
        2. 如果 API 调用失败，保存到重试队列
        3. 不抛出异常，静默失败
    """
    try:
        ide_type_str = ide_type.value if isinstance(ide_type, IDEType) else str(ide_type)

        # 构造更新数据
        update_data = {
            'session_end_time': datetime.now().isoformat()
        }

        logger.info(f'准备结束会话: {session_id} ({ide_type_str})')

        # 调用 DevLake API
        with DevLakeClient() as client:
            client.update_session(session_id, update_data)

        logger.info(f'会话已结束: {session_id}')

    except Exception as e:
        # API 调用失败，记录错误并保存到重试队列
        logger.error(f'结束会话失败 ({session_id}): {e}')

        # 保存到重试队列（支持自动重试）
        save_failed_upload(
            queue_type='session',
            data={
                'session_id': session_id,
                'ide_type': ide_type_str,
                **update_data
            },
            error=str(e)
        )


