#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript Scanner 模块单元测试
"""

import json
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from devlake_mcp.transcript_scanner import (
    TranscriptMetadata,
    should_upload_transcript,
    scan_local_transcripts,
)


class TestTranscriptScanner:
    """Transcript Scanner 测试"""

    def test_should_upload_ended_session(self):
        """测试已结束会话应该上传"""
        metadata = TranscriptMetadata(
            file_path=Path('/tmp/test.jsonl'),
            session_id='session-ended',
            start_time=datetime.now(timezone.utc) - timedelta(hours=1),
            is_ended=True,
            should_upload=False,
            upload_source=None,
        )

        result = should_upload_transcript(metadata, zombie_hours=24)

        assert result is True
        assert metadata.should_upload is True
        assert metadata.upload_source == 'manual'

    def test_should_upload_zombie_session(self):
        """测试僵尸会话应该上传"""
        metadata = TranscriptMetadata(
            file_path=Path('/tmp/test.jsonl'),
            session_id='session-zombie',
            start_time=datetime.now(timezone.utc) - timedelta(hours=25),  # 超过 24 小时
            is_ended=False,
            should_upload=False,
            upload_source=None,
        )

        result = should_upload_transcript(metadata, zombie_hours=24)

        assert result is True
        assert metadata.should_upload is True
        assert metadata.upload_source == 'auto_backfill'

    def test_should_skip_ongoing_session(self):
        """测试正在进行中的会话应该跳过"""
        metadata = TranscriptMetadata(
            file_path=Path('/tmp/test.jsonl'),
            session_id='session-ongoing',
            start_time=datetime.now(timezone.utc) - timedelta(hours=1),  # 1 小时前
            is_ended=False,
            should_upload=False,
            upload_source=None,
        )

        result = should_upload_transcript(metadata, zombie_hours=24)

        assert result is False
        assert metadata.should_upload is False
        assert metadata.skip_reason is not None

    def test_should_skip_no_start_time(self):
        """测试无法获取开始时间的会话应该跳过"""
        metadata = TranscriptMetadata(
            file_path=Path('/tmp/test.jsonl'),
            session_id='session-no-time',
            start_time=None,
            is_ended=False,
            should_upload=False,
            upload_source=None,
        )

        result = should_upload_transcript(metadata, zombie_hours=24)

        assert result is False
        assert metadata.should_upload is False
        assert metadata.skip_reason == '无法获取开始时间'

    @patch('devlake_mcp.transcript_scanner.scan_claude_projects_dir')
    @patch('devlake_mcp.transcript_scanner.extract_session_id')
    @patch('devlake_mcp.transcript_scanner.get_session_start_time')
    @patch('devlake_mcp.transcript_scanner.is_session_ended')
    @patch('devlake_mcp.transcript_scanner.upload_single_transcript')
    def test_scan_local_transcripts_basic(
        self,
        mock_upload,
        mock_is_ended,
        mock_get_start_time,
        mock_extract_id,
        mock_scan_dir,
    ):
        """测试基本扫描流程"""
        # Mock 扫描目录返回 1 个文件
        test_file = Path('/tmp/test.jsonl')
        mock_scan_dir.return_value = [test_file]

        # Mock 元数据提取
        mock_extract_id.return_value = 'test-session-123'
        mock_get_start_time.return_value = datetime.now(timezone.utc) - timedelta(hours=1)
        mock_is_ended.return_value = True

        # Mock 上传成功
        mock_upload.return_value = True

        # Mock 缓存和客户端
        mock_cache = MagicMock()
        mock_cache.is_uploaded.return_value = False

        mock_client = MagicMock()

        # 执行扫描
        report = scan_local_transcripts(
            cache=mock_cache,
            client=mock_client,
            check_server=False,
            force=False,
            dry_run=False,
        )

        # 验证结果
        assert report.total_scanned == 1
        assert report.uploaded_success == 1
        assert report.uploaded_failed == 0

        # 验证缓存被调用
        mock_cache.is_uploaded.assert_called_once_with('test-session-123')

    @patch('devlake_mcp.transcript_scanner.scan_claude_projects_dir')
    @patch('devlake_mcp.transcript_scanner.extract_session_id')
    def test_scan_local_transcripts_cached(
        self,
        mock_extract_id,
        mock_scan_dir,
    ):
        """测试缓存命中跳过"""
        # Mock 扫描目录返回 1 个文件
        test_file = Path('/tmp/test.jsonl')
        mock_scan_dir.return_value = [test_file]

        # Mock session_id 提取
        mock_extract_id.return_value = 'cached-session'

        # Mock 缓存（已存在）
        mock_cache = MagicMock()
        mock_cache.is_uploaded.return_value = True

        mock_client = MagicMock()

        # 执行扫描
        report = scan_local_transcripts(
            cache=mock_cache,
            client=mock_client,
            check_server=False,
            force=False,
            dry_run=False,
        )

        # 验证结果
        assert report.total_scanned == 1
        assert report.skipped_cached == 1
        assert report.uploaded_success == 0

    @patch('devlake_mcp.transcript_scanner.scan_claude_projects_dir')
    @patch('devlake_mcp.transcript_scanner.extract_session_id')
    @patch('devlake_mcp.transcript_scanner.get_session_start_time')
    @patch('devlake_mcp.transcript_scanner.is_session_ended')
    def test_scan_local_transcripts_ongoing(
        self,
        mock_is_ended,
        mock_get_start_time,
        mock_extract_id,
        mock_scan_dir,
    ):
        """测试正在进行中的会话被跳过"""
        # Mock 扫描目录
        test_file = Path('/tmp/test.jsonl')
        mock_scan_dir.return_value = [test_file]

        # Mock 元数据（未结束，1小时前）
        mock_extract_id.return_value = 'ongoing-session'
        mock_get_start_time.return_value = datetime.now(timezone.utc) - timedelta(hours=1)
        mock_is_ended.return_value = False

        # Mock 缓存
        mock_cache = MagicMock()
        mock_cache.is_uploaded.return_value = False

        mock_client = MagicMock()

        # 执行扫描
        report = scan_local_transcripts(
            cache=mock_cache,
            client=mock_client,
            check_server=False,
            force=False,
            dry_run=False,
        )

        # 验证结果
        assert report.total_scanned == 1
        assert report.skipped_ongoing == 1
        assert report.uploaded_success == 0

    @patch('devlake_mcp.transcript_scanner.scan_claude_projects_dir')
    def test_scan_local_transcripts_no_files(self, mock_scan_dir):
        """测试没有文件的情况"""
        # Mock 扫描目录返回空列表
        mock_scan_dir.return_value = []

        mock_cache = MagicMock()
        mock_client = MagicMock()

        # 执行扫描
        report = scan_local_transcripts(
            cache=mock_cache,
            client=mock_client,
            check_server=False,
            force=False,
            dry_run=False,
        )

        # 验证结果
        assert report.total_scanned == 0
        assert report.uploaded_success == 0

    @patch('devlake_mcp.transcript_scanner.scan_claude_projects_dir')
    @patch('devlake_mcp.transcript_scanner.extract_session_id')
    def test_scan_local_transcripts_extraction_error(
        self,
        mock_extract_id,
        mock_scan_dir,
    ):
        """测试提取 session_id 失败的情况"""
        # Mock 扫描目录
        test_file = Path('/tmp/test.jsonl')
        mock_scan_dir.return_value = [test_file]

        # Mock session_id 提取失败
        mock_extract_id.return_value = None

        mock_cache = MagicMock()
        mock_client = MagicMock()

        # 执行扫描
        report = scan_local_transcripts(
            cache=mock_cache,
            client=mock_client,
            check_server=False,
            force=False,
            dry_run=False,
        )

        # 验证结果
        assert report.total_scanned == 1
        assert report.skipped_error == 1
        assert report.uploaded_success == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
