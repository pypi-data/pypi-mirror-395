# DevLake MCP

[![PyPI version](https://img.shields.io/pypi/v/devlake-mcp.svg)](https://pypi.org/project/devlake-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/devlake-mcp.svg)](https://pypi.org/project/devlake-mcp/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

DevLake MCP 是一个 **AI 编程数据采集工具**，用于统计 **AI 出码率**和研发效率指标。支持两种工作模式：

- **🔌 Hooks 模式**（推荐）- 通过 IDE Hooks 自动采集 AI 编程数据，零感知、零配置
- **🤖 MCP 模式** - 作为 MCP 服务器，让 AI 助手主动调用工具记录数据

## ✨ 核心特性

- **🎯 自动采集** - 无需手动操作，IDE Hooks 自动记录 AI 编程数据
- **📊 AI 出码率统计** - 精确计算 AI 生成代码在最终提交中的占比
- **🔄 智能重试** - 失败请求自动重试，指数退避策略，数据不丢失
- **🚀 异步执行** - 后台运行，不阻塞 IDE 操作
- **🔧 双模式支持** - Hooks（自动）+ MCP（主动调用）
- **🌐 跨 IDE 支持** - Claude Code、Cursor、Claude Desktop 等

## Python 版本要求

| Python 版本 | Hooks 模式 | MCP Server 模式 |
|------------|-----------|----------------|
| 3.9.x      | ✅ 支持   | ❌ 不支持      |
| 3.10+      | ✅ 支持   | ✅ 支持        |

**推荐使用 Python 3.10 或更高版本以获得完整功能支持。**

## 📦 快速安装

### 方式一：基础安装（Python 3.9+，仅 Hooks 模式）

```bash
# 使用 pipx 安装（推荐）
pipx install devlake-mcp

# 或使用 pip
pip install devlake-mcp
```

### 方式二：完整安装（Python 3.10+，Hooks + MCP Server）

```bash
# 使用 pipx 安装（推荐）
pipx install "devlake-mcp[mcp]"

# 或使用 pip
pip install "devlake-mcp[mcp]"
```

### 检查安装

```bash
# 查看版本号
devlake-mcp --version
# 输出: devlake-mcp 0.3.4

# 查看详细的版本和功能支持状态
devlake-mcp info
```

`devlake-mcp info` 输出示例：
```
============================================================
DevLake MCP - 版本信息
============================================================
DevLake MCP: v0.3.4
Python: 3.10.19

功能支持:
  - Hooks 模式: ✓
  - MCP Server: ✓ (FastMCP 2.13.0.2)
============================================================
```

## ⚙️ 环境配置

<details>
<summary>点击展开详细配置选项</summary>

```bash
# ============================================================
# API 配置（可选）
# ============================================================
# DevLake API 地址（默认使用测试环境）
export DEVLAKE_BASE_URL="http://devlake.test.chinawayltd.com"

# API 请求超时时间（秒，默认 7 秒）
export DEVLAKE_TIMEOUT=7

# HTTP 请求失败后自动重试次数（默认 1 次）
export DEVLAKE_HTTP_RETRY_COUNT=1

# ============================================================
# Hooks 配置（可选）
# ============================================================
# Hook 执行超时时间（秒，默认 15 秒）
# 所有 hooks (SessionStart, Stop, UserPromptSubmit 等) 统一使用此超时值
export DEVLAKE_HOOK_TIMEOUT=15

# ============================================================
# Git 配置（必需）
# ============================================================
# 确保 Git 配置正确
git config user.name "Your Name"
git config user.email "your.email@example.com"

# ============================================================
# 日志配置（可选）
# ============================================================
export DEVLAKE_MCP_LOGGING_ENABLED=true  # 是否启用日志（默认 true）
export DEVLAKE_MCP_LOG_LEVEL=INFO        # 日志级别：DEBUG/INFO/WARNING/ERROR/CRITICAL（默认 INFO）
export DEVLAKE_MCP_CONSOLE_LOG=false     # 是否输出到控制台（默认 false，仅开发调试时启用）

# ============================================================
# 重试配置（可选）
# ============================================================
export DEVLAKE_RETRY_ENABLED=true           # 启用/禁用重试（默认 true）
export DEVLAKE_RETRY_MAX_ATTEMPTS=5         # 最大重试次数（默认 5）
export DEVLAKE_RETRY_CLEANUP_DAYS=7         # 失败记录保留天数（默认 7）
export DEVLAKE_RETRY_CHECK_ON_HOOK=true     # Hook 执行时自动检查重试（默认 true）
```

</details>

---

## 🔌 模式一：Hooks 自动采集（推荐）

Hooks 模式通过 IDE 的 Hooks 机制**自动**采集 AI 编程数据，无需 AI 主动调用工具，适合日常开发使用。

### Claude Code Hooks

#### 一键初始化

```bash
# 自动配置 .claude/settings.json
# 如果已有配置，将智能合并 hooks 部分（保留您的现有配置）
devlake-mcp init

# 强制完全覆盖已有配置（不推荐，将丢失现有配置）
devlake-mcp init --force
```

**智能合并说明**：
- ✅ 自动检测现有 settings.json 配置
- ✅ 仅添加或更新 `hooks` 部分
- ✅ 完全保留您的其他配置（如 `mcpServers`、`permissions`、`statusLine` 等）
- ✅ 如果 DevLake hooks 已配置，则跳过无需更新
- ⚠️  使用 `--force` 选项会完全覆盖配置文件，谨慎使用

#### 支持的 Hooks

| Hook | 触发时机 | 功能 |
|------|---------|------|
| **SessionStart** | 会话启动 | 创建 session 记录 |
| **UserPromptSubmit** | 用户提交 prompt | 记录用户输入 |
| **PreToolUse** | 工具使用前 | 记录文件变更前状态 |
| **PostToolUse** | 工具使用后 | 上传文件变更（diff） |
| **Stop** | AI 循环停止 | 更新会话统计 |
| **SessionEnd** | 会话结束 | 上传完整会话数据 |

#### 技术特点

- ✅ 使用 Claude Code 原生 `session_id`，无需额外管理
- ✅ 自动检测会话切换和超时（30 分钟）
- ✅ 异步上传，不阻塞 IDE 操作
- ✅ 失败自动加入重试队列

#### 配置示例

初始化后会在 `.claude/settings.json` 中生成以下配置：

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "python3 -m devlake_mcp.hooks.session_start",
        "timeout": 5
      }]
    }],
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "python3 -m devlake_mcp.hooks.user_prompt_submit",
        "timeout": 5
      }]
    }],
    "PreToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "python3 -m devlake_mcp.hooks.pre_tool_use",
        "timeout": 5
      }]
    }],
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "python3 -m devlake_mcp.hooks.post_tool_use",
        "timeout": 10
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python3 -m devlake_mcp.hooks.stop",
        "timeout": 5
      }]
    }],
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "python3 -m devlake_mcp.hooks.session_end",
        "timeout": 10
      }]
    }]
  }
}
```

---

### Cursor Hooks

#### 一键初始化

```bash
# 自动配置 Cursor hooks
devlake-mcp init-cursor

