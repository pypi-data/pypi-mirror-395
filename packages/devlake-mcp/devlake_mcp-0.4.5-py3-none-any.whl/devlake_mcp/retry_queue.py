#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地队列重试管理器

功能：
1. 保存失败记录（增强版 save_to_local_queue）
2. 扫描并重试失败记录
3. 管理重试状态和清理

设计原则：
- 指数退避策略：1分钟 → 5分钟 → 15分钟 → 60分钟 → 4小时
- 最大重试次数：5次
- 失败记录保留：7天
- 非阻塞执行：不影响主流程
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Literal
from dataclasses import dataclass, asdict

from .utils import get_data_dir
from .client import DevLakeClient
from .config import DevLakeConfig

# 队列类型定义
QueueType = Literal['session', 'prompt', 'prompt_update', 'file_change', 'transcript']

# 模块级 logger
logger = logging.getLogger(__name__)


# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class RetryMetadata:
    """重试元数据"""
    queue_type: str  # session, prompt, prompt_update, file_change, transcript
    api_endpoint: str  # API 端点路径
    created_at: str  # 创建时间（ISO 8601）
    retry_count: int = 0  # 重试次数
    last_retry_at: Optional[str] = None  # 上次重试时间
    next_retry_at: Optional[str] = None  # 下次重试时间
    error_history: List[Dict[str, str]] = None  # 错误历史

    def __post_init__(self):
        if self.error_history is None:
            self.error_history = []


@dataclass
class FailedUpload:
    """失败上传记录"""
    data: Dict[str, Any]  # 原始上传数据
    metadata: RetryMetadata  # 重试元数据


# ============================================================================
# 配置常量（支持环境变量覆盖）
# ============================================================================

def get_retry_config() -> Dict[str, Any]:
    """
    获取重试配置（从环境变量读取）

    环境变量：
    - DEVLAKE_RETRY_ENABLED: 是否启用重试（默认 true）
    - DEVLAKE_RETRY_MAX_ATTEMPTS: 最大重试次数（默认 5）
    - DEVLAKE_RETRY_CLEANUP_DAYS: 失败记录保留天数（默认 7）
    - DEVLAKE_RETRY_CHECK_ON_HOOK: Hook执行时检查重试（默认 true）
    """
    return {
        'enabled': os.getenv('DEVLAKE_RETRY_ENABLED', 'true').lower() == 'true',
        'max_attempts': int(os.getenv('DEVLAKE_RETRY_MAX_ATTEMPTS', '5')),
        'cleanup_days': int(os.getenv('DEVLAKE_RETRY_CLEANUP_DAYS', '7')),
        'check_on_hook': os.getenv('DEVLAKE_RETRY_CHECK_ON_HOOK', 'true').lower() == 'true',
    }


# 指数退避策略（秒）
RETRY_BACKOFF_SCHEDULE = [
    60,      # 第1次重试：1分钟后
    300,     # 第2次重试：5分钟后
    900,     # 第3次重试：15分钟后
    3600,    # 第4次重试：60分钟后
    14400,   # 第5次重试：4小时后
]

# 队列类型到 API 端点的映射
QUEUE_TYPE_TO_ENDPOINT = {
    'session': '/api/ai-coding/sessions',
    'prompt': '/api/ai-coding/prompts',
    'prompt_update': '/api/ai-coding/prompts',  # 更新操作使用相同端点
    'file_change': '/api/ai-coding/file-changes',
    'transcript': '/api/ai-coding/transcripts',
}

# 队列目录名称映射
QUEUE_TYPE_TO_DIR = {
    'session': 'failed_session_uploads',
    'prompt': 'failed_prompt_uploads',
    'prompt_update': 'failed_prompt_update_uploads',  # 更新操作使用独立目录
    'file_change': 'failed_file_change_uploads',
    'transcript': 'failed_transcript_uploads',
}


# ============================================================================
# 核心功能函数
# ============================================================================

