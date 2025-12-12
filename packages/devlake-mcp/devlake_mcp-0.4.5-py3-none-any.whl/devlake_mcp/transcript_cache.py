#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript 上传缓存管理

维护本地已上传 transcript 的记录，避免重复检查和上传。
缓存格式：
{
    "version": "1.0",
    "cache": {
        "sess-abc123": {
            "uploaded_at": "2025-11-19T10:00:00+08:00"
        }
    },
    "last_cleanup": "2025-11-19T00:00:00+08:00"
}
"""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Optional

from devlake_mcp.constants import (
    TRANSCRIPT_CACHE_DIR_NAME,
    TRANSCRIPT_CACHE_FILE_NAME,
    get_transcript_cache_retention_days,
)

logger = logging.getLogger(__name__)


class TranscriptCache:
    """Transcript 上传缓存管理器"""

    CACHE_VERSION = "1.0"

    def __init__(self, cache_path: Optional[Path] = None):
        """
        初始化缓存管理器

        Args:
            cache_path: 缓存文件路径，默认为 ~/.devlake/transcript_cache.json
        """
        if cache_path is None:
            cache_dir = Path.home() / TRANSCRIPT_CACHE_DIR_NAME
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_path = cache_dir / TRANSCRIPT_CACHE_FILE_NAME

        self.cache_path = cache_path
        self._cache_data: Optional[Dict] = None

    def _load_cache(self) -> Dict:
        """
        从文件加载缓存数据

        Returns:
            缓存数据字典
        """
        if self._cache_data is not None:
            return self._cache_data

        if not self.cache_path.exists():
            logger.debug(f"缓存文件不存在，创建新缓存: {self.cache_path}")
            self._cache_data = {
                "version": self.CACHE_VERSION,
                "cache": {},
                "last_cleanup": datetime.now(timezone.utc).isoformat(),
            }
            return self._cache_data

        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 版本检查
            if data.get('version') != self.CACHE_VERSION:
                logger.warning(
                    f"缓存版本不匹配 (期望: {self.CACHE_VERSION}, 实际: {data.get('version')}), 重建缓存"
                )
                self._cache_data = {
                    "version": self.CACHE_VERSION,
                    "cache": {},
                    "last_cleanup": datetime.now(timezone.utc).isoformat(),
                }
            else:
                self._cache_data = data

            return self._cache_data

        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"读取缓存文件失败: {e}, 重建缓存")
            self._cache_data = {
                "version": self.CACHE_VERSION,
                "cache": {},
                "last_cleanup": datetime.now(timezone.utc).isoformat(),
            }
            return self._cache_data

    def _save_cache(self) -> None:
        """保存缓存数据到文件"""
        try:
            # 确保目录存在
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)

            # 写入文件（使用临时文件 + 原子替换，防止写入中断导致文件损坏）
            temp_path = self.cache_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(self._cache_data, f, ensure_ascii=False, indent=2)

            # 原子替换
            temp_path.replace(self.cache_path)

            logger.debug(f"缓存已保存: {self.cache_path}")

        except IOError as e:
            logger.error(f"保存缓存文件失败: {e}")

    def is_uploaded(self, session_id: str) -> bool:
        """
        检查 session_id 是否已在缓存中（即已上传）

        Args:
            session_id: 会话 ID

        Returns:
            True 表示已上传，False 表示未上传
        """
        cache = self._load_cache()
        return session_id in cache.get('cache', {})

    def add(self, session_id: str, uploaded_at: Optional[str] = None) -> None:
        """
        添加 session_id 到缓存（标记为已上传）

        Args:
            session_id: 会话 ID
            uploaded_at: 上传时间（ISO 8601 格式），默认为当前时间
        """
        cache = self._load_cache()

        if uploaded_at is None:
            uploaded_at = datetime.now(timezone.utc).isoformat()

        cache['cache'][session_id] = {
            'uploaded_at': uploaded_at
        }

        self._save_cache()
        logger.debug(f"缓存已添加: {session_id} @ {uploaded_at}")

    def remove(self, session_id: str) -> bool:
        """
        从缓存中移除 session_id

        Args:
            session_id: 会话 ID

        Returns:
            True 表示成功移除，False 表示不存在
        """
        cache = self._load_cache()

        if session_id not in cache.get('cache', {}):
            return False

        del cache['cache'][session_id]
        self._save_cache()
        logger.debug(f"缓存已移除: {session_id}")
        return True

    def cleanup_old_entries(self, days: Optional[int] = None) -> int:
        """
        清理过期的缓存记录

        Args:
            days: 保留天数，默认从配置读取（30 天）

        Returns:
            清理的记录数量
        """
        if days is None:
            days = get_transcript_cache_retention_days()

        cache = self._load_cache()
        cache_entries = cache.get('cache', {})

        if not cache_entries:
            logger.debug("缓存为空，无需清理")
            return 0

        # 计算截止时间
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
        removed_count = 0

        # 遍历缓存，删除过期记录
        session_ids_to_remove = []
        for session_id, entry in cache_entries.items():
            uploaded_at_str = entry.get('uploaded_at')
            if not uploaded_at_str:
                # 没有上传时间，保留
                continue

            try:
                uploaded_at = datetime.fromisoformat(uploaded_at_str)
                if uploaded_at < cutoff_time:
                    session_ids_to_remove.append(session_id)
            except (ValueError, TypeError) as e:
                logger.warning(f"解析上传时间失败: {session_id} - {e}")
                # 解析失败，保留

        # 删除过期记录
        for session_id in session_ids_to_remove:
            del cache['cache'][session_id]
            removed_count += 1

        if removed_count > 0:
            cache['last_cleanup'] = datetime.now(timezone.utc).isoformat()
            self._save_cache()
            logger.info(f"清理了 {removed_count} 条过期缓存记录（保留 {days} 天）")
        else:
            logger.debug("没有过期的缓存记录")

        return removed_count

    def get_stats(self) -> Dict:
        """
        获取缓存统计信息

        Returns:
            统计信息字典，包含：
            - total_count: 总记录数
            - oldest_entry: 最老的记录（session_id 和上传时间）
            - newest_entry: 最新的记录（session_id 和上传时间）
            - last_cleanup: 上次清理时间
        """
        cache = self._load_cache()
        cache_entries = cache.get('cache', {})

        stats = {
            'total_count': len(cache_entries),
            'oldest_entry': None,
            'newest_entry': None,
            'last_cleanup': cache.get('last_cleanup'),
        }

        if not cache_entries:
            return stats

        # 找出最老和最新的记录
        oldest_session_id = None
        oldest_time = None
        newest_session_id = None
        newest_time = None

        for session_id, entry in cache_entries.items():
            uploaded_at_str = entry.get('uploaded_at')
            if not uploaded_at_str:
                continue

            try:
                uploaded_at = datetime.fromisoformat(uploaded_at_str)

                if oldest_time is None or uploaded_at < oldest_time:
                    oldest_time = uploaded_at
                    oldest_session_id = session_id

                if newest_time is None or uploaded_at > newest_time:
                    newest_time = uploaded_at
                    newest_session_id = session_id

            except (ValueError, TypeError):
                continue

        if oldest_session_id:
            stats['oldest_entry'] = {
                'session_id': oldest_session_id,
                'uploaded_at': oldest_time.isoformat(),
            }

        if newest_session_id:
            stats['newest_entry'] = {
                'session_id': newest_session_id,
                'uploaded_at': newest_time.isoformat(),
            }

        return stats

    def clear(self) -> int:
        """
        清空所有缓存

        Returns:
            清空的记录数量
        """
        cache = self._load_cache()
        count = len(cache.get('cache', {}))

        cache['cache'] = {}
        cache['last_cleanup'] = datetime.now(timezone.utc).isoformat()
        self._save_cache()

        logger.info(f"已清空所有缓存（共 {count} 条记录）")
        return count
