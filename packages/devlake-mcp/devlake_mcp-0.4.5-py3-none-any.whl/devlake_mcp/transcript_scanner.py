#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcript 扫描和上传模块

扫描本地所有 Claude Code 对话历史，上传服务端缺失的 transcript。
"""

import glob
import logging
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Optional

from devlake_mcp.client import DevLakeClient, DevLakeNotFoundError
from devlake_mcp.constants import (
    CLAUDE_PROJECTS_DIR_PATTERN,
    EXCLUDED_TRANSCRIPT_PREFIX,
    UPLOAD_SOURCE_AUTO_BACKFILL,
    UPLOAD_SOURCE_MANUAL,
    get_zombie_session_hours,
)
from devlake_mcp.hooks.transcript_utils import (
    compress_transcript_content,
    count_user_messages,
    extract_session_id,
    get_session_start_time,
    is_session_ended,
    read_transcript_content,
)
from devlake_mcp.retry_queue import save_failed_upload
from devlake_mcp.transcript_cache import TranscriptCache
from devlake_mcp.git_utils import get_git_info
import os

logger = logging.getLogger(__name__)


@dataclass
class TranscriptMetadata:
    """Transcript 元数据"""

    file_path: Path
    session_id: str
    start_time: Optional[datetime]
    is_ended: bool
    should_upload: bool
    upload_source: Optional[str]
    skip_reason: Optional[str] = None


@dataclass
class SyncReport:
    """同步报告"""

    total_scanned: int = 0  # 扫描的文件总数
    skipped_excluded: int = 0  # 跳过（文件名被排除）
    skipped_cached: int = 0  # 跳过（缓存命中）
    skipped_ongoing: int = 0  # 跳过（正在进行中的会话）
    skipped_server_exists: int = 0  # 跳过（服务端已存在）
    skipped_error: int = 0  # 跳过（解析错误）
    uploaded_success: int = 0  # 上传成功
    uploaded_failed: int = 0  # 上传失败

    def get_summary(self) -> str:
        """获取摘要文本"""
        return f"""
📊 同步统计:
  • 扫描文件: {self.total_scanned} 个
  • 跳过排除: {self.skipped_excluded} 个
  • 跳过缓存: {self.skipped_cached} 个
  • 跳过进行中: {self.skipped_ongoing} 个
  • 跳过已存在: {self.skipped_server_exists} 个
  • 跳过错误: {self.skipped_error} 个
  ✅ 上传成功: {self.uploaded_success} 个
  ❌ 上传失败: {self.uploaded_failed} 个