# 强制覆盖已有配置
devlake-mcp init-cursor --force
```

#### 支持的 Hooks

| Hook | 触发时机 | 功能 |
|------|---------|------|
| **beforeSubmitPrompt** | 用户提交 prompt 前 | 记录用户输入 |
| **beforeReadFile** | 读取文件前 | 记录文件访问 |
| **beforeShellExecution** | 执行 Shell 前 | 记录命令信息 |
| **afterShellExecution** | Shell 执行后 | 检测命令产生的文件变更 |
| **afterFileEdit** | 文件编辑后 | 上传文件编辑变更 |
| **afterAgentResponse** | AI 回复后 | 记录对话内容 |
| **stop** | 会话结束 | 上传会话统计 |

#### 技术特点

- ✅ 使用 Cursor 原生 `conversation_id` 作为 session_id
- ✅ `generation_id` 关联同一次 AI 生成的多个文件变更
- ✅ 自动检测 vim/nano/echo>/cp/mv 等文件操作命令
- ✅ 智能 diff 算法计算文件变更
- ✅ 与 Claude Code 完全兼容的数据格式
- ✅ 精确的工作目录定位（workspace_roots）

#### 详细文档

查看 [Cursor Hooks 集成文档](docs/integrations/CURSOR_HOOKS.md) 了解完整配置和使用指南。

---

### Hooks 模式对比

| 特性 | Claude Code | Cursor |
|------|-------------|--------|
| Session 管理 | 30分钟超时机制 | 对话生命周期管理 |
| 文件变更追踪 | ✅ | ✅ |
| Shell 命令检测 | ❌ | ✅ |
| 变更关联追踪 | 单个变更 | ✅ generation_id 关联 |
| 工作目录定位 | 手动推断 | ✅ workspace_roots |
| 数据格式 | 原生格式 | 完全兼容 Claude Code |

---

## 🤖 模式二：MCP 服务器模式

MCP 模式将 DevLake 作为 [Model Context Protocol](https://modelcontextprotocol.io) 服务器运行，基于 [FastMCP](https://gofastmcp.com) 框架，让 AI 助手可以**主动调用工具**记录数据。

### 配置方式

#### 方式 1：使用 Claude CLI（推荐）

```bash
claude mcp add devlake-mcp devlake-mcp
```

#### 方式 2：手动配置

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或相应配置文件：

```json
{
  "mcpServers": {
    "devlake-mcp": {
      "command": "devlake-mcp"
    }
  }
}
```

配置完成后重启 Claude Desktop。

### 可用工具

MCP 模式提供 3 个核心工具，AI 助手可以主动调用：

#### 1. `record_session`

**功能**：记录 AI 会话的元数据和统计信息

**参数**：
- `session_id` (string, 可选)：会话 ID，不提供则自动生成 UUID
- `metadata` (dict, 可选)：会话元数据
  - `user_intent`：用户意图描述
  - `model`：模型名称（如 "claude-sonnet-4-5"）
  - `ide`：IDE 类型（如 "cursor", "claude-code"）
  - `project_path`：项目路径

**返回示例**：
```json
{
  "success": true,
  "session_id": "uuid-xxx",
  "timestamp": "2025-01-07T10:00:00Z",
  "git_info": {
    "git_repo_path": "yourorg/devlake",
    "git_branch": "main",
    "git_author": "Your Name"
  }
}
```

**使用示例**：
```
调用 record_session 工具，metadata 设置为 {"ide": "cursor", "model": "claude-sonnet-4-5"}
```

---

#### 2. `before_edit_file`

**功能**：在文件变更前调用，记录文件的当前状态（快照）

**参数**：
- `session_id` (string, 必需)：会话唯一标识
- `file_paths` (list[string], 必需)：即将变更的文件绝对路径列表

**返回示例**：
```json
{
  "success": true,
  "session_id": "session-123",
  "files_snapshot": {
    "/path/to/file.py": {
      "exists": true,
      "line_count": 100,
      "size": 2048
    }
  }
}
```

**使用示例**：
```
调用 before_edit_file 工具，session_id 为 "session-123"，file_paths 为 ["/path/to/file.py"]
```

---

#### 3. `after_edit_file`

**功能**：在文件变更后调用，对比差异并上传变更数据到 DevLake API

**参数**：
- `session_id` (string, 必需)：会话唯一标识（与 before_edit_file 一致）
- `file_paths` (list[string], 必需)：已变更的文件绝对路径列表

**返回示例**：
```json
{
  "success": true,
  "session_id": "session-123",
  "uploaded_count": 1,
  "changes": [
    {
      "file_path": "src/main.py",
      "change_type": "edit",
      "file_type": "py"
    }
  ]
}
```

**工作流程**：
```
1. before_edit_file() - 记录文件变更前状态
2. [AI 执行文件变更操作]
3. after_edit_file() - 对比差异并上传
```

**使用示例**：
```
调用 after_edit_file 工具，session_id 为 "session-123"，file_paths 为 ["/path/to/file.py"]
```

---

### MCP 模式特点

- ✅ **AI 主动控制**：由 AI 决定何时记录数据
- ✅ **精确记录时机**：在最合适的时间点调用工具
- ✅ **完整的 before/after 对比**：准确的文件变更 diff
- ✅ **跨 IDE 支持**：适用于任何支持 MCP 的 AI 助手
- ✅ **手动 Session 管理**：AI 自行管理会话生命周期

---

## 🔄 失败重试机制

DevLake MCP 内置**智能失败重试队列**，确保数据不会因网络问题或临时故障丢失。

### 工作原理

当 API 调用失败时，失败记录自动保存到本地队列（`~/.devlake/retry_queue.json`），按**指数退避策略**自动重试：

| 重试次数 | 等待时间 | 累计时间 |
|---------|---------|---------|
| 第 1 次 | 1 分钟 | 1 分钟 |
| 第 2 次 | 5 分钟 | 6 分钟 |
| 第 3 次 | 15 分钟 | 21 分钟 |
| 第 4 次 | 60 分钟 | 81 分钟 |
| 第 5 次 | 4 小时 | ~5.5 小时 |

**自动重试**：当 `DEVLAKE_RETRY_CHECK_ON_HOOK=true`（默认），每次 Hook 执行时自动检查并重试失败记录（每次最多 3 条，避免阻塞）。

### 队列管理命令

```bash
# 查看失败队列状态和统计
devlake-mcp queue-status

