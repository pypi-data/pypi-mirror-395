#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git 信息获取工具模块

提供 Git 仓库信息的获取功能：
- 当前分支
- 最新 commit hash
- Git 配置的用户名和邮箱
- 项目ID提取（namespace/name）

改进：
- 完整的类型注解
- 使用常量配置
- 更好的错误处理
- 完善的日志记录
"""

import subprocess
import os
import re
import logging
from pathlib import Path
from typing import Optional, Dict

from .constants import GIT_COMMAND_TIMEOUT

# 配置日志
logger = logging.getLogger(__name__)


def get_git_info(
    cwd: str,
    timeout: int = GIT_COMMAND_TIMEOUT,
    include_user_info: bool = True
) -> Dict[str, str]:
    """
    获取当前项目的 Git 信息

    Args:
        cwd: 项目根目录路径
        timeout: Git 命令超时时间（秒），默认 1 秒
        include_user_info: 是否获取用户信息（git_author/git_email），默认 True
                          如果环境变量已缓存，可以设为 False 提升性能

    Returns:
        Git 信息字典：
        {
            "git_branch": "feature/ai-coding",       # 当前分支
            "git_commit": "abc123def456...",         # 最新 commit hash（完整）
            "git_author": "wangzhong",               # Git 配置的用户名（可选）
            "git_email": "wangzhong@example.com"     # Git 配置的邮箱（可选）
        }

        如果不是 Git 仓库或获取失败，返回 "unknown"

    示例:
        >>> git_info = get_git_info('/path/to/project')
        >>> print(git_info['git_branch'])
        feature/ai-coding

        >>> # 如果用户信息已缓存，可以跳过获取
        >>> git_info = get_git_info('/path/to/project', include_user_info=False)
    """
    git_info = {
        "git_branch": "unknown",
        "git_commit": "unknown",
        "git_author": "unknown",
        "git_email": "unknown"
    }

    try:
        # 1. 检查是否是 Git 仓库
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        is_git_repo = (result.returncode == 0)

        if not is_git_repo:
            # 不是 Git 仓库，只获取全局配置
            logger.debug(f"目录不是 Git 仓库: {cwd}，尝试获取全局 Git 配置")

            if include_user_info:
                # 获取全局用户名
                result_global = subprocess.run(
                    ['git', 'config', '--global', 'user.name'],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                if result_global.returncode == 0:
                    git_info['git_author'] = result_global.stdout.strip()
                    logger.debug(f"Git author (global): {git_info['git_author']}")

                # 获取全局邮箱
                result_global = subprocess.run(
                    ['git', 'config', '--global', 'user.email'],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                if result_global.returncode == 0:
                    git_info['git_email'] = result_global.stdout.strip()
                    logger.debug(f"Git email (global): {git_info['git_email']}")

            return git_info

        # 2. 获取当前分支
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            git_info['git_branch'] = result.stdout.strip()
            logger.debug(f"Git 分支: {git_info['git_branch']}")
        else:
            logger.warning(f"无法获取 Git 分支: {result.stderr.strip()}")

        # 3. 获取最新 commit hash（完整 40 位）
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            git_info['git_commit'] = result.stdout.strip()
            logger.debug(f"Git commit: {git_info['git_commit'][:8]}")
        else:
            logger.warning(f"无法获取 Git commit: {result.stderr.strip()}")

        # 4. 获取 Git 配置的用户名和邮箱（可选）
        # 直接使用全局配置，简化逻辑并确保一致性
        if include_user_info:
            # 获取全局用户名
            result = subprocess.run(
                ['git', 'config', '--global', 'user.name'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                git_info['git_author'] = result.stdout.strip()
                logger.debug(f"Git author (global): {git_info['git_author']}")
            else:
                logger.warning("未配置 git user.name (--global)")

            # 获取全局邮箱
            result = subprocess.run(
                ['git', 'config', '--global', 'user.email'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if result.returncode == 0:
                git_info['git_email'] = result.stdout.strip()
                logger.debug(f"Git email (global): {git_info['git_email']}")
            else:
                logger.warning("未配置 git user.email (--global)")

    except subprocess.TimeoutExpired as e:
        # 超时，返回默认值
        logger.warning(f"Git 命令超时 ({timeout}秒): {e.cmd}")
    except FileNotFoundError:
        # git 命令未找到
        logger.error("Git 命令未找到，请确保已安装 Git")
    except Exception as e:
        # 其他异常
        logger.error(f"获取 Git 信息失败: {e}", exc_info=True)

    return git_info


def get_current_branch(cwd: str, timeout: int = GIT_COMMAND_TIMEOUT) -> str:
    """
    快速获取当前 Git 分支（简化版）

    Args:
        cwd: 项目根目录
        timeout: 超时时间（秒）

    Returns:
        分支名称，失败返回 'unknown'
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.debug(f"获取分支失败: {result.stderr.strip()}")
    except Exception as e:
        logger.warning(f"获取当前分支失败: {e}")

    return 'unknown'


