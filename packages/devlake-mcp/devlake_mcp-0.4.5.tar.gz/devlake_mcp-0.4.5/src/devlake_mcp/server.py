"""
DevLake MCP 服务器实现

使用 FastMCP 框架实现 MCP 服务器，提供与 DevLake 交互的工具。

## 核心原则

**一句话记住**：有文件内容变更必须记录，无文件内容变更不需要记录。

```
文件内容变更操作 = beforeEditFile → [执行变更] → afterEditFile → recordSession
纯对话/只读操作 = 无需调用 beforeEditFile/afterEditFile
每次对话结束 = recordSession（记录会话）
```

## MCP 工具概览

### 1. recordSession - 会话记录
- **调用时机**：**每次对话结束时** ← 重要！
- **用途**：记录 AI 会话的元数据和统计信息
- **必需参数**：无（sessionId 可选，可自动生成）

### 2. beforeEditFile - 文件变更前记录
- **调用时机**：在执行 Write/Edit/NotebookEdit 等文件变更操作**之前立即调用**
- **用途**：记录文件的原始状态（快照）
- **必需参数**：sessionId（与 recordSession 返回的一致）, filePaths（绝对路径列表）

### 3. afterEditFile - 文件变更后记录
- **调用时机**：在文件变更操作完成**之后立即调用**
- **用途**：记录文件的最终状态，计算差异并上传
- **必需参数**：sessionId（与 beforeEditFile 一致）, filePaths（绝对路径列表）
- **建议参数**：metadata（包含 ide 和 model 信息，如 {"ide": "cursor", "model": "claude-sonnet-4-5"}）

## 操作分类

### ✅ 需要 MCP 记录的操作（文件内容变更）
- Write, create_file - 创建新文件
- Edit, search_replace, edit_file - 修改现有文件
- delete_file - 删除文件
- NotebookEdit - 编辑 Jupyter Notebook
- MultiEdit - 多文件编辑

### ❌ 不需要 MCP 记录的操作（只读或非文件操作）
- Read, read_file - 读取文件
- Glob, Grep, find - 搜索文件或内容
- Bash, shell - 执行系统命令
- WebFetch, WebSearch - 网络操作
- 纯对话 - AI 纯文本回复

## 强制要求

1. **100% 覆盖**：所有文件内容变更都必须调用 beforeEditFile + afterEditFile
2. **严格配对**：每次 beforeEditFile 必须有且仅有一次对应的 afterEditFile
3. **会话一致**：整个对话使用相同的 sessionId
4. **绝对路径**：filePaths 必须是绝对路径
5. **即时调用**：beforeEditFile 和 afterEditFile 必须紧邻文件变更操作

## 常见错误

❌ **错误 1**：只调用 beforeEditFile 不调用 afterEditFile
❌ **错误 2**：对只读操作（如 Read）也调用 MCP 工具
❌ **错误 3**：使用相对路径而非绝对路径
❌ **错误 4**：在不同操作中使用不同的 sessionId
❌ **错误 5**：合并多次操作到一次 afterEditFile（应批量记录）

## 详细文档

完整的使用指南请参考：
- MCP_TOOLS_USAGE_GUIDE.md - 完整的工具使用指南
- .cursorrules.template - Cursor IDE 的规则模板
- DESIGN.md - 项目设计文档
"""

import os
import json
import uuid
import sys
from typing import Optional, List
from datetime import datetime
from pathlib import Path

# 条件导入 fastmcp（需要 Python 3.10+ 且已安装）
from .compat import MCP_AVAILABLE, HAS_MCP_SUPPORT, FastMCP, get_compatibility_warnings

from .client import DevLakeClient
from .git_utils import get_git_info, get_git_repo_path, get_git_root, get_full_git_context
from .version_utils import detect_platform_info
from .logging_config import configure_logging
from .utils import (
    get_temp_file_path,
    compress_content,
    should_collect_file,
    get_file_type,
    read_file_content
)

# 创建 MCP 服务器实例（仅在 MCP 可用时）
# 如果 Python < 3.10 或 fastmcp 未安装，mcp 为 None
mcp = FastMCP("devlake-mcp") if MCP_AVAILABLE else None


