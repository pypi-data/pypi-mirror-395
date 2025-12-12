#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevLake MCP CLI 工具

提供命令行工具，用于初始化项目的 Claude Code 和 Cursor hooks 配置。

命令:
    devlake-mcp init         - 初始化 .claude/settings.json 配置（Claude Code）
    devlake-mcp init-cursor  - 初始化 ~/.cursor/hooks.json 配置（Cursor IDE）
    devlake-mcp --help       - 显示帮助信息
"""

import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

from .constants import get_hook_timeout


def print_help():
    """打印帮助信息"""
    help_text = """
DevLake MCP - AI 编程数据采集工具

用法:
    devlake-mcp <command> [options]

命令:
    init            初始化 Claude Code hooks 配置（默认全局: ~/.claude/settings.json）
    init-cursor     初始化 Cursor hooks 配置（默认全局: ~/.cursor/hooks.json）
    retry           手动触发重试失败的上传记录
    queue-status    查看失败队列状态和统计信息
    queue-clean     清理过期的失败记录
    sync            手动扫描并上传本地 transcript 文件
    clean-cache     备份并清理 Claude Code 缓存目录（projects/shell-snapshots/statsig/todos）
    info            显示详细的版本和功能支持信息
    --help, -h      显示此帮助信息
    --version, -v   显示版本号

选项:
    --force, -f     强制完全覆盖已存在的配置文件（不合并，将丢失现有配置）
    --project       使用项目配置（./.claude/ 或 ./.cursor/）而非全局配置

示例:
    # 全局配置（推荐，所有项目共享）
    devlake-mcp init              # Claude Code 全局配置 (~/.claude/)
                                  # 如已有配置，将智能合并 hooks 部分
    devlake-mcp init-cursor       # Cursor 全局配置 (~/.cursor/)

    # 项目配置（仅当前项目）
    cd your-project
    devlake-mcp init --project           # Claude Code 项目配置 (./.claude/)
    devlake-mcp init-cursor --project    # Cursor 项目配置 (./.cursor/)

    # 强制完全覆盖（不推荐，除非需要重置配置）
    devlake-mcp init --force             # 完全覆盖，丢失现有配置
    devlake-mcp init-cursor --force --project

    # 重试管理
    devlake-mcp retry           # 手动重试失败的上传
    devlake-mcp queue-status    # 查看失败队列状态
    devlake-mcp queue-clean     # 清理过期记录

    # Transcript 同步
    devlake-mcp sync                           # 扫描并上传缺失的 transcript
    devlake-mcp sync --dry-run                 # 预览模式，只扫描不上传
    devlake-mcp sync --force                   # 强制上传，忽略缓存
    devlake-mcp sync --check-server            # 向服务端确认是否存在
    devlake-mcp sync --session-id <id>         # 只同步指定会话

    # 缓存管理
    devlake-mcp clean-cache     # 备份并清理 Claude Code 缓存目录

    # 版本信息
    devlake-mcp --version       # 显示版本号
    devlake-mcp info            # 显示详细版本和功能支持信息

日志位置:
    全局配置: ~/.claude/logs/ 或 ~/.cursor/logs/
    项目配置: .claude/logs/ 或 .cursor/logs/