def get_git_remote_url(cwd: str, timeout: int = GIT_COMMAND_TIMEOUT) -> Optional[str]:
    """
    获取 Git remote URL

    Args:
        cwd: 项目路径
        timeout: 超时时间（秒）

    Returns:
        Git remote URL，失败返回 None
    """
    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    return None


def extract_git_repo_path(git_remote_url: Optional[str], cwd: str) -> str:
    """
    从 Git remote URL 提取 git_repo_path (namespace/name)

    支持的格式：
    - https://github.com/yourorg/devlake.git -> yourorg/devlake
    - git@github.com:yourorg/devlake.git -> yourorg/devlake
    - https://gitlab.com/team/subteam/project.git -> team/subteam/project
    - git@gitlab.com:team/project.git -> team/project

    Args:
        git_remote_url: Git 远程仓库 URL
        cwd: 项目路径（作为 fallback）

    Returns:
        git_repo_path (namespace/name)
        如果无法提取，返回 'local/{directory_name}'
    """
    if not git_remote_url:
        # 没有 Git 仓库，使用 local/{dirname}
        return f"local/{Path(cwd).name}"

    # 去掉 .git 后缀（修复：使用 removesuffix 避免误删末尾字符）
    url = git_remote_url.removesuffix('.git')

    # 提取 namespace/name (支持多级 namespace)
    # 匹配格式：
    # - https://github.com/yourorg/devlake -> yourorg/devlake
    # - git@gitlab.com:team/project -> team/project
    # - https://gitlab.com/team/subteam/project -> team/subteam/project

    patterns = [
        # HTTPS 格式：https://domain.com/namespace/name
        r'https?://[^/]+/(.+)',
        # SSH 格式：git@domain.com:namespace/name
        r'git@[^:]+:(.+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # 解析失败，降级到 local/{dirname}
    return f"local/{Path(cwd).name}"


def get_git_repo_path(cwd: str) -> str:
    """
    获取Git仓库路径 (namespace/name)

    Args:
        cwd: 项目路径

    Returns:
        git_repo_path，如 'yourorg/devlake'
    """
    git_remote_url = get_git_remote_url(cwd)
    return extract_git_repo_path(git_remote_url, cwd)


def get_git_root(cwd: str, timeout: int = GIT_COMMAND_TIMEOUT) -> Optional[str]:
    """
    获取 Git 仓库根目录

    Args:
        cwd: 当前工作目录
        timeout: 超时时间（秒）

    Returns:
        Git 仓库根目录的绝对路径，失败返回 None
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    return None


def get_full_git_context(cwd: str, use_env_cache: bool = True) -> Dict[str, str]:
    """
    获取完整的 Git 上下文信息（统一接口）

    这个函数整合了静态和动态 Git 信息的获取逻辑，避免重复代码。

    策略：
    - 静态信息（author, email, repo_path）：
      * 如果 use_env_cache=True，优先从环境变量读取（避免重复执行 git config）
      * 如果环境变量不存在，则执行 git 命令获取
    - 动态信息（branch, commit）：始终执行 git 命令获取最新值
    - 衍生信息（project_name, git_root）：自动计算

    Args:
        cwd: 当前工作目录
        use_env_cache: 是否使用环境变量缓存的静态信息（默认 True）

    Returns:
        Dict[str, str]: 完整的 Git 上下文，包含：
            - git_branch: 当前分支
            - git_commit: 当前 commit hash（完整40位）
            - git_author: Git 用户名
            - git_email: Git 用户邮箱
            - git_repo_path: 仓库路径 (namespace/name)
            - project_name: 项目名称（从 repo_path 提取）
            - git_root: Git 仓库根目录（绝对路径）

    示例:
        >>> context = get_full_git_context('/path/to/project')
        >>> print(context['git_branch'])
        main
        >>> print(context['git_repo_path'])
        yourorg/devlake
        >>> print(context['project_name'])
        devlake

        >>> # 不使用缓存，强制重新获取
        >>> context = get_full_git_context('/path/to/project', use_env_cache=False)
    """
    context = {}

    # 1. 静态信息：优先从环境变量读取（避免重复执行 git config）
    if use_env_cache:
        context['git_author'] = os.getenv('GIT_AUTHOR', 'unknown')
        context['git_email'] = os.getenv('GIT_EMAIL', 'unknown')
        context['git_repo_path'] = os.getenv('GIT_REPO_PATH', 'unknown')

        # 如果环境变量不存在，则执行 git 命令获取
        if context['git_author'] == 'unknown' or context['git_email'] == 'unknown':
            git_info = get_git_info(cwd, include_user_info=True)
            if context['git_author'] == 'unknown':
                context['git_author'] = git_info.get('git_author', 'unknown')
            if context['git_email'] == 'unknown':
                context['git_email'] = git_info.get('git_email', 'unknown')

        if context['git_repo_path'] == 'unknown':
            context['git_repo_path'] = get_git_repo_path(cwd)
    else:
        # 不使用缓存，直接获取
        git_info = get_git_info(cwd, include_user_info=True)
        context['git_author'] = git_info.get('git_author', 'unknown')
        context['git_email'] = git_info.get('git_email', 'unknown')
        context['git_repo_path'] = get_git_repo_path(cwd)

    # 2. 动态信息：每次获取最新值（确保 branch/commit 正确）
    git_info = get_git_info(cwd, include_user_info=False)
    context['git_branch'] = git_info.get('git_branch', 'unknown')
    context['git_commit'] = git_info.get('git_commit', 'unknown')

    # 3. 衍生信息：自动计算
    # 提取 project_name（从 repo_path 最后一段）
    repo_path = context['git_repo_path']
    context['project_name'] = repo_path.split('/')[-1] if '/' in repo_path else repo_path

    # 获取 git_root
    context['git_root'] = get_git_root(cwd) or ''

    logger.debug(
        f"Git 上下文: {context['project_name']} "
        f"({context['git_branch']}@{context['git_commit'][:8]})"
    )

    return context


def get_git_context_from_file(file_path: str, use_env_cache: bool = True) -> Dict[str, str]:
    """
    从文件路径获取 Git 上下文（支持 workspace 多项目环境）

    这个函数专门用于处理文件变更场景，能够正确识别 workspace 中不同子项目的 Git 仓库。

    工作原理：
    1. 从文件所在目录向上查找 .git 目录（获取 git_root）
    2. 基于 git_root 获取完整的 Git 上下文
    3. 如果找不到 git_root，降级到文件所在目录

    使用场景：
    - 文件编辑/创建操作（Edit/Write tool）
    - Shell 命令修改文件
    - 任何有具体文件路径的操作

    Workspace 支持：
    在 workspace 环境下，不同的文件可能属于不同的 git 仓库：
    ```
    workspace/
    ├── project-a/ (git: yourorg/project-a)
    │   └── main.py
    └── project-b/ (git: yourorg/project-b)
        └── app.py

    get_git_context_from_file('workspace/project-a/main.py')
    → git_repo_path = 'yourorg/project-a'  ✓

    get_git_context_from_file('workspace/project-b/app.py')
    → git_repo_path = 'yourorg/project-b'  ✓
    ```

    Args:
        file_path: 文件路径（可以是相对路径或绝对路径）
        use_env_cache: 是否使用环境变量缓存的静态信息（默认 True）

    Returns:
        Dict[str, str]: 完整的 Git 上下文，包含：
            - git_branch: 当前分支
            - git_commit: 当前 commit hash
            - git_author: Git 用户名
            - git_email: Git 用户邮箱
            - git_repo_path: 仓库路径 (namespace/name)
            - project_name: 项目名称
            - git_root: Git 仓库根目录

    示例:
        >>> # Workspace 环境
        >>> context = get_git_context_from_file('/workspace/project-a/src/main.py')
        >>> print(context['git_repo_path'])
        yourorg/project-a

        >>> # 单项目环境（向后兼容）
        >>> context = get_git_context_from_file('/project/src/utils.py')
        >>> print(context['git_repo_path'])
        yourorg/project
    """
    # 1. 转换为绝对路径
    abs_file_path = os.path.abspath(file_path)

    # 2. 获取文件所在目录
    file_dir = os.path.dirname(abs_file_path)

    # 3. 从文件所在目录向上查找 Git 仓库根目录
    git_root = get_git_root(file_dir)

    # 4. 基于 git_root 获取完整的 Git 上下文
    if git_root:
        # 找到了 git root，使用它作为工作目录
        logger.debug(f'从文件 {abs_file_path} 找到 Git root: {git_root}')
        return get_full_git_context(git_root, use_env_cache=use_env_cache)
    else:
        # 降级方案：使用文件所在目录
        logger.warning(
            f'文件 {abs_file_path} 不在 Git 仓库中，'
            f'使用文件所在目录 {file_dir} 作为 fallback'
        )
        return get_full_git_context(file_dir, use_env_cache=use_env_cache)