# ============================================================================
# 工具实现函数（可直接测试）
# ============================================================================

def record_session_impl(
    session_id: Optional[str] = None,
    metadata: Optional[dict] = None
) -> dict:  
    """
    记录 AI 会话的元数据和统计信息

    在会话开始时调用，创建会话记录并获取 session_id。

    """
    try:
        # 1. 生成或使用提供的 session_id
        if not session_id:
            session_id = str(uuid.uuid4())

        # 2. 获取项目路径（优先使用 metadata，否则使用当前目录）
        metadata = metadata or {}
        cwd = metadata.get('project_path') or os.getcwd()

        # 3. 获取 Git 信息（动态：branch/commit + 静态：author/email）
        git_info = get_git_info(cwd, timeout=1, include_user_info=True)
        git_branch = git_info.get('git_branch', 'unknown')
        git_commit = git_info.get('git_commit', 'unknown')
        git_author = git_info.get('git_author', 'unknown')
        git_email = git_info.get('git_email', 'unknown')

        # 4. 获取 Git 仓库路径（namespace/name）
        git_repo_path = get_git_repo_path(cwd)

        # 5. 从 git_repo_path 提取 project_name
        # 例如：yourorg/devlake -> devlake, team/subteam/project -> project
        project_name = git_repo_path.split('/')[-1] if '/' in git_repo_path else git_repo_path

        # 6. 检测平台信息和版本
        ide_type = metadata.get('ide', 'unknown')
        platform_info = detect_platform_info(ide_type=ide_type)

        # 7. 构造会话数据
        session_data = {
            'session_id': session_id,
            'user_name': git_author,  # 使用 Git 配置的用户名
            'ide_type': ide_type,
            'model_name': metadata.get('model', 'unknown'),
            'git_repo_path': git_repo_path,
            'project_name': project_name,
            'session_start_time': datetime.now().isoformat(),
            'conversation_rounds': 0,
            'is_adopted': 0,
            'git_branch': git_branch,
            'git_commit': git_commit,
            'git_author': git_author,
            'git_email': git_email,
            # 新增：版本信息
            'devlake_mcp_version': platform_info['devlake_mcp_version'],
            'ide_version': platform_info['ide_version'],
            'data_source': 'mcp'  # MCP 数据来源（区别于 hook）
        }

        # 8. 调用 DevLake API 创建会话（使用 context manager）
        with DevLakeClient() as client:
            response = client.post('/api/ai-coding/sessions', session_data)

        # 9. 返回结果
        return {
            'success': True,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'git_info': {
                'git_repo_path': git_repo_path,
                'project_name': project_name,
                'git_branch': git_branch,
                'git_commit': git_commit[:8] if git_commit != 'unknown' else 'unknown',
                'git_author': git_author,
                'git_email': git_email
            }
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'session_id': session_id if session_id else 'unknown'
        }


def before_edit_file_impl(
    session_id: str,
    file_paths: List[str]
) -> dict:
    """
    在文件内容变更操作前调用，记录变更前的文件状态

    读取文件的当前内容并保存到临时文件，供 afterEditFile 使用。

    Args:
        session_id: 会话唯一标识
        file_paths: 即将变更的文件绝对路径列表

    Returns:
        dict: {
            "success": true,
            "session_id": "session-123",
            "timestamp": "2025-01-07T10:00:00Z",
            "files_snapshot": {
                "/path/to/file1.py": {
                    "exists": true,
                    "line_count": 100,
                    "size": 2048
                }
            }
        }

    示例:
        >>> before_edit_file("session-123", ["/path/to/file.py"])
        {"success": true, "files_snapshot": {...}}
    """
    try:
        files_snapshot = {}

        for file_path in file_paths:
            # 1. 转换为绝对路径
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            # 2. 检查是否应该采集
            if not should_collect_file(file_path):
                files_snapshot[file_path] = {
                    'skipped': True,
                    'reason': 'Sensitive or binary file'
                }
                continue

            # 3. 读取文件内容（如果存在）
            exists = os.path.exists(file_path)
            content = ''

            if exists:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception:
                    # 读取失败（如二进制文件），跳过
                    files_snapshot[file_path] = {
                        'skipped': True,
                        'reason': 'Failed to read file (possibly binary)'
                    }
                    continue

            # 4. 保存到临时文件
            temp_file = get_temp_file_path(session_id, file_path)
            try:
                with open(temp_file, 'w', encoding='utf-8') as f:
                    data = {
                        'file_path': file_path,
                        'content': content,
                        'timestamp': datetime.now().isoformat()
                    }
                    json.dump(data, f)
            except Exception as e:
                files_snapshot[file_path] = {
                    'skipped': True,
                    'reason': f'Failed to save temp file: {str(e)}'
                }
                continue

            # 5. 记录快照信息
            files_snapshot[file_path] = {
                'exists': exists,
                'line_count': len(content.splitlines()) if content else 0,
                'size': len(content.encode('utf-8')) if content else 0
            }

        return {
            'success': True,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'files_snapshot': files_snapshot
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'session_id': session_id
        }


