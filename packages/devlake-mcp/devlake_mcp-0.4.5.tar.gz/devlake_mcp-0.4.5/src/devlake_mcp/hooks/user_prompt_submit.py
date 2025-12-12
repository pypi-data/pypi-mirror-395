#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户提示词提交时记录会话信息（UserPromptSubmit Hook）

触发时机: 用户点击发送按钮后、发起后端请求之前

Claude Code 输入格式:
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../xxx.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}

功能:
1. 调用 session_manager.start_new_session() 确保会话存在
   - 直接调用 API 创建会话，后端通过幂等性处理重复请求
2. 上传用户的 prompt 内容（记录用户输入）
3. 静默退出，不阻塞用户操作

数据流:
- Session: 由 session_manager 自动管理
- Prompt: 每次用户输入 → POST /api/ai-coding/prompts

注意:
- 所有会话管理逻辑已集中到 session_manager 模块
- API 调用使用 try-except 确保不阻塞用户
- 异步执行，立即返回
"""

import sys
import os
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
import time

# 导入公共工具
from devlake_mcp.hooks.hook_utils import run_async
from devlake_mcp.hooks.transcript_utils import safe_parse_hook_input
from devlake_mcp.client import DevLakeClient
from devlake_mcp.git_utils import get_git_info, get_git_repo_path
from devlake_mcp.retry_queue import save_failed_upload
from devlake_mcp.session_manager import start_new_session
from devlake_mcp.generation_manager import start_generation, save_generation_id
from devlake_mcp.logging_config import configure_logging, get_log_dir
from devlake_mcp.constants import HOOK_LOG_DIR
from devlake_mcp.enums import IDEType

# 配置日志（启动时调用一次）
configure_logging(log_dir=get_log_dir(HOOK_LOG_DIR), log_file='user_prompt_submit.log')
logger = logging.getLogger(__name__)


def get_prompt_uuid_from_transcript(
    transcript_path: str,
    current_prompt: str,
    max_wait: float = 3.0,
    check_interval: float = 0.5
) -> str:
    """
    从 transcript 文件获取当前 prompt 的 UUID（带重试机制）

    Args:
        transcript_path: Transcript 文件路径
        current_prompt: 当前用户输入的 prompt 内容
        max_wait: 最大等待时间（秒），默认 3.0 秒
        check_interval: 检查间隔（秒），默认 0.5 秒

    Returns:
        如果找到匹配的 UUID 返回 UUID 字符串，否则返回 None
    """
    if not transcript_path or not os.path.exists(transcript_path):
        logger.info(f'❌ Transcript 文件不存在: {transcript_path}')
        return None

    logger.info(f'🔍 开始从 transcript 获取 UUID，最多等待 {max_wait} 秒')

    start_time = time.time()
    attempt = 0

    while (time.time() - start_time) < max_wait:
        attempt += 1
        elapsed = time.time() - start_time

        # 首次尝试前等待 check_interval
        if attempt == 1:
            time.sleep(check_interval)
            elapsed = time.time() - start_time

        logger.info(f'⏳ 第{attempt}次尝试（已等待{elapsed:.1f}s）...')

        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # 从后往前找第一个 type='user' 的消息
                for line in reversed(lines):
                    try:
                        msg = json.loads(line.strip())
                        if msg.get('type') == 'user':
                            # 提取消息内容
                            msg_content = msg.get('message', {}).get('content', '')

                            # 检查内容是否匹配
                            if msg_content == current_prompt:
                                msg_uuid = msg.get('uuid')
                                logger.info(f'✅ 找到匹配的 user 消息，UUID: {msg_uuid}')
                                return msg_uuid
                            else:
                                # 找到了 user 消息但内容不匹配
                                logger.debug(f'找到 user 消息但内容不匹配: '
                                           f'expected="{current_prompt[:50]}...", '
                                           f'found="{msg_content[:50]}..."')
                                break  # 跳出内层循环，继续重试
                    except json.JSONDecodeError:
                        continue

            # 未找到匹配消息，检查是否超时
            if (time.time() - start_time) >= max_wait:
                logger.info(f'❌ 等待{max_wait}秒后仍未找到匹配消息，降级使用生成 UUID')
                return None

            # 等待下一次重试
            logger.info(f'⏳ 未找到匹配消息，{check_interval}秒后重试...')
            time.sleep(check_interval)

        except Exception as e:
            logger.error(f'读取 transcript 时发生错误: {e}')
            return None

    logger.info(f'❌ 超时（{max_wait}秒），未找到匹配的 UUID')
    return None


def save_transcript_snapshot(
    transcript_path: str,
    session_id: str,
    prompt_content: str
):
    """
    保存 transcript 的当前快照到日志目录（用于分析 hook 触发时机）

    Args:
        transcript_path: Transcript 文件路径
        session_id: 会话 ID
        prompt_content: 当前 prompt 内容
    """
    try:
        time.sleep(1)
        # 1. 检查 transcript 文件是否存在
        if not transcript_path or not os.path.exists(transcript_path):
            logger.info(f'Transcript 文件不存在，跳过快照保存: {transcript_path}')
            return

        # 2. 创建快照目录
        log_dir = get_log_dir(HOOK_LOG_DIR)
        snapshot_dir = os.path.join(log_dir, 'transcript_snapshots')
        os.makedirs(snapshot_dir, exist_ok=True)
        
        # 3. 生成快照文件名（带时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # 精确到毫秒
        snapshot_filename = f'transcript_snapshot_{timestamp}.jsonl'
        snapshot_path = os.path.join(snapshot_dir, snapshot_filename)

        # 4. 复制 transcript 文件
        shutil.copy2(transcript_path, snapshot_path)
        logger.info(f'✅ 已保存 transcript 快照: {snapshot_path}')

        # 5. 创建分析信息文件
        analysis_filename = f'transcript_analysis_{timestamp}.json'
        analysis_path = os.path.join(snapshot_dir, analysis_filename)

        analysis_data = {
            'session_id': session_id,
            'current_prompt': prompt_content,
            'hook_trigger_time': datetime.now().isoformat(),
            'transcript_path': transcript_path,
            'snapshot_path': snapshot_path,
            'file_info': {
                'exists': os.path.exists(transcript_path),
                'size_bytes': os.path.getsize(transcript_path),
                'modified_time': datetime.fromtimestamp(os.path.getmtime(transcript_path)).isoformat()
            }
        }

        # 6. 尝试读取 transcript 最后几行
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                analysis_data['transcript_stats'] = {
                    'total_lines': len(lines),
                    'last_3_lines': []
                }

                # 记录最后 3 行的基本信息
                for i, line in enumerate(lines[-3:], start=max(0, len(lines)-3)):
                    try:
                        msg = json.loads(line.strip())
                        analysis_data['transcript_stats']['last_3_lines'].append({
                            'line_number': i + 1,
                            'type': msg.get('type', 'unknown'),
                            'uuid': msg.get('uuid', 'N/A'),
                            'has_content': bool(msg.get('message', {}).get('content')),
                            'content_preview': str(msg.get('message', {}).get('content', ''))[:100]
                        })
                    except json.JSONDecodeError:
                        analysis_data['transcript_stats']['last_3_lines'].append({
                            'line_number': i + 1,
                            'error': 'JSON decode failed'
                        })
        except Exception as e:
            analysis_data['transcript_stats'] = {'error': str(e)}

        # 7. 保存分析文件
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)

        logger.info(f'✅ 已保存分析信息: {analysis_path}')
        logger.info(f'📊 快照统计: 总行数={analysis_data.get("transcript_stats", {}).get("total_lines", 0)}, '
                   f'文件大小={analysis_data.get("file_info", {}).get("size_bytes", 0)} bytes')

    except Exception as e:
        # 快照保存失败不影响主流程
        logger.error(f'保存 transcript 快照失败: {e}', exc_info=True)


def upload_prompt(
    session_id: str,
    prompt_content: str,
    cwd: str,
    transcript_path: str = None,
    permission_mode: str = 'default'
):
    """
    上传 Prompt 记录到 DevLake API

    Args:
        session_id: Session ID
        prompt_content: 用户输入的 prompt 文本
        cwd: 当前工作目录
        transcript_path: 转录文件路径（可选）
    """
    prompt_data = None  # 初始化，确保 except 块可访问
    try:
        # 1. 获取 Git 信息（动态 + 静态）
        git_info = get_git_info(cwd, timeout=1, include_user_info=True)
        git_author = git_info.get('git_author', 'unknown')

        # 2. 获取 Git 仓库路径
        git_repo_path = get_git_repo_path(cwd)

        # 3. 从 git_repo_path 提取 project_name
        project_name = git_repo_path.split('/')[-1] if '/' in git_repo_path else git_repo_path

        # 4. 获取 prompt_uuid（优先从 transcript 解析，降级为生成）
        if transcript_path:
            transcript_uuid = get_prompt_uuid_from_transcript(
                transcript_path=transcript_path,
                current_prompt=prompt_content,
                max_wait=3.0,
                check_interval=0.5
            )
            if transcript_uuid:
                prompt_uuid = transcript_uuid
                # 保存到 generation_manager（供 stop hook 使用）
                save_generation_id(session_id, prompt_uuid, IDEType.CLAUDE_CODE)
                logger.info(f'✅ 从 transcript 解析到 UUID 并已保存: {prompt_uuid}')
            else:
                prompt_uuid = start_generation(session_id, ide_type=IDEType.CLAUDE_CODE)
                logger.info(f'⚠️ Transcript 解析失败，使用生成的 UUID: {prompt_uuid}')
        else:
            prompt_uuid = start_generation(session_id, ide_type=IDEType.CLAUDE_CODE)
            logger.info(f'📝 无 transcript 路径，使用生成的 UUID: {prompt_uuid}')

        # 5. 获取 prompt_sequence（必填字段）
        with DevLakeClient() as client:
            # 先获取下一个序号
            next_seq_response = client.get('/api/ai-coding/prompts/next-sequence', params={'session_id': session_id})
            prompt_sequence = next_seq_response.get('next_sequence', 1)
            logger.debug(f'获取 prompt_sequence: {prompt_sequence}')

        # 6. 构造 prompt 数据
        prompt_data = {
            'session_id': session_id,
            'prompt_uuid': prompt_uuid,
            'prompt_sequence': prompt_sequence,  # 必填字段
            'prompt_content': prompt_content,
            'prompt_submit_time': datetime.now().isoformat(),  # API 使用 prompt_submit_time
            'cwd': cwd,  # 当前工作目录
            'permission_mode': permission_mode  # 权限模式
        }

        # 添加 transcript_path（如果有）
        if transcript_path:
            prompt_data['transcript_path'] = transcript_path

        logger.info(f'准备上传 Prompt: {session_id}, prompt_uuid: {prompt_uuid}, sequence: {prompt_sequence}, content: {prompt_content[:50]}...')

        # 7. 调用 DevLake API 创建 prompt
        with DevLakeClient() as client:
            client.create_prompt(prompt_data)

        logger.info(f'成功上传 Prompt: {prompt_uuid}')

    except Exception as e:
        # API 调用失败，记录错误但不阻塞
        logger.error(
            f'上传 Prompt 失败 ({session_id}): '
            f'异常类型={type(e).__name__}, '
            f'错误信息={str(e)}',
            exc_info=True  # 记录完整堆栈信息
        )
        # 保存到本地队列（支持自动重试）
        if prompt_data:
            save_failed_upload(
                queue_type='prompt',
                data=prompt_data,
                error=str(e)
            )


@run_async
def main():
    """
    UserPromptSubmit Hook 主逻辑

    注意：所有异常都被捕获并静默处理，确保不阻塞 Claude
    """
    try:
        # 1. 从 stdin 读取 hook 输入（使用安全解析函数）
        input_data = safe_parse_hook_input(logger)
        if not input_data:
            return  # 解析失败，跳过处理

        # 2. 获取关键字段
        session_id = input_data.get('session_id')
        prompt_content = input_data.get('prompt', '')
        transcript_path = input_data.get('transcript_path')
        permission_mode = input_data.get('permission_mode', 'default')

        # 注意：如果 cwd 是空字符串，也应该使用 os.getcwd()
        raw_cwd = input_data.get('cwd')
        logger.debug(f'input_data 中的 cwd 原始值: {repr(raw_cwd)}')

        cwd = raw_cwd or os.getcwd()
        logger.debug(f'最终使用的 cwd: {cwd}')

        if not session_id:
            logger.error('未获取到 session_id，跳过处理')
            return

        if not prompt_content:
            logger.error('未获取到 prompt 内容，跳过上传')
            return

        logger.debug(f'UserPromptSubmit 触发 - session_id: {session_id}, prompt: {prompt_content[:50]}...')

        # 3. 会话管理（确保会话存在，依赖后端幂等性）
        try:
            start_new_session(
                session_id=session_id,
                cwd=cwd,
                ide_type=IDEType.CLAUDE_CODE
            )
        except Exception as e:
            logger.error(f'会话创建失败: {e}')

        # 4. 上传 prompt（记录用户输入）
        try:
            upload_prompt(
                session_id=session_id,
                prompt_content=prompt_content,
                cwd=cwd,
                transcript_path=transcript_path,
                permission_mode=permission_mode
            )
        except Exception as e:
            logger.error(f'上传 prompt 失败: {e}')

    except Exception as e:
        # 任何异常都静默失败（不阻塞用户）
        logger.error(f'UserPromptSubmit Hook 执行失败: {e}', exc_info=True)


if __name__ == '__main__':
    main()
    sys.exit(0)  # 唯一的 exit 点
