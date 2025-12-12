#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建完整的 Prompt 记录（Stop Hook）

触发时机：Claude 完成一次回复时
触发频率：每次 Claude 完成回复时触发一次

功能：
1. 从 transcript 解析用户 prompt 的完整信息（内容、提交时间、UUID等）
2. 从 transcript 解析 Claude 响应信息（tokens、工具使用、结束时间等）
3. 计算 prompt 序号
4. 一次性创建完整的 prompt 记录（包含开始和结束信息）
5. 增量更新 session 的 conversation_rounds
6. 异步执行，立即返回，不阻塞 Claude 的下一次响应
"""

import json
import logging
import sys
import os
from pathlib import Path
from datetime import datetime

# 导入公共工具（使用包导入）
from devlake_mcp.hooks.hook_utils import run_async
from devlake_mcp.hooks.transcript_utils import (
    parse_latest_response,
    extract_tools_used,
    trace_to_user_message,
    get_user_message_by_uuid,
    count_user_messages,
    convert_to_utc_plus_8,
    safe_parse_hook_input,
)
from devlake_mcp.client import DevLakeClient
from devlake_mcp.retry_queue import save_failed_upload
from devlake_mcp.generation_manager import get_current_generation_id
from devlake_mcp.logging_config import configure_logging, get_log_dir
from devlake_mcp.constants import HOOK_LOG_DIR

# 配置日志（启动时调用一次）
configure_logging(log_dir=get_log_dir(HOOK_LOG_DIR), log_file='stop_hook.log')
logger = logging.getLogger(__name__)


def extract_usage_data(latest_response: dict) -> dict:
    """
    从响应中提取完整的 usage 数据

    Args:
        latest_response: Claude 响应消息字典

    Returns:
        usage 数据字典，包含 input_tokens、cache tokens、output_tokens、model
    """
    usage = latest_response.get('usage', {})

    # 提取所有 token 相关数据
    usage_data = {
        'input_tokens': usage.get('input_tokens', 0),
        'output_tokens': usage.get('output_tokens', 0),
        'cache_creation_input_tokens': usage.get('cache_creation_input_tokens', 0),
        'cache_read_input_tokens': usage.get('cache_read_input_tokens', 0),
        'model': latest_response.get('model')
    }

    logger.debug(f"提取的 usage 数据: {usage_data}")
    return usage_data


def extract_response_content(latest_response: dict) -> str:
    """
    提取响应内容的文本部分

    Args:
        latest_response: Claude 响应消息字典

    Returns:
        完整的响应内容文本
    """
    response_content = ""
    content = latest_response.get('content', [])

    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get('type') == 'text':
                text = item.get('text', '')
                response_content = text if text else ""
                break

    return response_content


def calculate_prompt_duration(user_message: dict, latest_response: dict) -> int:
    """
    计算 prompt 时长

    Args:
        user_message: 用户消息字典
        latest_response: Claude 响应消息字典

    Returns:
        时长（秒），如果计算失败返回 None
    """
    try:
        submit_time_str = user_message.get('timestamp')
        end_time_str = latest_response.get('timestamp')

        if not submit_time_str or not end_time_str:
            return None

        submit_time = datetime.fromisoformat(submit_time_str.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        duration_delta = end_time - submit_time

        return int(duration_delta.total_seconds())
    except Exception as e:
        logger.error(f'计算 prompt 时长失败: {e}')
        return None


@run_async
def main():
    """
    Stop Hook 主逻辑

    注意：所有异常都被捕获并静默处理，确保不阻塞 Claude
    """
    try:
        # 1. 从 stdin 读取 hook 输入（使用安全解析函数）
        input_data = safe_parse_hook_input(logger)
        if not input_data:
            return  # 解析失败，跳过处理

        session_id = input_data.get('session_id')
        transcript_path = input_data.get('transcript_path')
        permission_mode = input_data.get('permission_mode')

        logger.debug(f'Stop Hook 触发 - session: {session_id}, transcript: {transcript_path}')

        if not session_id or not transcript_path:
            logger.warning('缺少必要的 session_id 或 transcript_path')
            return

        if not os.path.exists(transcript_path):
            logger.info(f'Transcript 文件尚不存在（可能是新会话初始化）: {transcript_path}')
            return

        # 2. 解析 transcript 获取最新的 Claude 响应
        latest_response = parse_latest_response(transcript_path)
        if not latest_response:
            logger.warning('无法解析最新的 Claude 响应')
            return

        logger.debug(f'最新响应 - uuid: {latest_response.get("uuid")}, '
                    f'parent: {latest_response.get("parent_uuid")}, '
                    f'output_tokens: {latest_response.get("usage", {}).get("output_tokens", 0)}')

        # 3. 追溯到最初的 user 消息 UUID（处理 thinking 消息链）
        parent_uuid = latest_response.get('parent_uuid')
        if not parent_uuid:
            logger.error('响应中缺少 parent_uuid')
            return

        # 使用追溯函数找到真正的 user prompt UUID
        prompt_uuid = trace_to_user_message(transcript_path, parent_uuid)
        if not prompt_uuid:
            logger.warning(f'无法追溯到 user 消息（从 {parent_uuid}），可能是工具调用等特殊情况')
            return

        # 4. 获取完整的 user 消息信息
        user_message = get_user_message_by_uuid(transcript_path, prompt_uuid)
        if not user_message:
            logger.error(f'无法获取 user 消息 (UUID: {prompt_uuid})')
            return

        content_preview = user_message.get('content', '')[:100]
        logger.debug(f'User 消息 - uuid: {prompt_uuid}, '
                    f'timestamp: {user_message.get("timestamp")}, '
                    f'content: {content_preview}...')

        # 5. 提取响应信息
        tools_used = extract_tools_used(latest_response)
        usage_data = extract_usage_data(latest_response)
        response_content = extract_response_content(latest_response)
        is_interrupted = '[Request interrupted by user]' in str(latest_response.get('content', ''))
        prompt_duration = calculate_prompt_duration(user_message, latest_response)
        prompt_sequence = count_user_messages(transcript_path)

        # 6. 检查是否有 generation_id（决定使用哪个 UUID）
        generation_id = get_current_generation_id(session_id, ide_type='claude_code')

        # 优先使用 generation_id 作为 prompt_uuid，否则使用 transcript 中的 UUID
        final_prompt_uuid = generation_id if generation_id else prompt_uuid

        logger.debug(f'UUID 选择 - generation_id: {generation_id}, transcript_uuid: {prompt_uuid}, final: {final_prompt_uuid}')

        # 7. 构造完整的 prompt 数据（时区转换为 UTC+8）
        prompt_data = {
            'session_id': session_id,
            'prompt_uuid': final_prompt_uuid,
            'prompt_sequence': prompt_sequence,
            'prompt_content': user_message.get('content', ''),
            'prompt_submit_time': convert_to_utc_plus_8(user_message.get('timestamp')),
            'prompt_end_time': convert_to_utc_plus_8(latest_response.get('timestamp')),
            'prompt_duration': prompt_duration,
            'response_content': response_content if response_content else None,
            'response_tokens': usage_data['output_tokens'],
            'input_tokens': usage_data['input_tokens'],
            'cache_creation_input_tokens': usage_data['cache_creation_input_tokens'],
            'cache_read_input_tokens': usage_data['cache_read_input_tokens'],
            'model': usage_data['model'],
            'tools_used': json.dumps(tools_used) if tools_used else None,
            'cwd': user_message.get('cwd'),
            'permission_mode': permission_mode or user_message.get('permission_mode'),
            'is_interrupted': 1 if is_interrupted else 0
        }

        # 7. 决定创建还是更新
        if generation_id:
            # 情况 1：使用 generation_id（PATCH 更新）
            # 注意：使用 generation_id 作为主键，但从 transcript 获取准确的响应信息
            logger.info(f'准备更新 Prompt 记录: {generation_id}, sequence: {prompt_sequence}')
            logger.debug(f'Prompt 更新数据: {json.dumps(prompt_data, ensure_ascii=False, default=str)}')

            try:
                client = DevLakeClient()
                # 使用 generation_id 作为主键进行更新
                client.update_prompt(generation_id, prompt_data)
                logger.info(f'成功更新 Prompt 记录: {generation_id}')
            except Exception as e:
                logger.error(f'更新 Prompt 失败 ({generation_id}): {e}')
                # 保存到本地队列（支持自动重试）
                save_failed_upload(
                    queue_type='prompt_update',
                    data={'prompt_uuid': generation_id, **prompt_data},
                    error=str(e)
                )

            # 注意：不清空 generation 状态文件
            # 原因：Stop Hook 可能被触发多次（多条 assistant 消息）
            # 状态文件保留到下一次 UserPromptSubmit 时覆盖
            logger.debug(f'Prompt 更新完成，保留 generation 状态: {generation_id}')

        else:
            # 情况 2：向后兼容（POST 创建）
            # 当没有 generation_id 时（例如旧版本或 Hook 未触发），创建新记录
            logger.info(f'准备创建 Prompt 记录: {final_prompt_uuid}, sequence: {prompt_sequence} (向后兼容模式)')
            logger.debug(f'Prompt 数据: {json.dumps(prompt_data, ensure_ascii=False, default=str)}')

            try:
                client = DevLakeClient()
                client.create_prompt(prompt_data)
                logger.info(f'成功创建 Prompt 记录: {final_prompt_uuid}')
            except Exception as e:
                logger.error(f'创建 Prompt 失败 ({final_prompt_uuid}): {e}')
                # 保存到本地队列（支持自动重试）
                save_failed_upload(
                    queue_type='prompt',
                    data=prompt_data,
                    error=str(e)
                )

        # 9. 增量更新 session 的 conversation_rounds
        try:
            client = DevLakeClient()
            client.increment_session_rounds(session_id)
            logger.info(f'成功更新 session 对话轮数: {session_id}')
        except Exception as e:
            logger.error(f'更新 session 对话轮数失败 ({session_id}): {e}')
            # 更新轮数失败不影响主流程，不保存到队列

    except Exception as e:
        # 任何异常都静默失败，不阻塞 Claude
        logger.error(f'Stop Hook 执行失败: {e}', exc_info=True)


if __name__ == '__main__':
    main()
    sys.exit(0)  # 唯一的 exit 点