def after_edit_file_impl(
    session_id: str,
    file_paths: List[str],
    metadata: Optional[dict] = None
) -> dict:
    """
    在文件内容变更操作后调用，记录变更后的文件状态

    读取文件变更后的内容，对比变更前后的差异，并上传到 DevLake API。

    Args:
        session_id: 会话唯一标识（与 beforeEditFile 保持一致）
        file_paths: 已变更的文件绝对路径列表
        metadata: 可选的会话元数据，包含 ide 和 model 信息

    Returns:
        dict: {
            "success": true,
            "session_id": "session-123",
            "timestamp": "2025-01-07T10:01:00Z",
            "uploaded_count": 2,
            "changes": [...]
        }

    示例:
        >>> after_edit_file("session-123", ["/path/to/file.py"], {"ide": "cursor", "model": "claude-sonnet-4-5"})
        {"success": true, "uploaded_count": 1, ...}
    """
    try:
        changes = []
        cwd = os.getcwd()

        # 获取完整的 Git 上下文（使用统一接口，避免代码重复）
        git_context = get_full_git_context(cwd, use_env_cache=True)
        git_author = git_context['git_author']
        git_email = git_context['git_email']
        git_repo_path = git_context['git_repo_path']
        git_branch = git_context['git_branch']
        git_commit = git_context['git_commit']
        project_name = git_context['project_name']
        git_root = git_context['git_root']

        # 从 metadata 中获取 ide_type 和 model_name
        metadata = metadata or {}
        ide_type = metadata.get('ide', 'unknown')
        model_name = metadata.get('model', 'unknown')

        for file_path in file_paths:
            # 1. 转换为绝对路径
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

            # 2. 检查是否应该采集
            if not should_collect_file(file_path):
                continue

            # 3. 从临时文件加载 before_content
            temp_file = get_temp_file_path(session_id, file_path)
            before_content = ''

            if os.path.exists(temp_file):
                try:
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        before_content = data.get('content', '')
                except Exception:
                    pass

            # 4. 读取当前文件内容（after_content）
            after_content = read_file_content(file_path)

            # 5. 压缩内容（gzip + base64）
            before_content_gz = compress_content(before_content)
            after_content_gz = compress_content(after_content)

            # 6. 转换文件路径为相对路径（相对于 git root）
            relative_path = file_path
            if git_root:
                try:
                    relative_path = os.path.relpath(file_path, git_root)
                except Exception:
                    pass

            # 7. 判断变更类型
            change_type = 'create' if not before_content else 'edit'

            # 8. 构造变更数据
            change_data = {
                'session_id': session_id,
                'user_name': git_author,
                'ide_type': ide_type,
                'model_name': model_name,
                'git_repo_path': git_repo_path,
                'project_name': project_name,
                'file_path': relative_path,
                'file_type': get_file_type(file_path),
                'change_type': change_type,
                'tool_name': 'MCP',  # MCP 工具标识
                'before_content_gz': before_content_gz,
                'after_content_gz': after_content_gz,
                'git_branch': git_branch,
                'git_commit': git_commit,
                'git_author': git_author,
                'git_email': git_email,
                'change_time': datetime.now().isoformat(),
                'cwd': cwd
            }

            changes.append(change_data)

            # 9. 清理临时文件
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

        # 10. 批量上传到 DevLake API（使用 context manager）
        if changes:
            with DevLakeClient() as client:
                response = client.post('/api/ai-coding/file-changes', {'changes': changes})

        return {
            'success': True,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'uploaded_count': len(changes),
            'changes': [
                {
                    'file_path': c['file_path'],
                    'change_type': c['change_type'],
                    'file_type': c['file_type']
                }
                for c in changes
            ]
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'session_id': session_id
        }


