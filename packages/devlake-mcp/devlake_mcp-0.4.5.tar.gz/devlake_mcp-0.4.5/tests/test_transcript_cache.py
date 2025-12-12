#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript Cache 模块单元测试
"""

import json
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from devlake_mcp.transcript_cache import TranscriptCache


class TestTranscriptCache:
    """TranscriptCache 类测试"""

    def test_init_creates_cache_file(self):
        """测试初始化创建缓存文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'
            cache = TranscriptCache(cache_path=cache_path)

            # 添加一条记录会触发保存（创建文件）
            cache.add('test-session')

            assert cache_path.exists()

    def test_add_and_is_uploaded(self):
        """测试添加和查询缓存"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'
            cache = TranscriptCache(cache_path=cache_path)

            session_id = 'test-session-123'

            # 初始状态：不存在
            assert not cache.is_uploaded(session_id)

            # 添加到缓存
            cache.add(session_id)

            # 再次查询：存在
            assert cache.is_uploaded(session_id)

    def test_remove(self):
        """测试移除缓存"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'
            cache = TranscriptCache(cache_path=cache_path)

            session_id = 'test-session-456'

            # 添加
            cache.add(session_id)
            assert cache.is_uploaded(session_id)

            # 移除
            result = cache.remove(session_id)
            assert result is True
            assert not cache.is_uploaded(session_id)

            # 再次移除（不存在）
            result = cache.remove(session_id)
            assert result is False

    def test_cleanup_old_entries(self):
        """测试清理过期缓存"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'
            cache = TranscriptCache(cache_path=cache_path)

            # 添加新记录
            cache.add('session-new')

            # 添加旧记录（手动修改时间戳）
            old_time = (datetime.now(timezone.utc) - timedelta(days=35)).isoformat()
            cache.add('session-old', uploaded_at=old_time)

            # 确认两个记录都存在
            assert cache.is_uploaded('session-new')
            assert cache.is_uploaded('session-old')

            # 清理 30 天前的记录
            removed_count = cache.cleanup_old_entries(days=30)

            # 应该清理了 1 条记录
            assert removed_count == 1
            assert cache.is_uploaded('session-new')
            assert not cache.is_uploaded('session-old')

    def test_get_stats(self):
        """测试获取统计信息"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'
            cache = TranscriptCache(cache_path=cache_path)

            # 空缓存
            stats = cache.get_stats()
            assert stats['total_count'] == 0
            assert stats['oldest_entry'] is None
            assert stats['newest_entry'] is None

            # 添加记录
            cache.add('session-1')
            cache.add('session-2')

            stats = cache.get_stats()
            assert stats['total_count'] == 2
            assert stats['oldest_entry'] is not None
            assert stats['newest_entry'] is not None

    def test_clear(self):
        """测试清空缓存"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'
            cache = TranscriptCache(cache_path=cache_path)

            # 添加多条记录
            cache.add('session-1')
            cache.add('session-2')
            cache.add('session-3')

            # 确认记录存在
            assert cache.is_uploaded('session-1')
            assert cache.is_uploaded('session-2')
            assert cache.is_uploaded('session-3')

            # 清空
            count = cache.clear()
            assert count == 3

            # 确认已清空
            assert not cache.is_uploaded('session-1')
            assert not cache.is_uploaded('session-2')
            assert not cache.is_uploaded('session-3')

    def test_cache_persistence(self):
        """测试缓存持久化"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'

            # 第一次创建缓存并添加记录
            cache1 = TranscriptCache(cache_path=cache_path)
            cache1.add('session-persistent')

            # 第二次加载缓存
            cache2 = TranscriptCache(cache_path=cache_path)

            # 应该能读取到之前的记录
            assert cache2.is_uploaded('session-persistent')

    def test_corrupted_cache_file(self):
        """测试损坏的缓存文件处理"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'

            # 写入无效的 JSON
            with open(cache_path, 'w') as f:
                f.write('{ invalid json }')

            # 应该能正常创建缓存（重建）
            cache = TranscriptCache(cache_path=cache_path)
            cache._load_cache()

            # 缓存应该为空
            stats = cache.get_stats()
            assert stats['total_count'] == 0

    def test_version_mismatch(self):
        """测试版本不匹配的处理"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / 'test_cache.json'

            # 写入旧版本的缓存
            old_cache_data = {
                'version': '0.0',  # 错误的版本
                'cache': {
                    'session-old': {
                        'uploaded_at': datetime.now(timezone.utc).isoformat()
                    }
                },
                'last_cleanup': datetime.now(timezone.utc).isoformat(),
            }

            with open(cache_path, 'w') as f:
                json.dump(old_cache_data, f)

            # 加载缓存
            cache = TranscriptCache(cache_path=cache_path)
            cache._load_cache()

            # 应该重建缓存（旧数据丢失）
            assert not cache.is_uploaded('session-old')
            stats = cache.get_stats()
            assert stats['total_count'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
