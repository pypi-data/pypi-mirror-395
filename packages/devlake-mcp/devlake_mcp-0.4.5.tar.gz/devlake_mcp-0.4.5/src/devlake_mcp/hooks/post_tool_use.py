#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Hooks: AI出码数据采集脚本（v1.5 重构版本）

改进：
- 添加统一的日志系统（参考 stop.py）
- 添加异步执行，立即返回，不阻塞工具执行
- 移除本地 diff 计算（改为云端计算）
- 添加 gzip 压缩传输
- 完整上传 before/after 内容（不截断）
- 添加降级方案（API 失败时保存本地）
- 跨平台临时目录支持（Windows/macOS/Linux）

作者：Claude Code
版本：v1.5
日期：2025-01-04
"""

import json
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# 导入公共工具（使用包导入）
from devlake_mcp.enums import IDEType
from devlake_mcp.hooks.hook_utils import run_async
from devlake_mcp.utils import get_temp_file_path, compress_content
from devlake_mcp.hooks.transcript_utils import safe_parse_hook_input
from devlake_mcp.git_utils import get_git_context_from_file
from devlake_mcp.client import DevLakeClient
from devlake_mcp.retry_queue import save_failed_upload
from devlake_mcp.generation_manager import get_current_generation_id
from devlake_mcp.logging_config import configure_logging, get_log_dir
from devlake_mcp.constants import HOOK_LOG_DIR

# 配置日志（启动时调用一次）
configure_logging(log_dir=get_log_dir(HOOK_LOG_DIR), log_file='post_tool_use.log')
logger = logging.getLogger(__name__)


# ============================================================================
# 上传功能
# ============================================================================


def upload_to_api(change_data: dict) -> bool:
    """
    同步上传数据到 DevLake API

    Args:
        change_data: 变更数据字典

    Returns:
        是否上传成功
    """
    try:
        client = DevLakeClient()
        client.create_file_changes([change_data])
        logger.info(f'成功上传文件变更: {change_data.get("file_path")}')
        return True
    except Exception as e:
        logger.error(f'上传文件变更失败: {e}')
        return False


# ============================================================================
# 临时文件管理（PreToolUse 使用）
# ============================================================================

def load_before_content(session_id: str, file_path: str) -> str:
    """
    从临时文件加载 before_content

    Args:
        session_id: 会话ID
        file_path: 文件路径

    Returns:
        文件的 before_content，如果不存在返回空字符串
    """
    temp_file = get_temp_file_path(session_id, file_path)

    try:
        if os.path.exists(temp_file):
            with open(temp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('content', '')
    except Exception:
        pass

    return ''


def get_current_file_content(file_path: str) -> str:
    """
    读取文件当前内容

    Args:
        file_path: 文件路径

    Returns:
        文件内容，读取失败返回空字符串
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass

    return ''


# ============================================================================
# 辅助函数
# ============================================================================

def get_file_type(file_path: str) -> str:
    """获取文件类型"""
    return Path(file_path).suffix.lstrip('.') or 'unknown'


def extract_user_info(session_id: str) -> dict:
    """从环境变量提取用户信息"""
    return {
        'user_name': os.getenv('USER', 'unknown'),
        'project_name': Path(os.getcwd()).name
    }


def should_collect_file(file_path: str) -> bool:
    """判断是否应该采集该文件"""
    # 排除敏感文件
    sensitive_patterns = ['.env', '.secret', '.key']
    file_path_lower = file_path.lower()

    for pattern in sensitive_patterns:
        if pattern in file_path_lower:
            return False

    # 排除二进制文件（通过后缀判断）
    binary_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico',
        '.pdf', '.zip', '.tar', '.gz', '.rar',
        '.exe', '.dll', '.so', '.dylib',
        '.class', '.pyc', '.pyo'
    }

    file_ext = Path(file_path).suffix.lower()
    if file_ext in binary_extensions:
        return False

    return True


# ============================================================================
# 主逻辑
# ============================================================================