# ============================================================================
# MCP 工具装饰器（包装实现函数）
# 注意：这些装饰器仅在 MCP 可用时才会生效
# ============================================================================

# 仅在 MCP 可用时注册工具
if mcp is not None:
    @mcp.tool
    def record_session(
        session_id: str,
        metadata: dict
    ) -> dict:
        """
        记录 AI 会话的元数据和统计信息

        ## 调用时机

        ✅ **每次对话结束时** ← 重要！必须调用

        ## 用途

        记录 AI 会话的元数据和统计信息，包括：
        - 用户消息
        - AI回复
        - 使用的模型和 IDE

        ## 参数

        Args:
            session_id: 会话 ID（必填，示例：1c1a4b88-8701-4dc0-b53f-9d5262ac6628，整个对话开始时应确定一个统一的sessionId，并在所有后续对话轮次操作中保持该ID不变）
            metadata: 会话元数据（必填），支持字段：
                - prompt_content: 用户消息（如 "实现用户登录功能"）
                - response_content： AI回复
                - model: 模型名称（如 "claude-sonnet-4-5"）
                - ide: IDE 类型（如 "cursor", "claude-code"）

        ## 返回值

        Returns:
            dict: {
                "success": true,
                "session_id": "1c1a4b88-8701-4dc0-b53f-9d5262ac6628",
                "timestamp": "2025-01-07T10:00:00Z",
            }

        ## 注意事项

        - ✅ **每次对话结束时必须调用**
        - ✅ 文件变更场景：sessionId 必须与 beforeEditFile/afterEditFile 保持一致
        - ✅ 必须提供 sessionId 和 metadata
        - ❌ 不要在对话过程中多次调用
        """
        return record_session_impl(session_id, metadata)


    @mcp.tool
    def before_edit_file(
        session_id: str,
        file_paths: List[str]
    ) -> dict:
        """
        在文件内容变更操作前调用，记录变更前的文件状态

        ## 调用时机

        ✅ **文件内容变更操作前**：在执行以下操作**之前立即调用**
        - Write, create_file - 创建新文件
        - Edit, search_replace, edit_file - 修改现有文件
        - delete_file - 删除文件
        - NotebookEdit - 编辑 Jupyter Notebook

        ❌ **不要在以下操作前调用**：
        - Read, read_file - 读取文件（只读操作）
        - Glob, Grep - 搜索文件（只读操作）
        - Bash, shell - 执行命令（非文件操作）

        ## 用途

        记录文件的原始状态（快照），保存到临时文件，供 afterEditFile 对比使用。
        必须与 afterEditFile 成对出现。

        ## 参数

        Args:
            session_id: 会话 ID（必填，示例：1c1a4b88-8701-4dc0-b53f-9d5262ac6628，整个对话开始时应确定一个统一的sessionId，并在所有后续对话轮次操作中保持该ID不变）
            file_paths: 即将变更的文件**绝对路径**列表
                ⚠️ 必须使用绝对路径，如 ["/home/user/project/src/main.py", "/home/user/project/src/utils.py"]
                ❌ 不要使用相对路径，如 ["src/main.py"]

        ## 返回值

        Returns:
            dict: {
                "success": true,
                "session_id": "session-123",
                "timestamp": "2025-01-07T10:00:00Z",
                "files_snapshot": {
                    "/absolute/path/to/file1.py": {
                        "exists": true,
                        "line_count": 100,
                        "size": 2048
                    }
                }
            }
        ```

        ## 注意事项
        - ✅ 必须在文件变更操作**之前**调用
        - ✅ 必须使用绝对路径
        - ❌ 不要对只读操作调用
        - ❌ 不要使用相对路径
        """
        return before_edit_file_impl(session_id, file_paths)


    @mcp.tool
    def after_edit_file(
        session_id: str,
        file_paths: List[str],
        metadata: dict = None
    ) -> dict:
        """
        在文件内容变更操作后调用，记录变更后的文件状态

        ## 调用时机

        ✅ **文件内容变更操作后**：在文件变更完成**之后立即调用**

        必须在对应的 beforeEditFile 调用之后执行，两者必须成对出现。

        ## 用途

        1. 读取文件变更后的内容
        2. 从临时文件加载变更前的内容
        3. 计算变更差异（在服务端进行）
        4. 上传到 DevLake API
        5. 清理临时文件

        ## 参数

        Args:
            session_id: 会话唯一标识（⚠️ 必须与 beforeEditFile 的 sessionId 一致）
            file_paths: 已变更的文件**绝对路径**列表
                ⚠️ 必须与 beforeEditFile 的 filePaths 完全一致
                ⚠️ 必须使用绝对路径
            metadata: 会话元数据（可选），支持字段：
                - ide: IDE 类型（如 "cursor", "claude-code"）
                - model: 模型名称（如 "claude-sonnet-4-5"）

        ## 返回值

        Returns:
            dict: {
                "success": true,
                "session_id": "session-123",
                "timestamp": "2025-01-07T10:01:00Z",
                "uploaded_count": 2,
                "changes": [
                    {
                        "file_path": "src/main.py",  # 相对路径（相对于 git root）
                        "change_type": "edit",       # "create", "edit", "delete"
                        "file_type": "py"
                    },
                    {
                        "file_path": "src/utils.js",
                        "change_type": "create",
                        "file_type": "js"
                    }
                ]
            }


        ## 注意事项

        - ✅ 必须在文件变更操作**之后**调用
        - ✅ 必须与 beforeEditFile 成对出现
        - ✅ sessionId 必须与 beforeEditFile 一致
        - ✅ filePaths 必须与 beforeEditFile 完全一致
        - ✅ 必须使用绝对路径
        - ✅ **建议传递 metadata**（包含 ide 和 model 信息）
        - ❌ 不要在 beforeEditFile 之前调用
        - ❌ 不要使用不同的 sessionId
        - ❌ 不要使用不同的 filePaths
        """
        return after_edit_file_impl(session_id, file_paths, metadata)


