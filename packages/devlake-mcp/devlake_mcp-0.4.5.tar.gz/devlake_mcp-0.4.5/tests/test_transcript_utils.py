#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript Utils 模块单元测试
"""

import json
import tempfile
from pathlib import Path

import pytest

from devlake_mcp.hooks.transcript_utils import (
    extract_session_id,
    _extract_session_id_from_filename,
)


class TestExtractSessionId:
    """extract_session_id 函数测试"""

    def test_extract_from_sessionid_field(self):
        """测试从消息的 sessionId 字段提取"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # 写入包含 sessionId 字段的消息
            message = {
                'type': 'user',
                'uuid': 'msg-uuid-123',
                'sessionId': 'session-uuid-456',
                'timestamp': '2025-01-19T10:00:00Z',
                'content': 'test message'
            }
            f.write(json.dumps(message) + '\n')
            temp_path = f.name

        try:
            session_id = extract_session_id(temp_path)
            assert session_id == 'session-uuid-456'
        finally:
            Path(temp_path).unlink()

    def test_extract_from_filename_uuid(self):
        """测试从 UUID 格式的文件名提取"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建正确的 UUID 格式文件名
            test_path = Path(tmpdir) / '357874b4-0982-4d0c-b9b7-7ad2a97a3c50.jsonl'
            with open(test_path, 'w') as f:
                # 写入空消息（没有 sessionId 字段）
                f.write(json.dumps({'type': 'user'}) + '\n')

            session_id = extract_session_id(str(test_path))
            # 从文件名提取 UUID
            assert session_id == '357874b4-0982-4d0c-b9b7-7ad2a97a3c50'
            assert len(session_id) == 36  # UUID 标准长度

    def test_extract_from_filename_agent(self):
        """测试从 agent 格式的文件名提取"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建 agent-xxx.jsonl 格式的文件
            test_path = Path(tmpdir) / 'agent-da9ab721.jsonl'
            with open(test_path, 'w') as f:
                f.write(json.dumps({'type': 'user'}) + '\n')

            session_id = extract_session_id(str(test_path))
            assert session_id == 'agent-da9ab721'

    def test_extract_empty_file(self):
        """测试空文件的情况"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建正确的 UUID 格式文件名
            test_path = Path(tmpdir) / '357874b4-0982-4d0c-b9b7-7ad2a97a3c50.jsonl'
            # 创建空文件
            test_path.touch()

            session_id = extract_session_id(str(test_path))
            # 应该从文件名提取
            assert session_id == '357874b4-0982-4d0c-b9b7-7ad2a97a3c50'

    def test_extract_invalid_json(self):
        """测试无效 JSON 的情况"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建正确的 UUID 格式文件名
            test_path = Path(tmpdir) / '357874b4-0982-4d0c-b9b7-7ad2a97a3c50.jsonl'
            with open(test_path, 'w') as f:
                f.write('{ invalid json }\n')

            session_id = extract_session_id(str(test_path))
            # 应该从文件名提取（因为 JSON 解析失败）
            assert session_id == '357874b4-0982-4d0c-b9b7-7ad2a97a3c50'


class TestExtractSessionIdFromFilename:
    """_extract_session_id_from_filename 函数测试"""

    def test_uuid_format(self):
        """测试 UUID 格式文件名"""
        test_cases = [
            '/path/to/357874b4-0982-4d0c-b9b7-7ad2a97a3c50.jsonl',
            '/path/to/6526e452-864f-4358-a3d2-6afbd14b70ea.jsonl',
            'c125c548-43e7-4de4-9180-4aaef2731090.jsonl',
        ]

        for path in test_cases:
            session_id = _extract_session_id_from_filename(path)
            assert session_id is not None
            assert len(session_id) == 36
            # 验证 UUID 格式
            parts = session_id.split('-')
            assert len(parts) == 5
            assert len(parts[0]) == 8
            assert len(parts[1]) == 4
            assert len(parts[2]) == 4
            assert len(parts[3]) == 4
            assert len(parts[4]) == 12

    def test_agent_format(self):
        """测试 agent 格式文件名"""
        test_cases = [
            '/path/to/agent-da9ab721.jsonl',
            '/path/to/agent-b171785b.jsonl',
            'agent-23127ab7.jsonl',
        ]

        for path in test_cases:
            session_id = _extract_session_id_from_filename(path)
            assert session_id is not None
            assert session_id.startswith('agent-')

    def test_invalid_format(self):
        """测试无效格式文件名"""
        test_cases = [
            '/path/to/invalid-filename.jsonl',
            '/path/to/not-a-uuid.jsonl',
            'random.jsonl',
        ]

        for path in test_cases:
            session_id = _extract_session_id_from_filename(path)
            assert session_id is None

    def test_case_insensitive_uuid(self):
        """测试 UUID 大小写不敏感"""
        test_cases = [
            '357874B4-0982-4D0C-B9B7-7AD2A97A3C50.jsonl',  # 大写
            '357874b4-0982-4d0c-b9b7-7ad2a97a3c50.jsonl',  # 小写
            '357874B4-0982-4d0c-B9b7-7aD2a97a3C50.jsonl',  # 混合
        ]

        for path in test_cases:
            session_id = _extract_session_id_from_filename(path)
            assert session_id is not None
            assert len(session_id) == 36


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
