#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PreToolUse Hook - 在工具执行前记录文件内容

功能：
1. 拦截 Write/Edit/NotebookEdit 工具
2. 读取文件的完整内容（before_content）
3. 保存到临时文件，供 PostToolUse 使用

注意：此 hook 不使用异步执行，因为必须在工具执行前完成文件内容的保存
"""

import json
import logging
import sys
import os
from pathlib import Path
from datetime import datetime

# 导入公共工具（使用包导入）
from devlake_mcp.utils import get_temp_file_path
from devlake_mcp.logging_config import configure_logging, get_log_dir
from devlake_mcp.constants import HOOK_LOG_DIR
from devlake_mcp.hooks.transcript_utils import safe_parse_hook_input

# 配置日志（启动时调用一次）
configure_logging(log_dir=get_log_dir(HOOK_LOG_DIR), log_file='pre_tool_use.log')
logger = logging.getLogger(__name__)


def save_before_content(session_id: str, file_path: str, content: str):
    """
    保存文件的 before_content 到临时文件

    Args:
        session_id: 会话ID
        file_path: 文件路径
        content: 文件内容
    """
    temp_file = get_temp_file_path(session_id, file_path)

    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            # 保存为 JSON 格式，包含元数据
            data = {
                'file_path': file_path,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            json.dump(data, f)
    except Exception:
        # 静默失败
        pass


def main():
    """
    PreToolUse Hook 主逻辑

    注意：所有异常都被捕获并静默处理，确保不阻塞 Claude
    """
    try:
        # 读取 Hook 输入（使用安全解析函数）
        input_data = safe_parse_hook_input(logger)
        if not input_data:
            return  # 解析失败，跳过处理

        tool_name = input_data.get('tool_name')
        tool_input = input_data.get('tool_input', {})
        session_id = input_data.get('session_id')

        # 只处理文件修改工具
        if tool_name not in ['Write', 'Edit', 'NotebookEdit']:
            return

        # 获取文件路径
        file_path = tool_input.get('file_path')
        if not file_path:
            logger.debug(f'工具 {tool_name} 没有 file_path，跳过')
            return

        # 转换为绝对路径
        if not os.path.isabs(file_path):
            cwd = input_data.get('cwd', os.getcwd())
            file_path = os.path.join(cwd, file_path)

        logger.debug(f'PreToolUse Hook 触发 - tool: {tool_name}, file: {file_path}')

        # 读取文件当前内容（before_content）
        before_content = ''

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    before_content = f.read()
                logger.debug(f'成功读取文件内容 - 长度: {len(before_content)} 字符')
            except Exception as e:
                # 读取失败（如二进制文件），跳过
                logger.warning(f'读取文件失败（可能是二进制文件）: {e}')
                return
        else:
            logger.debug('文件不存在（新建文件）')

        # 保存到临时文件
        save_before_content(session_id, file_path, before_content)
        logger.info(f'成功保存 before_content: {file_path}')

    except Exception as e:
        # 任何异常都静默失败，不影响 AI 执行
        logger.error(f'PreToolUse Hook 执行失败: {e}', exc_info=True)


if __name__ == '__main__':
    main()
    sys.exit(0)  # 唯一的 exit 点