def save_failed_upload(
    queue_type: QueueType,
    data: Dict[str, Any],
    error: str,
    api_endpoint: Optional[str] = None
) -> bool:
    """
    保存失败的上传记录（增强版）

    Args:
        queue_type: 队列类型（'session', 'prompt', 'prompt_update', 'file_change'）
        data: 原始上传数据
        error: 错误信息
        api_endpoint: API 端点（可选，默认从 queue_type 推断）

    Returns:
        bool: 保存成功返回 True，失败返回 False

    示例:
        # 创建操作
        save_failed_upload(
            queue_type='prompt',
            data=prompt_data,
            error='Connection timeout'
        )

        # 更新操作
        save_failed_upload(
            queue_type='prompt_update',
            data={'prompt_uuid': uuid, **update_data},
            error='500 Server Error'
        )
    """
    try:
        # 推断 API 端点
        if api_endpoint is None:
            api_endpoint = QUEUE_TYPE_TO_ENDPOINT.get(queue_type)
            if not api_endpoint:
                logger.error(f"未知的队列类型: {queue_type}")
                return False

        # 获取队列目录
        queue_dir_name = QUEUE_TYPE_TO_DIR.get(queue_type)
        if not queue_dir_name:
            logger.error(f"未知的队列类型: {queue_type}")
            return False

        queue_dir = get_data_dir(persistent=True) / queue_dir_name
        queue_dir.mkdir(parents=True, exist_ok=True)

        # 创建元数据
        now = datetime.utcnow()
        next_retry_time = calculate_next_retry_time(retry_count=0)

        metadata = RetryMetadata(
            queue_type=queue_type,
            api_endpoint=api_endpoint,
            created_at=now.isoformat() + 'Z',
            retry_count=0,
            last_retry_at=None,
            next_retry_at=next_retry_time.isoformat() + 'Z',
            error_history=[{
                'timestamp': now.isoformat() + 'Z',
                'error': error
            }]
        )

        # 构造完整记录
        failed_upload = FailedUpload(data=data, metadata=metadata)

        # 使用时间戳作为文件名，确保唯一性
        filename = f"{int(now.timestamp() * 1000)}.json"
        queue_file = queue_dir / filename

        # 保存到文件
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(failed_upload), f, ensure_ascii=False, indent=2)

        logger.info(f"已保存失败记录到队列 '{queue_type}': {queue_file}")
        return True

    except Exception as e:
        # 保存失败也不影响主流程
        logger.error(f"保存失败记录到队列 '{queue_type}' 时出错: {e}", exc_info=True)
        return False


def retry_failed_uploads(max_parallel: int = 3, verbose: bool = False) -> Dict[str, Any]:
    """
    扫描并重试所有失败的上传记录

    Args:
        max_parallel: 每次最多重试的记录数（避免阻塞）
        verbose: 是否显示详细进度信息到控制台（默认 False，适合 CLI 调用）

    Returns:
        Dict: 重试统计信息
        {
            'checked': 10,      # 检查的记录数
            'retried': 5,       # 尝试重试的记录数
            'succeeded': 3,     # 重试成功的记录数
            'failed': 2,        # 重试失败的记录数
            'skipped': 5        # 跳过的记录数（未到重试时间）
        }

    注意：
    - 非阻塞执行，快速返回
    - 每次最多重试 max_parallel 条记录
    - 适合在 Hook 中调用（verbose=False）或 CLI 手动调用（verbose=True）
    """
    config = get_retry_config()
    if not config['enabled']:
        logger.debug("重试功能已禁用（DEVLAKE_RETRY_ENABLED=false）")
        return {'checked': 0, 'retried': 0, 'succeeded': 0, 'failed': 0, 'skipped': 0}

    stats = {
        'checked': 0,
        'retried': 0,
        'succeeded': 0,
        'failed': 0,
        'skipped': 0,
    }

    try:
        now = datetime.utcnow()
        retry_count = 0

        # 遍历所有队列类型
        for queue_type in QUEUE_TYPE_TO_DIR.keys():
            queue_dir_name = QUEUE_TYPE_TO_DIR[queue_type]
            queue_dir = get_data_dir(persistent=True) / queue_dir_name

            if not queue_dir.exists():
                continue

            # 获取所有失败记录文件（按时间排序，优先处理旧的）
            failed_files = sorted(queue_dir.glob('*.json'), key=lambda f: f.stat().st_mtime)

            for failed_file in failed_files:
                # 限制单次重试数量（避免阻塞）
                if retry_count >= max_parallel:
                    logger.debug(f"已达到单次最大重试数量 {max_parallel}，跳过剩余记录")
                    if verbose:
                        print(f"\n⏸️  已达到单次最大重试数量 {max_parallel}，跳过剩余记录")
                    return stats

                stats['checked'] += 1

                try:
                    # 读取失败记录
                    with open(failed_file, 'r', encoding='utf-8') as f:
                        record = json.load(f)

                    data = record.get('data', {})
                    metadata_dict = record.get('metadata', {})

                    # 转换为数据类
                    metadata = RetryMetadata(**metadata_dict)

                    # 检查是否超过最大重试次数
                    if metadata.retry_count >= config['max_attempts']:
                        logger.debug(f"记录已达最大重试次数 {config['max_attempts']}，跳过: {failed_file}")
                        stats['skipped'] += 1
                        continue

                    # 检查是否到达重试时间（转换为 naive datetime 以便比较）
                    next_retry_time = datetime.fromisoformat(metadata.next_retry_at.replace('Z', '+00:00')).replace(tzinfo=None)
                    if now < next_retry_time:
                        logger.debug(f"未到重试时间（{metadata.next_retry_at}），跳过: {failed_file}")
                        stats['skipped'] += 1
                        continue

                    # 执行重试
                    logger.info(f"开始重试上传（第 {metadata.retry_count + 1} 次）: {failed_file}")
                    if verbose:
                        print(f"[{stats['checked']}/{stats['checked']}] 重试 {queue_type}（第 {metadata.retry_count + 1}/{config['max_attempts']} 次）...", end=' ', flush=True)

                    stats['retried'] += 1
                    retry_count += 1

                    success, error = _retry_upload(queue_type, data, metadata.api_endpoint)

                    if success:
                        # 重试成功，删除本地文件
                        failed_file.unlink()
                        logger.info(f"重试成功，已删除本地记录: {failed_file}")
                        stats['succeeded'] += 1
                        if verbose:
                            print("✅ 成功")
                    else:
                        # 重试失败，更新元数据
                        _update_retry_metadata(failed_file, metadata, error)
                        logger.warning(f"重试失败（第 {metadata.retry_count + 1} 次）: {error}")
                        stats['failed'] += 1
                        if verbose:
                            # 截断错误信息，避免输出过长
                            error_msg = error[:50] + '...' if len(error) > 50 else error
                            print(f"❌ 失败: {error_msg}")

                except Exception as e:
                    logger.error(f"处理失败记录时出错: {failed_file}, 错误: {e}", exc_info=True)
                    stats['failed'] += 1
                    if verbose:
                        print(f"❌ 处理出错: {str(e)[:50]}")

        if stats['retried'] > 0:
            logger.info(f"重试统计: {stats}")

        return stats

    except Exception as e:
        logger.error(f"重试失败上传时出错: {e}", exc_info=True)
        return stats