"""


def scan_claude_projects_dir() -> List[Path]:
    """
    扫描 Claude Code projects 目录下的所有 jsonl 文件

    扫描路径：~/.claude/projects* （包含所有子目录）
    排除规则：文件名以 'agent-' 开头的文件

    Returns:
        所有符合条件的 jsonl 文件路径列表
    """
    logger.info("开始扫描 Claude Code projects 目录...")

    # 展开路径模式
    pattern_path = Path(CLAUDE_PROJECTS_DIR_PATTERN.replace('~', str(Path.home())))
    base_pattern = str(pattern_path)

    # 查找所有匹配的目录
    matching_dirs = glob.glob(base_pattern)

    if not matching_dirs:
        logger.warning(f"未找到匹配的目录: {base_pattern}")
        return []

    logger.debug(f"找到 {len(matching_dirs)} 个 projects 目录")

    # 扫描所有目录下的 jsonl 文件
    jsonl_files = []
    for project_dir in matching_dirs:
        # 递归查找所有 .jsonl 文件
        pattern = str(Path(project_dir) / '**' / '*.jsonl')
        files = glob.glob(pattern, recursive=True)

        for file_path in files:
            file_name = Path(file_path).name

            # 排除 agent-*.jsonl
            if file_name.startswith(EXCLUDED_TRANSCRIPT_PREFIX):
                logger.debug(f"排除文件: {file_name}")
                continue

            jsonl_files.append(Path(file_path))

    logger.info(f"扫描完成，找到 {len(jsonl_files)} 个 transcript 文件")
    return jsonl_files


def should_upload_transcript(metadata: TranscriptMetadata, zombie_hours: int) -> bool:
    """
    判断是否应该上传 transcript

    过滤规则：
    1. 会话已结束 → 上传
    2. 会话未结束 + 开始时间 > zombie_hours → 上传（僵尸会话）
    3. 会话未结束 + 开始时间 ≤ zombie_hours → 跳过

    Args:
        metadata: Transcript 元数据
        zombie_hours: 僵尸会话阈值（小时）

    Returns:
        True 表示应该上传，False 表示跳过
    """
    # 规则 1: 会话已结束
    if metadata.is_ended:
        metadata.should_upload = True
        metadata.upload_source = UPLOAD_SOURCE_MANUAL
        logger.debug(f"会话已结束，应该上传: {metadata.session_id}")
        return True

    # 规则 2 & 3: 会话未结束，检查是否是僵尸会话
    if metadata.start_time is None:
        logger.warning(f"无法获取会话开始时间，跳过: {metadata.session_id}")
        metadata.should_upload = False
        metadata.skip_reason = "无法获取开始时间"
        return False

    # 计算会话已持续时间
    now = datetime.now(timezone.utc)
    elapsed_hours = (now - metadata.start_time).total_seconds() / 3600

    if elapsed_hours > zombie_hours:
        # 僵尸会话
        metadata.should_upload = True
        metadata.upload_source = UPLOAD_SOURCE_AUTO_BACKFILL
        logger.debug(
            f"僵尸会话（已持续 {elapsed_hours:.1f} 小时），应该上传: {metadata.session_id}"
        )
        return True
    else:
        # 正在进行中
        metadata.should_upload = False
        metadata.skip_reason = f"正在进行中（已持续 {elapsed_hours:.1f} 小时）"
        logger.debug(f"会话正在进行中，跳过: {metadata.session_id}")
        return False


def upload_single_transcript(
    file_path: Path,
    session_id: str,
    upload_source: str,
    client: DevLakeClient,
    cache: TranscriptCache,
) -> bool:
    """
    上传单个 transcript

    Args:
        file_path: Transcript 文件路径
        session_id: 会话 ID
        upload_source: 上传来源（auto/auto_backfill/manual）
        client: API 客户端
        cache: 缓存管理器

    Returns:
        True 表示上传成功，False 表示失败
    """
    try:
        logger.info(f"开始上传 transcript: {session_id}")

        # 1. 读取 transcript 内容
        transcript_content = read_transcript_content(str(file_path))
        if not transcript_content:
            logger.error(f"读取 transcript 内容失败: {file_path}")
            return False

        # 2. 压缩内容
        compression_result = compress_transcript_content(transcript_content)

        # 3. 统计消息数量
        message_count = count_user_messages(str(file_path))

        # 4. 获取 git 用户信息
        cwd = os.getcwd()
        git_info = get_git_info(cwd, include_user_info=True)
        git_author = git_info.get('git_author')
        git_email = git_info.get('git_email')
        # 如果获取失败或为 'unknown',则设为 None
        if git_author == 'unknown':
            git_author = None
        if git_email == 'unknown':
            git_email = None

        # 5. 构建上传数据
        upload_data = {
            'session_id': session_id,
            'transcript_path': str(file_path),
            'transcript_content': compression_result['content'],
            'compression': compression_result['compression'],
            'original_size': compression_result['original_size'],
            'compressed_size': compression_result['compressed_size'],
            'compression_ratio': compression_result['compression_ratio'],
            'message_count': message_count,
            'upload_time': datetime.now().isoformat(),
            'upload_source': upload_source,
            'git_author': git_author,
            'git_email': git_email,
        }

        # 5. 调用 API 上传
        response = client.create_transcript(upload_data)

        if response.get('success'):
            logger.info(f"上传成功: {session_id}")
            # 添加到缓存
            cache.add(session_id)
            return True
        else:
            error_msg = response.get('message', '未知错误')
            logger.error(f"上传失败: {session_id} - {error_msg}")
            # 保存到重试队列
            save_failed_upload(
                queue_type='transcript',
                api_endpoint='/api/ai-coding/transcripts',
                data=upload_data,
                error=error_msg,
            )
            return False

    except Exception as e:
        logger.error(f"上传 transcript 异常: {session_id} - {e}", exc_info=True)
        # 保存到重试队列
        save_failed_upload(
            queue_type='transcript',
            api_endpoint='/api/ai-coding/transcripts',
            data={
                'session_id': session_id,
                'transcript_path': str(file_path),
                'upload_source': upload_source,
            },
            error=str(e),
        )
        return False


def scan_local_transcripts(
    cache: TranscriptCache,
    client: DevLakeClient,
    check_server: bool = False,
    force: bool = False,
    session_id_filter: Optional[str] = None,
    dry_run: bool = False,
) -> SyncReport:
    """
    扫描并上传本地 transcript

    Args:
        cache: 缓存实例
        client: API 客户端
        check_server: 是否向服务端检查（False 时只依赖缓存）
        force: 强制上传，忽略缓存
        session_id_filter: 只处理特定 session_id
        dry_run: 预览模式，只扫描不上传

    Returns:
        同步报告
    """
    report = SyncReport()
    zombie_hours = get_zombie_session_hours()

    logger.info("=" * 60)
    logger.info("开始扫描本地 transcript 文件")
    logger.info(f"配置: check_server={check_server}, force={force}, dry_run={dry_run}")
    logger.info(f"僵尸会话阈值: {zombie_hours} 小时")
    logger.info("=" * 60)

    # 1. 扫描文件
    jsonl_files = scan_claude_projects_dir()
    report.total_scanned = len(jsonl_files)

    if report.total_scanned == 0:
        logger.info("未找到任何 transcript 文件")
        return report

    # 2. 遍历文件，提取元数据并过滤
    total_files = len(jsonl_files)
    for idx, file_path in enumerate(jsonl_files, start=1):
        try:
            # 显示整体进度
            print(f"📄 处理中 ({idx}/{total_files}): {file_path.name}")

            # 2.1 提取 session_id
            session_id = extract_session_id(str(file_path))
            if not session_id:
                logger.warning(f"无法提取 session_id，跳过: {file_path}")
                print(f"   ⚠️  无法提取 session_id，已跳过")
                report.skipped_error += 1
                continue

            # 2.2 会话过滤
            if session_id_filter and session_id != session_id_filter:
                continue

            # 2.3 检查缓存（除非 force）
            if not force and cache.is_uploaded(session_id):
                logger.debug(f"缓存命中，跳过: {session_id}")
                print(f"   ⏭️  缓存命中，已跳过")
                report.skipped_cached += 1
                continue

            # 2.4 提取元数据
            start_time = get_session_start_time(str(file_path))
            is_ended = is_session_ended(str(file_path))

            metadata = TranscriptMetadata(
                file_path=file_path,
                session_id=session_id,
                start_time=start_time,
                is_ended=is_ended,
                should_upload=False,
                upload_source=None,
            )

            # 2.5 应用过滤规则
            if not should_upload_transcript(metadata, zombie_hours):
                if metadata.skip_reason:
                    logger.debug(f"跳过: {session_id} - {metadata.skip_reason}")
                    print(f"   ⏭️  {metadata.skip_reason}")
                report.skipped_ongoing += 1
                continue

            # 2.6 检查服务端是否存在（如果启用）
            if check_server:
                print(f"   🌐 正在检查服务端: {session_id[:8]}...")
                try:
                    exists = client.check_transcript_exists(session_id)
                    if exists:
                        logger.info(f"服务端已存在，跳过: {session_id}")
                        print(f"   ✅ 服务端已存在，已跳过")
                        report.skipped_server_exists += 1
                        # 添加到缓存（避免下次再检查）
                        cache.add(session_id)
                        continue
                    else:
                        print(f"   📤 服务端不存在，准备上传")
                except Exception as e:
                    logger.warning(f"检查服务端失败: {session_id} - {e}")
                    print(f"   ⚠️  检查服务端失败: {e}，继续上传")
                    # 继续执行上传

            # 2.7 上传 transcript
            if dry_run:
                logger.info(f"[DRY RUN] 将上传: {session_id} ({metadata.upload_source})")
                print(f"   🔍 [预览] 将上传 ({metadata.upload_source})")
                report.uploaded_success += 1
            else:
                print(f"   📤 开始上传: {session_id[:8]}...")
                success = upload_single_transcript(
                    file_path=file_path,
                    session_id=session_id,
                    upload_source=metadata.upload_source,
                    client=client,
                    cache=cache,
                )

                if success:
                    print(f"   ✅ 上传成功")
                    report.uploaded_success += 1
                else:
                    print(f"   ❌ 上传失败")
                    report.uploaded_failed += 1

        except Exception as e:
            logger.error(f"处理文件失败: {file_path} - {e}", exc_info=True)
            print(f"   ❌ 处理失败: {e}")
            report.skipped_error += 1

    logger.info("=" * 60)
    logger.info("扫描完成")
    logger.info(report.get_summary())
    logger.info("=" * 60)

    return report