# 手动触发重试（不等待自动重试时间）
devlake-mcp retry

# 清理过期的失败记录（默认保留 7 天）
devlake-mcp queue-clean
```

<details>
<summary>点击查看重试配置选项</summary>

通过环境变量配置重试行为：

```bash
# 启用/禁用重试（默认 true）
export DEVLAKE_RETRY_ENABLED=true

# 最大重试次数（默认 5）
export DEVLAKE_RETRY_MAX_ATTEMPTS=5

# 失败记录保留天数（默认 7）
export DEVLAKE_RETRY_CLEANUP_DAYS=7

# Hook 执行时自动检查重试（默认 true）
export DEVLAKE_RETRY_CHECK_ON_HOOK=true
```

禁用自动重试后，需手动执行 `devlake-mcp retry` 触发重试。

</details>

---

## CLI 命令总览

```bash
# MCP 服务器
devlake-mcp                     # 启动 MCP 服务器

# Hooks 初始化
devlake-mcp init                # 初始化 Claude Code hooks
devlake-mcp init --force        # 强制覆盖 Claude Code hooks
devlake-mcp init-cursor         # 初始化 Cursor hooks
devlake-mcp init-cursor --force # 强制覆盖 Cursor hooks

# 失败队列管理
devlake-mcp queue-status        # 查看失败队列状态
devlake-mcp retry               # 手动触发重试
devlake-mcp queue-clean         # 清理过期记录

