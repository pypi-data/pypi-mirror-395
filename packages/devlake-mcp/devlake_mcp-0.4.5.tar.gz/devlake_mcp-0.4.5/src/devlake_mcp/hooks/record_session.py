#!/usr/bin/env python3
"""
记录 AI 编码会话信息（SessionEnd Hook）

触发时机：会话真正结束时（/clear、logout、退出程序等）
触发频率：每个会话只触发一次

功能：
1. 统计对话轮次（从 transcript）
2. 更新会话记录（PATCH /api/ai-coding/sessions/{session_id}）
3. 上传 transcript 完整内容（POST /api/ai-coding/transcripts）
4. API 后端自动计算会话时长

注意：
- 不要放在 Stop hook 中，那会在每次对话结束时触发（多次调用）
- SessionEnd 才是真正的会话结束，只触发一次
"""

import json
import sys
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# 导入公共工具（使用包导入）
from devlake_mcp.hooks.transcript_utils import (
    count_user_messages,
    read_transcript_content,
    compress_transcript_content,
    safe_parse_hook_input,
)
from devlake_mcp.hooks.hook_utils import run_async
from devlake_mcp.client import DevLakeClient
from devlake_mcp.retry_queue import save_failed_upload
from devlake_mcp.logging_config import configure_logging, get_log_dir
from devlake_mcp.constants import HOOK_LOG_DIR
from devlake_mcp.generation_manager import end_generation
from devlake_mcp.enums import IDEType
from devlake_mcp.git_utils import get_git_info

# 配置日志（启动时调用一次）
configure_logging(log_dir=get_log_dir(HOOK_LOG_DIR), log_file='record_session.log')
logger = logging.getLogger(__name__)


def _validate_input(input_data: dict) -> Optional[Tuple[str, str]]:
    """验证输入数据的有效性

    Args:
        input_data: Hook 输入数据

    Returns:
        tuple[session_id, transcript_path] 或 None（验证失败时）
    """
    hook_event_name = input_data.get('hook_event_name')
    if hook_event_name != 'SessionEnd':
        return None

    session_id = input_data.get('session_id')
    if not session_id:
        return None

    transcript_path = input_data.get('transcript_path', '')
    return session_id, transcript_path


def _update_session(client: DevLakeClient, session_id: str, conversation_rounds: int) -> None:
    """更新会话记录

    Args:
        client: DevLake 客户端
        session_id: 会话 ID
        conversation_rounds: 对话轮次
    """
    update_data = {
        'session_id': session_id,
        'session_end_time': datetime.now().isoformat(),
        'conversation_rounds': conversation_rounds
    }

    try:
        client.update_session(session_id, update_data)
    except Exception as e:
        logger.error(f'Failed to update session {session_id}', exc_info=True)
        # 保存到本地队列（支持自动重试）
        save_failed_upload(
            queue_type='session',
            data=update_data,
            error=str(e)
        )


def _upload_transcript(client: DevLakeClient, session_id: str,
                      transcript_path: str, conversation_rounds: int) -> None:
    """上传 transcript 内容（支持智能压缩）

    Args:
        client: DevLake 客户端
        session_id: 会话 ID
        transcript_path: transcript 文件路径
        conversation_rounds: 对话轮次

    功能：
        1. 读取 transcript 原始内容
        2. 智能压缩（大于 1MB 时自动启用 gzip 压缩）
        3. 上传到 DevLake API
        4. 失败时保存到重试队列
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return

    transcript_data = None
    try:
        # 1. 读取原始内容
        transcript_content = read_transcript_content(transcript_path)
        original_size = os.path.getsize(transcript_path)

        # 2. 智能压缩
        compression_result = compress_transcript_content(transcript_content)

        # 3. 获取 git 用户信息
        cwd = os.getcwd()
        git_info = get_git_info(cwd, include_user_info=True)
        git_author = git_info.get('git_author')
        git_email = git_info.get('git_email')
        # 如果获取失败或为 'unknown',则设为 None
        if git_author == 'unknown':
            git_author = None
        if git_email == 'unknown':
            git_email = None

        # 4. 准备上传数据
        transcript_data = {
            'session_id': session_id,
            'transcript_path': transcript_path,
            'transcript_content': compression_result['content'],
            'compression': compression_result['compression'],
            'original_size': compression_result['original_size'],
            'compressed_size': compression_result['compressed_size'],
            'compression_ratio': compression_result.get('compression_ratio', 0.0),
            'message_count': conversation_rounds,
            'upload_time': datetime.now().isoformat(),
            'git_author': git_author,
            'git_email': git_email,
        }

        # 5. 上传
        client.create_transcript(transcript_data)

        # 6. 记录日志
        if compression_result['compression'] == 'gzip':
            logger.info(
                f"Transcript 上传成功 (已压缩): {session_id}, "
                f"原始大小: {original_size} bytes, "
                f"压缩后: {compression_result['compressed_size']} bytes, "
                f"压缩率: {compression_result['compression_ratio']:.1f}%"
            )
        else:
            logger.info(
                f"Transcript 上传成功 (未压缩): {session_id}, "
                f"大小: {original_size} bytes"
            )

    except Exception as e:
        logger.error(f'Failed to upload transcript for {session_id}', exc_info=True)
        # 保存到本地队列（支持自动重试）
        if transcript_data:
            save_failed_upload(
                queue_type='transcript',
                data=transcript_data,
                error=str(e)
            )


@run_async
def main():
    """
    SessionEnd Hook 主逻辑：记录会话结束信息

    注意：所有异常都被捕获并静默处理，确保不阻塞 Claude
    """
    try:
        # 1. 读取并验证输入（使用安全解析函数）
        input_data = safe_parse_hook_input(logger)
        if not input_data:
            return  # 解析失败，跳过处理

        validation_result = _validate_input(input_data)
        if not validation_result:
            return

        session_id, transcript_path = validation_result

        # 2. 统计对话轮次
        conversation_rounds = count_user_messages(transcript_path)

        # 3. 初始化客户端（复用）
        client = DevLakeClient()

        # 4. 更新会话记录
        _update_session(client, session_id, conversation_rounds)

        # 5. 上传 transcript 内容
        _upload_transcript(client, session_id, transcript_path, conversation_rounds)

        # 6. 清理 generation 状态文件（防止文件堆积）
        try:
            end_generation(session_id, ide_type=IDEType.CLAUDE_CODE)
            logger.info(f'已清理 generation 状态文件: {session_id}')
        except Exception as e:
            # 清理失败不影响主流程
            logger.warning(f'清理 generation 状态文件失败: {e}')

        logger.info(f'会话记录完成: {session_id}')

    except Exception:
        # 任何异常都静默失败，不阻塞 Claude
        logger.error('SessionEnd hook failed', exc_info=True)


if __name__ == '__main__':
    main()
    sys.exit(0)  # 唯一的 exit 点