def cleanup_expired_failures(max_age_hours: Optional[int] = None) -> int:
    """
    清理过期的失败记录

    Args:
        max_age_hours: 最大保留时间（小时），默认从配置读取

    Returns:
        int: 清理的文件数量

    清理条件：
    1. 超过最大重试次数的记录
    2. 超过保留期限的记录（默认 7 天）
    """
    config = get_retry_config()
    if max_age_hours is None:
        max_age_hours = config['cleanup_days'] * 24

    cleaned_count = 0

    try:
        now = datetime.utcnow()
        max_age_seconds = max_age_hours * 3600

        # 遍历所有队列目录
        for queue_dir_name in QUEUE_TYPE_TO_DIR.values():
            queue_dir = get_data_dir(persistent=True) / queue_dir_name

            if not queue_dir.exists():
                continue

            for failed_file in queue_dir.glob('*.json'):
                try:
                    # 检查文件年龄
                    file_age_seconds = now.timestamp() - failed_file.stat().st_mtime

                    should_delete = False
                    delete_reasons = []

                    # 条件1: 文件过期
                    if file_age_seconds > max_age_seconds:
                        should_delete = True
                        delete_reasons.append(f"文件已过期（{file_age_seconds / 3600:.1f} 小时）")

                    # 条件2: 超过最大重试次数(独立检查)
                    try:
                        with open(failed_file, 'r', encoding='utf-8') as f:
                            record = json.load(f)
                        metadata_dict = record.get('metadata', {})
                        retry_count = metadata_dict.get('retry_count', 0)

                        if retry_count >= config['max_attempts']:
                            should_delete = True
                            delete_reasons.append(f"已达最大重试次数 {config['max_attempts']}")
                    except Exception:
                        # 无法读取的文件也删除
                        should_delete = True
                        delete_reasons.append("无法读取的文件")

                    if should_delete:
                        logger.debug(f"删除文件: {failed_file.name}, 原因: {', '.join(delete_reasons)}")
                        failed_file.unlink()
                        cleaned_count += 1

                except Exception as e:
                    logger.error(f"清理文件时出错: {failed_file}, 错误: {e}")

        if cleaned_count > 0:
            logger.info(f"已清理 {cleaned_count} 个过期的失败记录")

        return cleaned_count

    except Exception as e:
        logger.error(f"清理过期失败记录时出错: {e}", exc_info=True)
        return cleaned_count