@run_async
def main():
    """
    PostToolUse Hook 主逻辑

    注意：所有异常都被捕获并静默处理，确保不阻塞 Claude
    """
    temp_file = None  # 初始化临时文件路径
    try:
        # 读取 Hook 输入（使用安全解析函数）
        input_data = safe_parse_hook_input(logger)
        if not input_data:
            return  # 解析失败，跳过处理

        hook_event_name = input_data.get('hook_event_name')
        tool_name = input_data.get('tool_name')
        tool_input = input_data.get('tool_input', {})
        session_id = input_data.get('session_id')

        # 获取当前工作目录（用于获取 Git 信息）
        cwd = input_data.get('cwd', os.getcwd())

        # 只处理 PostToolUse 事件
        if hook_event_name != 'PostToolUse':
            return

        # 只处理文件修改相关的工具
        if tool_name not in ['Write', 'Edit', 'NotebookEdit']:
            return

        logger.debug(f'PostToolUse Hook 触发 - tool: {tool_name}, session: {session_id}')

        # 提取文件路径
        file_path = tool_input.get('file_path') or tool_input.get('notebook_path')
        if not file_path:
            logger.debug('没有 file_path，跳过')
            return

        # 转换为绝对路径
        if not os.path.isabs(file_path):
            cwd = input_data.get('cwd', os.getcwd())
            file_path = os.path.join(cwd, file_path)

        # 检查是否应该采集
        if not should_collect_file(file_path):
            logger.debug(f'文件不需要采集（敏感文件或二进制文件）: {file_path}')
            return

        logger.info(f'开始处理文件变更: {file_path}')

        # 获取用户信息
        user_info = extract_user_info(session_id)

        # ====================================================================
        # v1.3 核心改进：同步上传 + 分支支持
        # ====================================================================

        # 1. 获取临时文件路径（用于后续清理）
        temp_file = get_temp_file_path(session_id, file_path)

        # 2. 从 PreToolUse 临时文件加载 before_content
        before_content = load_before_content(session_id, file_path)

        # 3. 读取当前文件内容（after_content）
        after_content = get_current_file_content(file_path)

        # 4. 压缩内容（减少传输大小）
        before_content_gz = compress_content(before_content)
        after_content_gz = compress_content(after_content)

        # ====================================================================
        # Git 信息获取策略：基于文件路径获取 Git 上下文（支持 workspace）
        # - 从文件路径向上查找 .git 目录
        # - 静态信息（author, email, repo_path）：优先从环境变量读取
        # - 动态信息（branch, commit）：每次执行 git 命令获取最新值
        # ====================================================================

        # 5. 获取完整的 Git 上下文（基于文件路径，支持 workspace 多项目）
        git_context = get_git_context_from_file(file_path, use_env_cache=True)
        git_author = git_context.get('git_author', 'unknown')
        git_email = git_context.get('git_email', 'unknown')
        git_repo_path = git_context.get('git_repo_path', 'unknown')
        git_branch = git_context.get('git_branch', 'unknown')
        git_commit = git_context.get('git_commit', 'unknown')

        # 6. 其他配置
        ide_type = 'claude_code'  # 固定值
        model_name = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5')

        logger.debug(f'Git 信息 - branch: {git_branch}, '
                    f'commit: {git_commit[:8] if git_commit != "unknown" else "unknown"}, '
                    f'email: {git_email}, repo: {git_repo_path}')

        # 6. 转换 file_path 为相对路径（使用 git_context 中的 git_root）
        git_root = git_context.get('git_root')
        if git_root:
            try:
                # 计算相对路径
                relative_path = os.path.relpath(file_path, git_root)
                logger.debug(f'文件路径转换: {file_path} -> {relative_path}')
                file_path = relative_path
            except Exception as e:
                # 如果转换失败，保持原路径
                logger.warning(f'路径转换失败: {e}')

        # 7. 获取 prompt_uuid（关联到具体的 prompt）
        prompt_uuid = get_current_generation_id(session_id, ide_type=IDEType.CLAUDE_CODE)
        logger.debug(f'获取到 prompt_uuid: {prompt_uuid}')

        # 8. 构造上报数据（不包含 diff 计算结果）
        change_data = {
            'session_id': session_id,
            'prompt_uuid': prompt_uuid,                   # 新增：关联到具体的 prompt
            'user_name': user_info['user_name'],
            'ide_type': ide_type,                         # IDE 类型
            'model_name': model_name,                     # AI 模型名称
            'git_repo_path': git_repo_path,               # Git仓库路径 (namespace/name)
            'project_name': user_info['project_name'],
            'file_path': file_path,                       # 相对路径
            'file_type': get_file_type(file_path),
            'change_type': 'create' if tool_name == 'Write' else 'edit',
            'tool_name': tool_name,
            'before_content_gz': before_content_gz,       # 压缩内容
            'after_content_gz': after_content_gz,         # 压缩内容
            'git_branch': git_branch,                     # Git 分支（动态）
            'git_commit': git_commit,                     # Git commit（动态）
            'git_author': git_author,                     # Git 作者（环境变量）
            'git_email': git_email,                       # Git 邮箱（环境变量）
            'change_time': datetime.now().isoformat(),
            'cwd': cwd
        }

        # 9. 同步上传到 API（超时 3 秒）
        success = upload_to_api(change_data)

        if not success:
            # 上传失败，保存到本地队列（支持自动重试）
            logger.warning(f'API 上传失败，保存到本地队列: {file_path}')
            save_failed_upload(
                queue_type='file_change',
                data=change_data,
                error='API upload failed'
            )

    except Exception as e:
        # 任何异常都静默失败，不阻塞 Claude
        logger.error(f'PostToolUse Hook 执行失败: {e}', exc_info=True)
    finally:
        # 10. 清理临时文件（使用 finally 确保一定执行）
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                logger.debug(f'清理临时文件: {temp_file}')
            except Exception as e:
                logger.warning(f'清理临时文件失败: {e}')


if __name__ == '__main__':
    main()
    sys.exit(0)  # 唯一的 exit 点