更多信息请访问: https://github.com/engineering-efficiency/devlake-mcp
"""
    print(help_text)


def print_version():
    """打印简洁的版本号（标准格式）"""
    from devlake_mcp import __version__
    print(f"devlake-mcp {__version__}")


def print_info():
    """打印详细的版本和功能支持信息"""
    from devlake_mcp import __version__
    from devlake_mcp.compat import get_version_info

    info = get_version_info()

    print("=" * 60)
    print("DevLake MCP - 版本信息")
    print("=" * 60)
    print(f"DevLake MCP: v{__version__}")
    print(f"Python: {info['python_version']}")

    # 显示功能状态
    print("\n功能支持:")
    print(f"  - Hooks 模式: {'✓' if info['features']['hooks'] else '✗'}")

    if info['mcp_available']:
        print(f"  - MCP Server: ✓ (FastMCP {info['fastmcp_version']})")
    elif info['mcp_supported']:
        print(f"  - MCP Server: ✗ (未安装 fastmcp)")
    else:
        print(f"  - MCP Server: ✗ (需要 Python 3.10+)")

    # 显示建议
    if info['recommended_action'] != "✓ 所有功能可用":
        print(f"\n建议: {info['recommended_action']}")

    print("=" * 60)


def get_devlake_hooks_config() -> dict:
    """
    获取 DevLake hooks 配置（仅包含 hooks 部分）

    Returns:
        dict: DevLake hooks 配置字典

    Note:
        超时时间通过环境变量 DEVLAKE_HOOK_TIMEOUT 配置（默认 15 秒）
    """
    # 获取动态超时配置
    timeout = get_hook_timeout()

    return {
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 -m devlake_mcp.hooks.stop",
                        "timeout": timeout
                    }
                ]
            }
        ],
        "SubagentStop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 -m devlake_mcp.hooks.stop",
                        "timeout": timeout
                    }
                ]
            }
        ],
        "UserPromptSubmit": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 -m devlake_mcp.hooks.user_prompt_submit",
                        "timeout": timeout
                    }
                ]
            }
        ],
        "PreToolUse": [
            {
                "matcher": "Write|Edit|NotebookEdit",
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 -m devlake_mcp.hooks.pre_tool_use",
                        "timeout": timeout
                    }
                ]
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Write|Edit|NotebookEdit",
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 -m devlake_mcp.hooks.post_tool_use",
                        "timeout": timeout
                    }
                ]
            }
        ],
        "SessionStart": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 -m devlake_mcp.hooks.session_start",
                        "timeout": timeout
                    }
                ]
            }
        ],
        "SessionEnd": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 -m devlake_mcp.hooks.record_session",
                        "timeout": timeout
                    }
                ]
            }
        ]
    }


def get_settings_template() -> dict:
    """
    获取完整的 settings.json 模板（用于全新创建）

    Returns:
        dict: settings.json 配置字典
    """
    return {
        "hooks": get_devlake_hooks_config()
    }


def is_devlake_hook(hook: dict) -> bool:
    """
    检查一个 hook 是否是 DevLake 的 hook

    Args:
        hook: hook 配置字典

    Returns:
        bool: 是否是 DevLake hook
    """
    if hook.get("type") == "command":
        command = hook.get("command", "")
        # 检查是否包含 devlake_mcp.hooks
        return "devlake_mcp.hooks" in command
    return False


def merge_hooks_config(existing_config: dict, devlake_hooks: dict) -> tuple[dict, list[str]]:
    """
    将 DevLake hooks 配置合并到现有配置中

    Args:
        existing_config: 现有的 settings.json 配置
        devlake_hooks: DevLake hooks 配置

    Returns:
        tuple: (合并后的配置, 新增/更新的 hook 事件列表)
    """
    # 创建配置的深拷贝，避免修改原始数据
    import copy
    merged_config = copy.deepcopy(existing_config)

    # 确保有 hooks 字段
    if "hooks" not in merged_config:
        merged_config["hooks"] = {}

    added_or_updated = []

    # 遍历 DevLake 的每个 hook 事件
    for event_name, event_configs in devlake_hooks.items():
        if event_name not in merged_config["hooks"]:
            # 事件不存在，直接添加
            merged_config["hooks"][event_name] = event_configs
            added_or_updated.append(f"{event_name} (新增)")
        else:
            # 事件已存在，需要检查是否已有 DevLake 的 hook
            existing_event_configs = merged_config["hooks"][event_name]

            # 检查现有配置中是否已有 DevLake hook
            has_devlake_hook = False
            for config_block in existing_event_configs:
                if "hooks" in config_block:
                    for hook in config_block["hooks"]:
                        if is_devlake_hook(hook):
                            has_devlake_hook = True
                            break
                if has_devlake_hook:
                    break

            if not has_devlake_hook:
                # 没有 DevLake hook，追加到列表
                # 注意：这里追加整个 event_configs，保持与模板一致
                merged_config["hooks"][event_name].extend(event_configs)
                added_or_updated.append(f"{event_name} (追加)")
            else:
                # 已有 DevLake hook，跳过
                pass

    return merged_config, added_or_updated


def create_settings_file(force: bool = False, global_config: bool = True) -> bool:
    """
    创建或更新 .claude/settings.json 配置文件（智能合并模式）

    Args:
        force: 是否强制覆盖已存在的文件（完全替换，不合并）
        global_config: 是否使用全局配置（True: ~/.claude/settings.json, False: ./.claude/settings.json）

    Returns:
        bool: 是否成功创建或更新
    """
    if global_config:
        claude_dir = Path.home() / ".claude"
    else:
        claude_dir = Path.cwd() / ".claude"

    settings_file = claude_dir / "settings.json"

    # 创建 .claude 目录
    claude_dir.mkdir(parents=True, exist_ok=True)

    # 获取 DevLake hooks 配置
    devlake_hooks = get_devlake_hooks_config()

    # 检查文件是否已存在
    if settings_file.exists():
        if force:
            # force 模式：完全覆盖
            print(f"⚠️  配置文件已存在: {settings_file}")
            response = input("确认完全覆盖（将丢失现有配置）？ [y/N]: ")
            if response.lower() not in ['y', 'yes']:
                print("❌ 已取消")
                return False
            print()

            # 完全覆盖模式
            settings = get_settings_template()
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)

            print(f"✅ 已覆盖配置文件: {settings_file}")
            return True
        else:
            # 智能合并模式
            print(f"📋 检测到现有配置: {settings_file}")
            print("   将采用智能合并模式（保留您的现有配置）")
            print()

            try:
                # 读取现有配置
                with open(settings_file, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)

                # 合并 hooks 配置
                merged_config, added_hooks = merge_hooks_config(existing_config, devlake_hooks)

                if not added_hooks:
                    print("✅ DevLake hooks 已全部配置，无需更新")
                    return True

                # 显示将要添加的 hooks
                print("📝 将要添加/更新的 hooks：")
                for hook_name in added_hooks:
                    print(f"   • {hook_name}")
                print()

                response = input("确认更新配置？ [Y/n]: ")
                if response.lower() in ['n', 'no']:
                    print("❌ 已取消")
                    return False
                print()

                # 写入合并后的配置
                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(merged_config, f, indent=2, ensure_ascii=False)

                print(f"✅ 已更新配置文件: {settings_file}")
                print(f"   新增/更新了 {len(added_hooks)} 个 hook 事件")
                return True

            except json.JSONDecodeError as e:
                print(f"❌ 错误：无法解析现有配置文件: {e}")
                print("   建议使用 --force 选项重新创建配置")
                return False
            except Exception as e:
                print(f"❌ 错误：{e}")
                return False
    else:
        # 文件不存在，创建新文件
        settings = get_settings_template()

        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)

        print(f"✅ 创建配置文件: {settings_file}")
        return True


def init_command(force: bool = False, global_config: bool = True):
    """
    初始化 Claude Code hooks 配置

    Args:
        force: 是否强制覆盖已存在的文件
        global_config: 是否使用全局配置（默认为 True）
    """
    print("\n🚀 开始初始化 DevLake MCP hooks 配置（Claude Code）...\n")

    config_scope = "全局配置" if global_config else "项目配置"
    print(f"📌 配置范围：{config_scope}")
    print()

    # 1. 如果是项目配置，检查是否在 Git 仓库中（可选）
    if not global_config and not Path(".git").exists():
        print("⚠️  警告：当前目录不是 Git 仓库，建议在项目根目录执行此命令。")
        response = input("是否继续？ [y/N]: ")
        if response.lower() not in ['y', 'yes']:
            print("❌ 已取消")
            sys.exit(0)
        print()

    # 2. 创建 settings.json 文件
    success = create_settings_file(force, global_config)

    if not success:
        sys.exit(0)

    # 3. 显示完成信息
    print(f"\n✨ 初始化完成！")

    # 4. 显示下一步提示
    print("\n📝 下一步：")
    if global_config:
        print("   1. 重启 Claude Code")
        print("   2. 配置日志级别（可选）：")
        print("      export DEVLAKE_MCP_LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR")
        print()
        print("   3. 日志位置：~/.claude/logs/")
    else:
        print("   1. 配置 Git 用户信息（如果未配置）：")
        print("      git config user.email 'your-email@example.com'")
        print("      git config user.name 'Your Name'")
        print()
        print("   2. 配置 Git 远程仓库（如果未配置）：")
        print("      git remote add origin <repository-url>")
        print()
        print("   3. 日志位置：.claude/logs/")
    print()
    print("   开始使用 Claude Code，hooks 会自动工作！")
    print()


def get_cursor_hooks_template() -> dict:
    """
    获取 Cursor hooks.json 模板

    Returns:
        dict: hooks.json 配置字典
    """
    return {
        "version": 1,
        "hooks": {
            "beforeSubmitPrompt": [
                {
                    "command": "python3 -m devlake_mcp.hooks.cursor.before_submit_prompt"
                }
            ],
            "afterAgentResponse": [
                {
                    "command": "python3 -m devlake_mcp.hooks.cursor.after_agent_response"
                }
            ],
            "beforeReadFile": [
                {
                    "command": "python3 -m devlake_mcp.hooks.cursor.before_read_file"
                }
            ],
            "beforeShellExecution": [
                {
                    "command": "python3 -m devlake_mcp.hooks.cursor.before_shell_execution"
                }
            ],
            "afterShellExecution": [
                {
                    "command": "python3 -m devlake_mcp.hooks.cursor.after_shell_execution"
                }
            ],
            "afterFileEdit": [
                {
                    "command": "python3 -m devlake_mcp.hooks.cursor.after_file_edit"
                }
            ],
            "stop": [
                {
                    "command": "python3 -m devlake_mcp.hooks.cursor.stop_hook"
                }
            ]
        }
    }


def check_python3():
    """检查 Python 3 是否可用"""
    if not shutil.which('python3'):
        print("❌ 错误：未找到 python3，请先安装 Python 3")
        sys.exit(1)
    print("✅ Python 3 已安装")


def check_devlake_mcp_installed():
    """检查 devlake-mcp 模块是否已安装"""
    try:
        import devlake_mcp
        print("✅ devlake-mcp 模块已安装")
        return True
    except ImportError:
        print("❌ 错误：devlake-mcp 模块未安装")
        print()
        print("请先安装 devlake-mcp：")
        print("  pipx install devlake-mcp")
        print("  或")
        print("  pip install -e .")
        sys.exit(1)


def check_git_config():
    """检查 Git 配置"""
    try:
        result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
        git_user = result.stdout.strip()

        result = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
        git_email = result.stdout.strip()

        if not git_user or not git_email:
            print()
            print("⚠️  警告：Git 用户信息未配置")
            print("请配置 Git 用户信息：")
            print("  git config --global user.name \"Your Name\"")
            print("  git config --global user.email \"your.email@example.com\"")
            return False

        print(f"✅ Git 配置已设置 ({git_user} <{git_email}>)")
        return True
    except FileNotFoundError:
        print("⚠️  警告：未找到 git 命令")
        return False


def create_cursor_hooks_file(force: bool = False, global_config: bool = True) -> bool:
    """
    创建 Cursor hooks.json 配置文件

    Args:
        force: 是否强制覆盖已存在的文件
        global_config: 是否使用全局配置（True: ~/.cursor/hooks.json, False: ./.cursor/hooks.json）

    Returns:
        bool: 是否成功创建
    """
    if global_config:
        cursor_dir = Path.home() / ".cursor"
    else:
        cursor_dir = Path.cwd() / ".cursor"

    hooks_file = cursor_dir / "hooks.json"

    # 检查文件是否已存在
    if hooks_file.exists() and not force:
        print(f"⚠️  配置文件已存在: {hooks_file}")

        # 备份现有文件
        backup_file = cursor_dir / "hooks.json.backup"
        shutil.copy2(hooks_file, backup_file)
        print(f"✅ 已备份现有配置: {backup_file}")

        response = input("是否覆盖？ [y/N]: ")
        if response.lower() not in ['y', 'yes']:
            print("❌ 已取消")
            return False
        print()

    # 创建 .cursor 目录
    cursor_dir.mkdir(parents=True, exist_ok=True)

    # 获取模板并写入文件
    hooks = get_cursor_hooks_template()

    with open(hooks_file, 'w', encoding='utf-8') as f:
        json.dump(hooks, f, indent=2, ensure_ascii=False)

    print(f"✅ 创建配置文件: {hooks_file}")
    return True


def init_cursor_command(force: bool = False, global_config: bool = True):
    """
    初始化 Cursor hooks 配置

    Args:
        force: 是否强制覆盖已存在的文件
        global_config: 是否使用全局配置（默认为 True）
    """
    print("\n🚀 开始初始化 Cursor hooks 配置...\n")

    config_scope = "全局配置" if global_config else "项目配置"
    print(f"📌 配置范围：{config_scope}")
    print("=" * 60)

    # 1. 检查 Python 3
    check_python3()

    # 2. 检查 devlake-mcp 模块
    check_devlake_mcp_installed()

    # 3. 检查 Git 配置（警告但不阻止）
    check_git_config()

    print("=" * 60)
    print()

    # 4. 创建 hooks.json 文件
    success = create_cursor_hooks_file(force, global_config)

    if not success:
        sys.exit(0)

    # 5. 显示完成信息
    print("\n✨ Cursor hooks 初始化完成！")

    # 6. 显示下一步提示
    print("\n📝 下一步：")
    print("   1. 重启 Cursor IDE")
    print("   2. 在 Cursor 设置中查看 Hooks 选项卡，确认 hooks 已激活")
    print("   3. 配置日志级别（可选）：")
    print("      export DEVLAKE_MCP_LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR")
    print()
    if global_config:
        print("   4. 日志位置：~/.cursor/logs/")
    else:
        print("   4. 日志位置：.cursor/logs/")
    print()
    print("   5. 开始使用 Cursor Agent，hooks 会自动采集数据！")
    print()
    print("📚 详细文档：")
    print("   - 使用指南：CURSOR_HOOKS.md")
    if global_config:
        print("   - 故障排查：查看 ~/.cursor/logs/cursor_*.log")
    else:
        print("   - 故障排查：查看 .cursor/logs/cursor_*.log")
    print()


def retry_command():
    """手动触发重试失败的上传记录"""
    from devlake_mcp.retry_queue import retry_failed_uploads, get_retry_config

    print("\n🔄 开始重试失败的上传记录...\n")

    config = get_retry_config()
    if not config['enabled']:
        print("⚠️  重试功能已禁用（DEVLAKE_RETRY_ENABLED=false）")
        print("   如需启用，请设置环境变量：")
        print("   export DEVLAKE_RETRY_ENABLED=true")
        return

    print(f"配置：")
    print(f"  - 最大重试次数：{config['max_attempts']}")
    print(f"  - 记录保留天数：{config['cleanup_days']}")
    print()

    # 执行重试（不限制数量，显示详细进度）
    stats = retry_failed_uploads(max_parallel=999, verbose=True)

    # 显示结果
    print("\n📊 重试统计：")
    print(f"  - 检查记录数：{stats['checked']}")
    print(f"  - 尝试重试数：{stats['retried']}")
    print(f"  - 重试成功数：{stats['succeeded']} ✅")
    print(f"  - 重试失败数：{stats['failed']} ❌")
    print(f"  - 跳过记录数：{stats['skipped']} ⏭️")
    print()

    if stats['succeeded'] > 0:
        print(f"✨ 成功重试 {stats['succeeded']} 条记录！")
    elif stats['retried'] == 0:
        print("💡 没有需要重试的记录")
    else:
        print("⚠️  部分记录重试失败，将在下次自动重试")


def queue_status_command():
    """查看失败队列状态和统计信息"""
    from devlake_mcp.retry_queue import get_queue_statistics, get_retry_config

    print("\n📊 失败队列状态\n")

    config = get_retry_config()
    stats = get_queue_statistics()

    # 显示配置
    print("⚙️  重试配置：")
    print(f"  - 启用状态：{'✅ 已启用' if config['enabled'] else '❌ 已禁用'}")
    print(f"  - 最大重试次数：{config['max_attempts']}")
    print(f"  - 记录保留天数：{config['cleanup_days']}")
    print(f"  - Hook 触发检查：{'✅ 已启用' if config['check_on_hook'] else '❌ 已禁用'}")
    print()

    # 显示总体统计
    summary = stats['summary']
    print("📈 总体统计：")
    print(f"  - 总记录数：{summary['total']}")
    print(f"  - 待重试数：{summary['pending']}")
    print(f"  - 已达最大重试次数：{summary['max_retried']}")
    print()

    # 显示各队列详情
    if summary['total'] > 0:
        print("📋 队列详情：")
        for queue_type in ['session', 'prompt', 'file_change']:
            queue_stats = stats[queue_type]
            if queue_stats['total'] > 0:
                queue_name = {
                    'session': 'Session 会话',
                    'prompt': 'Prompt 提示',
                    'file_change': '文件变更'
                }[queue_type]
                print(f"  - {queue_name}：总数 {queue_stats['total']}, "
                      f"待重试 {queue_stats['pending']}, "
                      f"已达上限 {queue_stats['max_retried']}")
        print()

    if summary['total'] == 0:
        print("✨ 队列为空，没有失败记录！")
    elif summary['pending'] > 0:
        print(f"💡 提示：有 {summary['pending']} 条记录待重试")
        print("   可运行 'devlake-mcp retry' 手动触发重试")


def queue_clean_command():
    """清理过期的失败记录"""
    from devlake_mcp.retry_queue import cleanup_expired_failures, get_retry_config

    print("\n🧹 清理过期的失败记录...\n")

    config = get_retry_config()
    max_age_hours = config['cleanup_days'] * 24

    print(f"清理条件：")
    print(f"  - 超过 {config['cleanup_days']} 天的记录")
    print(f"  - 已达最大重试次数 ({config['max_attempts']}) 的记录")
    print()

    # 执行清理
    cleaned_count = cleanup_expired_failures(max_age_hours=max_age_hours)

    # 显示结果
    if cleaned_count > 0:
        print(f"✅ 已清理 {cleaned_count} 条过期记录")
    else:
        print("💡 没有需要清理的记录")


def sync_command():
    """手动同步本地 transcript 到服务端"""
    from devlake_mcp.transcript_cache import TranscriptCache
    from devlake_mcp.transcript_scanner import scan_local_transcripts
    from devlake_mcp.client import DevLakeClient

    # 解析参数
    dry_run = '--dry-run' in sys.argv
    force = '--force' in sys.argv
    check_server = '--check-server' in sys.argv
    session_id_filter = None

    # 查找 --session-id 参数
    for i, arg in enumerate(sys.argv):
        if arg == '--session-id' and i + 1 < len(sys.argv):
            session_id_filter = sys.argv[i + 1]
            break

    print("\n" + "=" * 60)
    print("📦 Transcript 同步工具")
    print("=" * 60 + "\n")

    if dry_run:
        print("🔍 预览模式（--dry-run）：只扫描，不上传\n")

    if force:
        print("⚠️  强制模式（--force）：忽略缓存，重新上传\n")

    if check_server:
        print("🌐 服务端检查（--check-server）：向服务端确认是否存在\n")

    if session_id_filter:
        print(f"🎯 只同步指定会话：{session_id_filter}\n")

    print("🔍 扫描本地 transcript 文件...\n")

    # 初始化缓存和客户端
    cache = TranscriptCache()

    try:
        with DevLakeClient() as client:
            # 执行扫描
            report = scan_local_transcripts(
                cache=cache,
                client=client,
                check_server=check_server,
                force=force,
                session_id_filter=session_id_filter,
                dry_run=dry_run,
            )

            # 显示报告
            print(report.get_summary())

            # 缓存统计
            if not dry_run:
                cache_stats = cache.get_stats()
                print(f"📊 缓存统计:")
                print(f"  • 缓存记录数: {cache_stats['total_count']} 个")
                if cache_stats['oldest_entry']:
                    print(f"  • 最早记录: {cache_stats['oldest_entry']['uploaded_at']}")
                if cache_stats['newest_entry']:
                    print(f"  • 最新记录: {cache_stats['newest_entry']['uploaded_at']}")
                print()

            # 成功或失败提示
            if report.uploaded_failed > 0:
                print(f"⚠️  有 {report.uploaded_failed} 个上传失败，已加入重试队列")
                print(f"   使用 'devlake-mcp retry' 命令重试\n")
            elif report.uploaded_success > 0:
                print("✅ 同步完成！\n")
            else:
                print("💡 没有需要同步的 transcript\n")

    except Exception as e:
        print(f"\n❌ 同步失败: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def clean_cache_command():
    """备份并清理 Claude Code 缓存目录"""
    print("\n🧹 备份并清理 Claude Code 缓存目录...\n")

    # 生成时间戳后缀
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 定义需要备份的目录
    claude_home = Path.home() / ".claude"
    directories = [
        "projects",
        "shell-snapshots",
        "statsig",
        "todos"
    ]

    # 检查 .claude 目录是否存在
    if not claude_home.exists():
        print(f"⚠️  Claude Code 配置目录不存在: {claude_home}")
        print("   该命令仅适用于已安装 Claude Code 的系统")
        return

    # 统计
    backed_up_count = 0
    skipped_count = 0

    print("📋 开始备份缓存目录：\n")

    for dir_name in directories:
        source_dir = claude_home / dir_name

        if not source_dir.exists():
            print(f"⏭️  跳过（不存在）: {dir_name}")
            skipped_count += 1
            continue

        # 目标路径：添加时间戳后缀
        target_dir = claude_home / f"{dir_name}-{timestamp}"

        try:
            # 使用 shutil.move 进行重命名
            shutil.move(str(source_dir), str(target_dir))
            print(f"✅ 已备份: {dir_name} → {dir_name}-{timestamp}")
            backed_up_count += 1
        except Exception as e:
            print(f"❌ 备份失败: {dir_name} - {e}")

    # 显示结果
    print(f"\n📊 备份统计：")
    print(f"  • 成功备份: {backed_up_count} 个目录")
    print(f"  • 跳过目录: {skipped_count} 个目录")
    print()

    if backed_up_count > 0:
        print("✨ 清理完成！Claude Code 将在下次启动时重新创建这些目录")
        print(f"   备份位置: {claude_home}/")
        print(f"   备份后缀: -{timestamp}")
        print()
        print("💡 提示：如需恢复备份，可手动将目录重命名回原名称")
    else:
        print("💡 没有需要清理的缓存目录")


def main():
    """CLI 主入口

    无参数运行时启动 MCP 服务器，有参数时执行 CLI 命令。
    """
    # 无参数时启动 MCP 服务器（用于 Claude Desktop 集成）
    if len(sys.argv) < 2:
        from devlake_mcp.server import main as server_main
        server_main()
        return

    command = sys.argv[1]

    # 处理命令
    if command in ['--help', '-h', 'help']:
        print_help()
    elif command in ['--version', '-v', 'version']:
        print_version()
    elif command == 'info':
        print_info()
    elif command == 'init':
        # 检查参数
        force = '--force' in sys.argv or '-f' in sys.argv
        # 默认全局配置,除非明确指定 --project
        global_config = '--project' not in sys.argv
        init_command(force=force, global_config=global_config)
    elif command == 'init-cursor':
        # 检查参数
        force = '--force' in sys.argv or '-f' in sys.argv
        # 默认全局配置,除非明确指定 --project
        global_config = '--project' not in sys.argv
        init_cursor_command(force=force, global_config=global_config)
    elif command == 'retry':
        retry_command()
    elif command == 'queue-status':
        queue_status_command()
    elif command == 'queue-clean':
        queue_clean_command()
    elif command == 'sync':
        sync_command()
    elif command == 'clean-cache':
        clean_cache_command()
    else:
        print(f"❌ 错误：未知命令: {command}")
        print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
