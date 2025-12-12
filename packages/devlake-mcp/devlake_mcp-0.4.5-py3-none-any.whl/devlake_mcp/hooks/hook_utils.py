#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Hooks 公共工具模块

提供跨 hooks 脚本的通用功能：
- 错误日志记录
- 本地队列保存（降级方案）
- 统一的 logging 配置
- 异步执行包装

注意：临时目录等通用功能已移至 devlake_mcp.utils，避免重复代码
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Callable

# 导入通用工具函数（避免代码重复）
from devlake_mcp.utils import get_data_dir, get_temp_file_path
from devlake_mcp.constants import HOOK_LOG_DIR

# 注意：hook_utils 是基础模块，不导入其他 hooks 模块以避免循环依赖


# 模块级 logger（Python logging 有 lastResort 机制，无需手动配置）
logger = logging.getLogger(__name__)


def save_to_local_queue(queue_name: str, data: dict):
    """
    保存数据到本地队列（降级方案）

    用于 API 上传失败时的备份，后续可通过定时脚本重试上传

    Args:
        queue_name: 队列名称（如 'failed_session_uploads'）
        data: 要保存的数据字典

    文件格式:
        ~/.devlake/{queue_name}/{timestamp}.json
    """
    try:
        queue_dir = get_data_dir(persistent=True) / queue_name
        queue_dir.mkdir(parents=True, exist_ok=True)

        # 使用时间戳作为文件名，确保唯一性
        filename = f"{int(datetime.now().timestamp() * 1000)}.json"
        queue_file = queue_dir / filename

        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # 记录失败，不影响主流程（Python logging 会自动输出到 stderr）
        logger.error(
            f"Failed to save to local queue '{queue_name}': {e}",
            exc_info=True
        )


def cleanup_old_files(directory: str, max_age_hours: int = 24):
    """
    清理指定目录中的过期文件

    Args:
        directory: 目录名称（相对于持久化数据目录）
        max_age_hours: 最大保留时间（小时）

    示例:
        cleanup_old_files('failed_session_uploads', max_age_hours=168)  # 7天
    """
    try:
        target_dir = get_data_dir(persistent=True) / directory
        if not target_dir.exists():
            return

        now = datetime.now().timestamp()
        max_age_seconds = max_age_hours * 3600

        for file in target_dir.iterdir():
            if file.is_file():
                file_age = now - file.stat().st_mtime
                if file_age > max_age_seconds:
                    file.unlink()
    except Exception as e:
        # 记录失败，不影响主流程（Python logging 会自动输出到 stderr）
        logger.error(
            f"Failed to cleanup old files in '{directory}': {e}",
            exc_info=True
        )


__all__ = ['save_to_local_queue', 'cleanup_old_files', 'run_async']


def run_async(func: Callable):
    """
    异步执行装饰器，让 hook 立即返回，后台执行任务

    原理（标准的双重 fork daemon 化）：
    1. 第一次 fork：创建子进程，父进程立即退出
    2. setsid()：子进程创建新会话，脱离控制终端
    3. 第二次 fork：创建孙进程，第一个子进程退出
    4. 孙进程（真正的 daemon）执行实际工作

    为什么需要双重 fork？
    - 单次 fork：子进程仍在父进程的会话中，可能被 Claude Code 等待
    - setsid()：创建新会话，但子进程成为 session leader
    - 第二次 fork：确保孙进程不是 session leader，完全独立

    参考：Stevens "Advanced Programming in the UNIX Environment"

    使用方法：
        @run_async
        def main():
            # 你的 hook 逻辑
            pass

        if __name__ == '__main__':
            main()

    优点：
    - hook 0 延迟，不阻塞 Claude 响应（即使 API 超时 10 秒）
    - 完全脱离父进程会话，不会被等待
    - API 调用慢或失败不影响用户体验

    注意：
    - 只在 Unix-like 系统（macOS/Linux）使用 fork
    - Windows 会降级为同步执行（因为 fork 不可用）
    """
    def wrapper(*args, **kwargs):
        # 检查是否支持 fork（Unix-like 系统）
        if sys.platform == 'win32' or not hasattr(os, 'fork'):
            # Windows 或不支持 fork 的系统，降级为同步执行
            func(*args, **kwargs)
            _check_and_retry_uploads()  # 同步模式下也检查重试
            return

        # === 第一次 fork ===
        try:
            pid = os.fork()
        except OSError:
            # fork 失败，降级为同步执行
            func(*args, **kwargs)
            _check_and_retry_uploads()
            return

        if pid > 0:
            # 父进程：立即退出（返回给 Claude Code）
            os._exit(0)

        # === 第一个子进程 ===
        try:
            # 创建新会话，脱离控制终端
            # 此时子进程成为 session leader
            os.setsid()
        except OSError:
            # setsid 失败，退出
            os._exit(1)

        # === 第二次 fork ===
        try:
            pid = os.fork()
        except OSError:
            # fork 失败，退出
            os._exit(1)

        if pid > 0:
            # 第一个子进程：退出
            # 让孙进程被 init 进程接管
            os._exit(0)

        # === 孙进程（真正的 daemon）===
        try:
            # 1. 读取 stdin 内容（在关闭文件描述符之前）
            from io import StringIO
            try:
                stdin_content = sys.stdin.read()
            except Exception:
                stdin_content = ''

            # 2. 关闭并重定向标准文件描述符（关键！）
            # 这是 daemon 化的必要步骤，确保 subprocess.run 不会等待
            sys.stdout.flush()
            sys.stderr.flush()

            # 关闭标准输入/输出/错误的文件描述符
            os.close(0)  # stdin
            os.close(1)  # stdout
            os.close(2)  # stderr

            # 重新打开到 /dev/null 或日志文件
            # stdin -> /dev/null
            os.open('/dev/null', os.O_RDONLY)  # 返回 fd 0

            # stdout 和 stderr -> 保留日志功能
            # 注意：由于我们已经配置了 logging 到文件，这里重定向到 /dev/null 不影响日志
            os.open('/dev/null', os.O_WRONLY)  # 返回 fd 1 (stdout)
            os.open('/dev/null', os.O_WRONLY)  # 返回 fd 2 (stderr)

            # 3. 用 StringIO 替换 Python 的 sys.stdin（让代码能正常读取）
            sys.stdin = StringIO(stdin_content)

            # 4. 执行主 hook 逻辑
            func(*args, **kwargs)

            # 5. 检查并重试失败的上传记录（非阻塞）
            _check_and_retry_uploads()

            # daemon 正常退出
            os._exit(0)
        except Exception:
            # daemon 异常退出
            os._exit(1)

    return wrapper


def _check_and_retry_uploads():
    """
    检查并重试失败的上传记录（内部函数）

    说明：
    - 每次 Hook 执行时自动调用
    - 非阻塞，快速返回（默认最多重试3条记录）
    - 静默失败，不影响主流程
    """
    try:
        # 延迟导入，避免循环依赖
        from devlake_mcp.retry_queue import retry_failed_uploads, get_retry_config

        # 检查是否启用重试
        config = get_retry_config()
        if not config.get('check_on_hook', True):
            return

        # 执行重试（限制单次最多3条，避免阻塞）
        retry_failed_uploads(max_parallel=3)

    except Exception as e:
        # 静默失败，不影响主流程
        logger.debug(f"重试检查失败（不影响主流程）: {e}")