def get_queue_statistics() -> Dict[str, Any]:
    """
    获取队列统计信息

    Returns:
        Dict: 统计信息
        {
            'session': {'total': 5, 'pending': 3, 'max_retried': 2},
            'prompt': {'total': 10, 'pending': 7, 'max_retried': 3},
            'file_change': {'total': 0, 'pending': 0, 'max_retried': 0},
            'summary': {'total': 15, 'pending': 10, 'max_retried': 5}
        }
    """
    config = get_retry_config()
    stats = {}
    summary = {'total': 0, 'pending': 0, 'max_retried': 0}

    try:
        for queue_type, queue_dir_name in QUEUE_TYPE_TO_DIR.items():
            queue_dir = get_data_dir(persistent=True) / queue_dir_name
            queue_stats = {'total': 0, 'pending': 0, 'max_retried': 0}

            if queue_dir.exists():
                for failed_file in queue_dir.glob('*.json'):
                    queue_stats['total'] += 1

                    try:
                        with open(failed_file, 'r', encoding='utf-8') as f:
                            record = json.load(f)
                        metadata_dict = record.get('metadata', {})
                        retry_count = metadata_dict.get('retry_count', 0)

                        if retry_count < config['max_attempts']:
                            queue_stats['pending'] += 1
                        else:
                            queue_stats['max_retried'] += 1
                    except Exception:
                        # 无法读取的文件计入 total
                        pass

            stats[queue_type] = queue_stats
            summary['total'] += queue_stats['total']
            summary['pending'] += queue_stats['pending']
            summary['max_retried'] += queue_stats['max_retried']

        stats['summary'] = summary
        return stats

    except Exception as e:
        logger.error(f"获取队列统计信息时出错: {e}", exc_info=True)
        return stats


# ============================================================================
# 辅助函数（私有）
# ============================================================================

def calculate_next_retry_time(retry_count: int) -> datetime:
    """
    计算下次重试时间（指数退避）

    Args:
        retry_count: 当前重试次数

    Returns:
        datetime: 下次重试时间

    退避策略：
        第1次：1分钟后
        第2次：5分钟后
        第3次：15分钟后
        第4次：60分钟后
        第5次：4小时后
    """
    if retry_count >= len(RETRY_BACKOFF_SCHEDULE):
        # 超过预定义次数，使用最后一个间隔
        backoff_seconds = RETRY_BACKOFF_SCHEDULE[-1]
    else:
        backoff_seconds = RETRY_BACKOFF_SCHEDULE[retry_count]

    return datetime.utcnow() + timedelta(seconds=backoff_seconds)


def _retry_upload(
    queue_type: str,
    data: Dict[str, Any],
    api_endpoint: str
) -> tuple[bool, Optional[str]]:
    """
    执行实际的重试上传

    Args:
        queue_type: 队列类型
        data: 上传数据
        api_endpoint: API 端点

    Returns:
        (success: bool, error: Optional[str])
    """
    try:
        client = DevLakeClient()

        # 根据队列类型调用不同的 API 方法
        if queue_type == 'session':
            # 智能判断：如果包含 session_end_time，说明是更新操作
            if 'session_end_time' in data:
                session_id = data.get('session_id')
                if not session_id:
                    return False, "session 更新缺少 session_id"
                client.update_session(session_id, data)
            else:
                # 否则是创建操作
                client.create_session(data)
        elif queue_type == 'prompt':
            client.create_prompt(data)
        elif queue_type == 'prompt_update':
            # 更新操作需要 prompt_uuid
            prompt_uuid = data.get('prompt_uuid')
            if not prompt_uuid:
                return False, "prompt_update 缺少 prompt_uuid"
            client.update_prompt(prompt_uuid, data)
        elif queue_type == 'file_change':
            # file_change 是批量接口，需要包装成 changes 数组
            if 'changes' not in data:
                data = {'changes': [data]}
            client.create_file_changes(data['changes'])
        elif queue_type == 'transcript':
            client.create_transcript(data)
        else:
            return False, f"未知的队列类型: {queue_type}"

        client.close()
        return True, None

    except Exception as e:
        error_msg = str(e)
        logger.error(f"重试上传失败: {error_msg}")
        return False, error_msg


def _update_retry_metadata(
    failed_file: Path,
    metadata: RetryMetadata,
    error: str
) -> None:
    """
    更新失败记录的重试元数据

    Args:
        failed_file: 失败记录文件路径
        metadata: 当前元数据
        error: 最新的错误信息
    """
    try:
        # 读取原始数据
        with open(failed_file, 'r', encoding='utf-8') as f:
            record = json.load(f)

        # 更新元数据
        now = datetime.utcnow()
        metadata.retry_count += 1
        metadata.last_retry_at = now.isoformat() + 'Z'
        metadata.next_retry_at = calculate_next_retry_time(metadata.retry_count).isoformat() + 'Z'
        metadata.error_history.append({
            'timestamp': now.isoformat() + 'Z',
            'error': error
        })

        # 保存更新后的记录
        record['metadata'] = asdict(metadata)
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"更新重试元数据失败: {failed_file}, 错误: {e}", exc_info=True)
