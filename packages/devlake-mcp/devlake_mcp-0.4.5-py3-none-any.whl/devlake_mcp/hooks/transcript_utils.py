#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript 解析工具模块

提供 transcript 文件的解析功能：
- 获取最新用户消息 UUID
- 解析最新的 Claude 响应
- 提取使用的工具列表
- 统计消息数量
- 读取完整内容
- 压缩 transcript 内容
- 安全地解析 Hook 输入 JSON
"""

import json
import logging
import gzip
import base64
import sys
import os
from typing import Optional, Dict, List, Any
from datetime import datetime, timezone, timedelta

from devlake_mcp.constants import (
    TRANSCRIPT_COMPRESSION_THRESHOLD,
    TRANSCRIPT_COMPRESSION_ALGORITHM,
)

# 配置日志（使用标准 Python logging）
logger = logging.getLogger(__name__)

# 时区配置
UTC_PLUS_8 = timezone(timedelta(hours=8))


def convert_to_utc_plus_8(iso_timestamp: str) -> str:
    """
    将 ISO 8601 格式的时间戳转换为 UTC+8 时区

    Args:
        iso_timestamp: ISO 8601 格式时间戳，如 "2025-11-03T05:39:16.109Z"

    Returns:
        UTC+8 时区的 ISO 8601 格式时间戳，如 "2025-11-03T13:39:16.109+08:00"
    """
    try:
        if not iso_timestamp:
            return None

        # 解析 ISO 8601 时间戳
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))

        # 转换为 UTC+8
        dt_utc8 = dt.astimezone(UTC_PLUS_8)

        # 返回 ISO 格式（保留时区信息）
        return dt_utc8.isoformat()
    except Exception as e:
        logger.error(f"Failed to convert timestamp {iso_timestamp}: {e}")
        return iso_timestamp  # 转换失败时返回原始值


def get_latest_user_message_uuid(transcript_path: str) -> Optional[str]:
    """
    获取最新的用户消息 UUID

    如果找不到用户消息的 UUID，则尝试从 summary 中获取 leafUuid

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        最新用户消息的 UUID，或者 summary 的 leafUuid，如果都没有返回 None
    """
    logger.debug(f"开始获取最新用户消息 UUID，transcript: {transcript_path}")

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            logger.debug(f"读取到 {len(lines)} 行数据")

            # 从后往前找第一个 type='user' 的消息
            user_msg_count = 0
            for line in reversed(lines):
                try:
                    msg = json.loads(line.strip())
                    if msg.get('type') == 'user':
                        user_msg_count += 1
                        msg_uuid = msg.get('uuid')
                        logger.debug(f"找到第 {user_msg_count} 个 user 消息，UUID: {msg_uuid}")
                        if msg_uuid:
                            logger.debug(f"成功获取用户消息 UUID: {msg_uuid}")
                            return msg_uuid
                except json.JSONDecodeError:
                    continue

            logger.debug(f"未找到有效的 user 消息 UUID，尝试从 summary 获取 leafUuid")

            # 如果没有找到 user 消息的 UUID，尝试从 summary 中获取 leafUuid
            for line in reversed(lines):
                try:
                    msg = json.loads(line.strip())
                    if msg.get('type') == 'summary':
                        leaf_uuid = msg.get('leafUuid')
                        if leaf_uuid:
                            logger.info(f"未找到用户消息 UUID，使用 summary 的 leafUuid: {leaf_uuid}")
                            return leaf_uuid
                except json.JSONDecodeError:
                    continue

    except FileNotFoundError:
        logger.error(f"Transcript 文件不存在: {transcript_path}")
    except Exception as e:
        logger.error(f"Failed to get latest user message UUID: {e}")

    # 无法获取任何 UUID
    logger.warning(f"无法从 transcript 获取 UUID 或 leafUuid")
    return None


def parse_latest_response(transcript_path: str) -> Optional[Dict]:
    """
    解析最新的 Claude 响应（等待完整响应）

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        响应消息字典，包含 uuid、parent_uuid、content、usage、timestamp、model
        如果不存在返回 None
    """
    try:
        import time
        max_wait = 5  # 最多等待 5 秒
        wait_interval = 0.1  # 每次等待 100ms
        elapsed = 0

        while elapsed < max_wait:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                logger.debug(f"读取 transcript: {transcript_path}, 行数: {len(lines)}")
                # 从后往前找第一个 type='assistant' 的消息
                for line in reversed(lines):
                    try:
                        msg = json.loads(line.strip())
                        if msg.get('type') == 'assistant':
                            message_obj = msg.get('message', {})
                            usage = message_obj.get('usage', {})
                            output_tokens = usage.get('output_tokens', 0)

                            # 确保响应已完成：output_tokens > 1（避免只获取到第一个 token）
                            # 或者有 stop_reason
                            stop_reason = message_obj.get('stop_reason')
                            if output_tokens > 1 or stop_reason:
                                logger.debug(f"找到完整响应：tokens={output_tokens}, stop_reason={stop_reason}")
                                return {
                                    'uuid': msg.get('uuid'),
                                    'parent_uuid': msg.get('parentUuid'),
                                    'content': message_obj.get('content', []),
                                    'usage': usage,
                                    'timestamp': msg.get('timestamp'),
                                    'model': message_obj.get('model')
                                }
                            else:
                                # 响应还未完成，继续等待
                                logger.debug(f"响应未完成（tokens={output_tokens}），等待...")
                                break
                    except json.JSONDecodeError:
                        continue

            # 等待一小段时间后重试
            time.sleep(wait_interval)
            elapsed += wait_interval

        # 超时后，返回最后找到的响应（即使不完整）
        logger.warning(f"等待 {max_wait}s 后仍未获取完整响应，返回最后的响应")
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    msg = json.loads(line.strip())
                    if msg.get('type') == 'assistant':
                        message_obj = msg.get('message', {})
                        return {
                            'uuid': msg.get('uuid'),
                            'parent_uuid': msg.get('parentUuid'),
                            'content': message_obj.get('content', []),
                            'usage': message_obj.get('usage', {}),
                            'timestamp': msg.get('timestamp'),
                            'model': message_obj.get('model')
                        }
                except json.JSONDecodeError:
                    continue

    except Exception as e:
        logger.error(f"Failed to parse latest response: {e}")

    return None


def extract_tools_used(response_message: Dict) -> List[str]:
    """
    从响应中提取使用的工具列表

    Args:
        response_message: 响应消息字典（由 parse_latest_response 返回）

    Returns:
        工具名称列表，如 ['Edit', 'Bash', 'Read']
    """
    tools = set()
    try:
        content = response_message.get('content', [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    tool_name = item.get('name', '')
                    if tool_name:
                        tools.add(tool_name)
    except Exception as e:
        logger.error(f"Failed to extract tools: {e}")

    return list(tools)


def count_user_messages(transcript_path: str) -> int:
    """
    统计 transcript 中的用户消息数量

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        用户消息数量
    """
    count = 0
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line.strip())
                    if msg.get('type') == 'user':
                        count += 1
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        logger.error(f"Failed to count user messages: {e}")

    return count


def read_transcript_content(transcript_path: str) -> str:
    """
    读取 transcript 文件的完整内容

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        完整的 JSONL 内容（字符串）
    """
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read transcript: {e}")
        return ''


def get_user_message_by_uuid(transcript_path: str, user_uuid: str) -> Optional[Dict]:
    """
    根据 UUID 获取完整的 user 消息信息

    Args:
        transcript_path: Transcript 文件路径
        user_uuid: 用户消息的 UUID

    Returns:
        用户消息字典，包含 uuid、content、timestamp 等完整信息
        如果不存在返回 None
    """
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line.strip())
                    if msg.get('uuid') == user_uuid and msg.get('type') == 'user':
                        # user 消息的内容在 message.content 中
                        message_obj = msg.get('message', {})
                        content = message_obj.get('content', '')

                        return {
                            'uuid': msg.get('uuid'),
                            'content': content,
                            'timestamp': msg.get('timestamp'),
                            'parent_uuid': msg.get('parentUuid'),
                            # 提取额外的元数据（如果存在）
                            'cwd': msg.get('cwd'),
                            'permission_mode': msg.get('permissionMode'),
                            'raw_message': msg  # 保留原始消息，以备需要
                        }
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        logger.error(f"Failed to get user message by UUID {user_uuid}: {e}")

    return None


def trace_to_user_message(transcript_path: str, start_uuid: str, max_depth: int = 100) -> Optional[str]:
    """
    从给定的 UUID 追溯到最初的 user 消息（排除 tool_result 类型的 user 消息）

    用于处理：
    1. thinking 消息链：user → assistant(thinking) → assistant(thinking) → assistant(response)
    2. tool_result 消息链：user(prompt) → assistant(tool_use) → user(tool_result) → assistant(response)
    3. 复杂的消息链：包含多个工具调用、hook 触发、system 消息等

    Args:
        transcript_path: Transcript 文件路径
        start_uuid: 起始 UUID（通常是 assistant 消息的 parentUuid）
        max_depth: 最大追溯深度（防止死循环），默认 100 步

    Returns:
        最初的 user 消息 UUID（内容是真正的用户输入，而非 tool_result），如果未找到或超过深度限制返回 None

    注意：
        在包含大量工具调用和 hooks 的复杂对话中，追溯深度可能超过 20 步。
        例如：user → assistant(tool_use) → user(tool_result) → system(hook) → assistant(thinking) → ...
    """
    try:
        # 构建 UUID -> 消息的映射
        uuid_to_message = {}
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line.strip())
                    uuid_to_message[msg.get('uuid')] = msg
                except json.JSONDecodeError:
                    continue

        # 从 start_uuid 开始追溯
        current_uuid = start_uuid
        depth = 0

        while current_uuid and depth < max_depth:
            msg = uuid_to_message.get(current_uuid)
            if not msg:
                # UUID 不存在，停止追溯
                logger.warning(f"UUID {current_uuid} not found in transcript")
                return None

            msg_type = msg.get('type')

            if msg_type == 'user':
                # 检查是否是 tool_result 类型的 user 消息
                message_obj = msg.get('message', {})
                content = message_obj.get('content', '')

                # 如果 content 是列表且包含 tool_result，继续往上追溯
                if isinstance(content, list):
                    has_tool_result = any(
                        isinstance(item, dict) and item.get('type') == 'tool_result'
                        for item in content
                    )
                    if has_tool_result:
                        # 这是 tool_result 类型的 user 消息，继续追溯
                        logger.debug(f"跳过 tool_result 类型的 user 消息: {current_uuid}")
                        parent_uuid = msg.get('parentUuid')
                        if parent_uuid:
                            current_uuid = parent_uuid
                            depth += 1
                            continue
                        else:
                            logger.warning(f"tool_result user message {current_uuid} has no parentUuid")
                            return None

                # 找到真正的 user 消息，返回
                logger.debug(f"找到真实 user 消息: {current_uuid}")
                return current_uuid

            elif msg_type == 'assistant':
                # 继续向上追溯
                parent_uuid = msg.get('parentUuid')
                if not parent_uuid:
                    logger.warning(f"No parentUuid for assistant message {current_uuid}")
                    return None
                current_uuid = parent_uuid
            else:
                # 跳过其他类型（如 system、file-history-snapshot 等），继续追溯
                parent_uuid = msg.get('parentUuid')
                if parent_uuid:
                    current_uuid = parent_uuid
                else:
                    logger.warning(f"No parentUuid for message type {msg_type}: {current_uuid}")
                    return None

            depth += 1

        if depth >= max_depth:
            logger.warning(f"Exceeded max depth {max_depth} when tracing from {start_uuid}")

        return None

    except Exception as e:
        logger.error(f"Failed to trace to user message: {e}")
        return None


def get_transcript_stats(transcript_path: str) -> Dict:
    """
    获取 transcript 的统计信息

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        统计信息字典
    """
    try:
        import os

        user_count = 0
        assistant_count = 0

        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    msg = json.loads(line.strip())
                    msg_type = msg.get('type')
                    if msg_type == 'user':
                        user_count += 1
                    elif msg_type == 'assistant':
                        assistant_count += 1
                except json.JSONDecodeError:
                    continue

        file_size = os.path.getsize(transcript_path) if os.path.exists(transcript_path) else 0

        return {
            'user_messages': user_count,
            'assistant_messages': assistant_count,
            'total_messages': user_count + assistant_count,
            'file_size_bytes': file_size,
            'file_size_kb': round(file_size / 1024, 2)
        }
    except Exception as e:
        logger.error(f"Failed to get transcript stats: {e}")
        return {
            'user_messages': 0,
            'assistant_messages': 0,
            'total_messages': 0,
            'file_size_bytes': 0,
            'file_size_kb': 0.0
        }


def compress_transcript_content(
    content: str,
    threshold_bytes: int = TRANSCRIPT_COMPRESSION_THRESHOLD
) -> Dict[str, Any]:
    """
    智能压缩 transcript 内容

    根据内容大小自动判断是否需要压缩：
    - 大于阈值：使用 gzip 压缩 + base64 编码
    - 小于阈值：直接返回原始内容

    Args:
        content: 原始 JSONL 内容（字符串）
        threshold_bytes: 压缩阈值（字节），默认使用 TRANSCRIPT_COMPRESSION_THRESHOLD

    Returns:
        Dict[str, Any]: {
            'content': str,           # 处理后的内容（压缩+base64 或原始）
            'compression': str,        # 压缩类型：'gzip' 或 'none'
            'original_size': int,      # 原始大小（字节）
            'compressed_size': int,    # 处理后大小（字节）
            'compression_ratio': float # 压缩率（百分比，0-100）
        }

    异常处理：
        如果压缩过程失败，会自动降级为不压缩，返回原始内容。

    示例：
        >>> content = read_transcript_content('/path/to/transcript.jsonl')
        >>> result = compress_transcript_content(content)
        >>> if result['compression'] == 'gzip':
        >>>     logger.info(f"压缩率: {result['compression_ratio']:.1f}%")
    """
    try:
        # 1. 计算原始大小
        content_bytes = content.encode('utf-8')
        original_size = len(content_bytes)

        # 2. 判断是否需要压缩
        if original_size <= threshold_bytes:
            # 不压缩，直接返回原始内容
            logger.debug(
                f"Transcript 大小 {original_size} bytes <= {threshold_bytes} bytes，不压缩"
            )
            return {
                'content': content,
                'compression': 'none',
                'original_size': original_size,
                'compressed_size': original_size,
                'compression_ratio': 0.0
            }

        # 3. 执行压缩
        logger.debug(
            f"Transcript 大小 {original_size} bytes > {threshold_bytes} bytes，开始压缩"
        )

        # gzip 压缩（使用最大压缩级别）
        compressed_bytes = gzip.compress(content_bytes, compresslevel=9)
        compressed_size = len(compressed_bytes)

        # base64 编码（以便在 JSON 中传输）
        encoded_content = base64.b64encode(compressed_bytes).decode('ascii')

        # 4. 计算压缩率
        compression_ratio = (1 - compressed_size / original_size) * 100

        logger.info(
            f"压缩完成：{original_size} bytes → {compressed_size} bytes "
            f"(压缩率: {compression_ratio:.1f}%)"
        )

        return {
            'content': encoded_content,
            'compression': TRANSCRIPT_COMPRESSION_ALGORITHM,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(compression_ratio, 2)
        }

    except Exception as e:
        # 压缩失败，降级为不压缩
        logger.error(f"压缩 transcript 失败，使用原始内容: {e}", exc_info=True)

        original_size = len(content.encode('utf-8'))
        return {
            'content': content,
            'compression': 'none',
            'original_size': original_size,
            'compressed_size': original_size,
            'compression_ratio': 0.0
        }


def extract_session_id(transcript_path: str) -> Optional[str]:
    """
    从 transcript 文件中提取 session_id

    提取策略：
    1. 优先从任意消息的 sessionId 字段提取
    2. 如果提取失败，从文件名提取（备用方案）

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        session_id，如果无法提取返回 None
    """
    logger.debug(f"开始提取 session_id，transcript: {transcript_path}")

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            # 读取第一行（通常包含 sessionId）
            first_line = f.readline()
            if not first_line:
                logger.warning(f"Transcript 文件为空: {transcript_path}")
                return _extract_session_id_from_filename(transcript_path)

            msg = json.loads(first_line.strip())
            session_id = msg.get('sessionId')

            if session_id:
                logger.debug(f"从消息中提取到 session_id: {session_id}")
                return session_id

            # 策略 2: 从文件名提取（备用）
            logger.debug(f"消息中未找到 sessionId，尝试从文件名提取")
            return _extract_session_id_from_filename(transcript_path)

    except json.JSONDecodeError as e:
        logger.warning(f"解析 JSON 失败: {e}，尝试从文件名提取")
        return _extract_session_id_from_filename(transcript_path)
    except Exception as e:
        logger.error(f"提取 session_id 失败: {e}")
        # 最后尝试从文件名提取
        return _extract_session_id_from_filename(transcript_path)


def _extract_session_id_from_filename(transcript_path: str) -> Optional[str]:
    """
    从文件名提取 session_id

    支持格式：
    - 普通会话: {uuid}.jsonl -> uuid
    - Agent 会话: agent-{short_id}.jsonl -> agent-{short_id}

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        session_id，如果无法提取返回 None
    """
    import re
    from pathlib import Path

    filename = Path(transcript_path).stem  # 去除 .jsonl 后缀

    # UUID 格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if re.match(uuid_pattern, filename, re.IGNORECASE):
        logger.debug(f"从文件名提取到 UUID session_id: {filename}")
        return filename

    # Agent 格式: agent-{short_id}
    if filename.startswith('agent-'):
        logger.debug(f"从文件名提取到 Agent session_id: {filename}")
        return filename

    logger.warning(f"无法从文件名提取 session_id: {filename}")
    return None


def get_session_start_time(transcript_path: str) -> Optional[datetime]:
    """
    提取会话开始时间

    从第一条有 timestamp 的消息中提取（跳过 summary 等没有 timestamp 的消息）

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        会话开始时间（datetime 对象），如果无法提取返回 None
    """
    logger.debug(f"开始提取会话开始时间，transcript: {transcript_path}")

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            # 遍历消息，找到第一条有 timestamp 的消息
            for line_num, line in enumerate(f, start=1):
                if not line.strip():
                    continue

                try:
                    msg = json.loads(line.strip())
                    timestamp_str = msg.get('timestamp')

                    if timestamp_str:
                        # 解析 ISO 8601 时间戳
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        logger.debug(f"从第 {line_num} 行找到会话开始时间: {timestamp}")
                        return timestamp
                except json.JSONDecodeError as e:
                    logger.debug(f"跳过第 {line_num} 行（JSON 解析失败）: {e}")
                    continue

        # 未找到任何有 timestamp 的消息
        logger.warning(f"未找到任何有 timestamp 的消息: {transcript_path}")
        return None

    except (ValueError) as e:
        logger.error(f"解析会话开始时间失败: {e}")
        return None
    except Exception as e:
        logger.error(f"提取会话开始时间失败: {e}")
        return None


def is_session_ended(transcript_path: str) -> bool:
    """
    判断会话是否已结束

    检查 transcript 文件中是否包含 summary 消息

    Args:
        transcript_path: Transcript 文件路径

    Returns:
        True 表示会话已结束，False 表示正在进行中
    """
    logger.debug(f"检查会话是否已结束，transcript: {transcript_path}")

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 从后往前查找 summary 消息（通常在最后）
        for line in reversed(lines):
            try:
                msg = json.loads(line.strip())
                if msg.get('type') == 'summary':
                    logger.debug(f"会话已结束（找到 summary 消息）: {transcript_path}")
                    return True
            except json.JSONDecodeError:
                continue

        logger.debug(f"会话正在进行中（未找到 summary 消息）: {transcript_path}")
        return False

    except Exception as e:
        logger.error(f"检查会话状态失败: {e}")
        return False


def safe_parse_hook_input(logger: logging.Logger = None) -> Optional[Dict[str, Any]]:
    """
    安全地解析来自 stdin 的 Hook 输入 JSON

    功能：
    1. 读取 stdin 原始数据
    2. 检查空输入
    3. 尝试解析 JSON
    4. 记录详细的错误信息
    5. 保存失败的输入到调试文件

    参数:
        logger: 日志记录器（如果为 None，使用模块级 logger）

    返回:
        Dict[str, Any]: 解析成功的 JSON 数据
        None: 解析失败或输入为空

    使用示例:
        # 在 hook 脚本中
        input_data = safe_parse_hook_input(logger)
        if not input_data:
            return  # 解析失败，直接返回

        # 继续处理 input_data
        session_id = input_data.get('session_id')
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    try:
        # 1. 读取原始数据
        raw_input = sys.stdin.read()

        # 2. 检查是否为空
        if not raw_input or not raw_input.strip():
            logger.warning('stdin 为空，跳过处理')
            return None

        # 3. 尝试解析 JSON
        try:
            return json.loads(raw_input)

        except json.JSONDecodeError as json_err:
            # JSON 解析失败时，记录详细错误信息
            logger.error(f'JSON 解析失败: {json_err}')
            logger.debug(f'原始输入长度: {len(raw_input)} 字符')

            # 记录错误位置附近的内容（帮助调试）
            if hasattr(json_err, 'pos') and json_err.pos:
                start = max(0, json_err.pos - 100)
                end = min(len(raw_input), json_err.pos + 100)
                context = raw_input[start:end]
                # 清理不可打印字符
                context = context.replace('\n', '\\n').replace('\r', '\\r')
                logger.debug(f'错误位置附近内容: ...{context}...')

            # 尝试记录到临时文件以供分析
            try:
                debug_file = os.path.expanduser('~/.devlake/debug_hook_input.txt')
                os.makedirs(os.path.dirname(debug_file), exist_ok=True)
                with open(debug_file, 'a', encoding='utf-8') as f:
                    f.write(f'=== Hook Input Debug ===\n')
                    f.write(f'时间: {datetime.now().isoformat()}\n')
                    f.write(f'错误: {json_err}\n')
                    f.write(f'长度: {len(raw_input)} 字符\n')
                    f.write(f'\n=== 原始内容 ===\n')
                    f.write(raw_input)
                logger.info(f'原始输入已保存到: {debug_file}')
            except Exception as save_err:
                logger.warning(f'保存调试文件失败: {save_err}')

            return None

    except Exception as e:
        logger.error(f'读取 stdin 失败: {e}', exc_info=True)
        return None