# 版本信息
devlake-mcp --version           # 显示版本号
devlake-mcp info                # 显示详细的版本和功能支持信息
devlake-mcp --help              # 显示帮助信息
```

---

## 使用建议

### 选择合适的模式

| 场景 | 推荐模式 | 理由 |
|------|---------|------|
| 日常开发 | **Hooks 模式** | 自动采集，无需关注 |
| 精确控制记录时机 | **MCP 模式** | AI 主动决定何时记录 |
| Claude Code | **Hooks 模式** | 原生集成，体验最佳 |
| Cursor | **Hooks 模式** | 专门优化，功能最全 |
| Claude Desktop | **MCP 模式** | 标准 MCP 协议支持 |

### 两种模式可以共存

Hooks 模式和 MCP 模式可以同时启用：
- Hooks 模式负责自动采集日常数据
- MCP 模式让 AI 在特殊场景下主动记录

---

## 📚 相关文档

### 项目文档

- **[文档中心](docs/README.md)** - 完整的文档索引和导航
- **[架构设计](docs/development/DESIGN.md)** - 完整的架构设计和技术方案
- **[开发指南](docs/development/CLAUDE.md)** - 开发者指南和最佳实践
- **[Cursor 集成](docs/integrations/CURSOR_HOOKS.md)** - Cursor Hooks 详细配置指南
- **[MCP 工具指南](docs/integrations/MCP_TOOLS_USAGE_GUIDE.md)** - MCP 工具调用规范
- **[更新日志](CHANGELOG.md)** - 版本更新记录
- **[贡献指南](CONTRIBUTING.md)** - 如何为项目贡献代码

### 外部资源

- [Model Context Protocol 官方文档](https://modelcontextprotocol.io)
- [FastMCP 官方文档](https://gofastmcp.com)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Claude Desktop](https://claude.ai/download)
- [Cursor 编辑器](https://cursor.sh)

---

## ⚠️ 前置要求

### Git 配置（必需）

工具会自动从 Git 配置读取用户信息，请确保已配置：

```bash
# 配置 Git 用户信息
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 配置仓库远程地址（用于识别项目）
git remote add origin <repository-url>
```

### Python 环境

- Python 3.9+（Hooks 模式）
- Python 3.10+（完整功能，包括 MCP Server）
- 建议使用 `pipx` 进行全局安装

---

## 🐛 故障排查

<details>
<summary>点击查看常见问题解决方案</summary>

### Hook 未执行

1. 检查配置文件：`.claude/settings.json` 或 `.cursor/hooks.json`
2. 查看日志：`tail -f ~/.devlake/logs/devlake_mcp.log`
3. 验证 Python 路径：`which python3`
4. 重新初始化：`devlake-mcp init --force`

### API 调用失败

1. 检查网络：`curl http://devlake.test.chinawayltd.com`
2. 查看重试队列：`devlake-mcp queue-status`
3. 手动重试：`devlake-mcp retry`
4. 检查环境变量：`echo $DEVLAKE_BASE_URL`

### 数据未上传

1. 检查 Git 配置：`git config user.name` 和 `git config user.email`
2. 启用调试日志：`export DEVLAKE_MCP_LOG_LEVEL=DEBUG`
3. 查看完整日志：`cat ~/.devlake/logs/devlake_mcp.log`

### Session ID 混乱

1. 清理状态文件：`rm -rf ~/.devlake/sessions/*`
2. 重启 IDE
3. 重新开始会话

</details>

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

[MIT License](LICENSE)