def main():
    """
    启动 MCP 服务器

    使用 stdio 传输协议，适合与 Claude Desktop 等客户端集成。

    注意：MCP Server 需要 Python 3.10+ 和 fastmcp 包。
    """
    # 检查 MCP 是否可用
    if not MCP_AVAILABLE:
        print("\n" + "=" * 60, file=sys.stderr)
        print("DevLake MCP Server - 启动失败", file=sys.stderr)
        print("=" * 60, file=sys.stderr)

        # 显示警告信息
        warnings = get_compatibility_warnings()
        for warning in warnings:
            print(warning, file=sys.stderr)

        print("\n可用功能:", file=sys.stderr)
        print("  - Hooks 模式: ✓ 可用（适用于 Claude Code/Cursor hooks）", file=sys.stderr)
        print("  - MCP Server: ✗ 不可用", file=sys.stderr)

        if not HAS_MCP_SUPPORT:
            print("\n推荐操作: 升级到 Python 3.10+ 以使用 MCP Server", file=sys.stderr)
        else:
            print("\n推荐操作: pip install 'devlake-mcp[mcp]'", file=sys.stderr)

        print("=" * 60, file=sys.stderr)
        sys.exit(1)

    # 配置日志（读取环境变量）
    configure_logging()

    print("✓ MCP Server 启动成功 (FastMCP)", file=sys.stderr)
    mcp.run()  # 默认使用 stdio transport


if __name__ == "__main__":
    main()
