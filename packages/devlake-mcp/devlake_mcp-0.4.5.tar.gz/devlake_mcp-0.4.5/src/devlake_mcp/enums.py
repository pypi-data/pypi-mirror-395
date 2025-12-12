#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
枚举类型定义模块

提供项目中使用的所有枚举类型
"""

from enum import Enum


class IDEType(str, Enum):
    """
    支持的 IDE 类型枚举

    继承 str 以便：
    1. 直接用于字符串比较和拼接
    2. JSON 序列化时自动转换为字符串
    3. 向后兼容现有字符串参数

    使用示例：
        # 作为参数
        start_generation(session_id, ide_type=IDEType.CLAUDE_CODE)

        # 字符串比较
        if ide_type == IDEType.CLAUDE_CODE:
            ...

        # 获取字符串值
        ide_type.value  # 'claude_code'

        # 从字符串创建
        IDEType('claude_code')  # IDEType.CLAUDE_CODE
    """
    CLAUDE_CODE = 'claude_code'  # Anthropic Claude Code
    CURSOR = 'cursor'            # Cursor AI IDE
    QODER = 'qoder'              # Qoder IDE (未来支持)
    UNKNOWN = 'unknown'          # 未知或不支持的 IDE

    @classmethod
    def from_string(cls, value: str) -> 'IDEType':
        """
        从字符串创建枚举（安全转换）

        Args:
            value: IDE 类型字符串

        Returns:
            对应的 IDEType 枚举值，无效值返回 UNKNOWN

        示例：
            IDEType.from_string('claude_code')  # IDEType.CLAUDE_CODE
            IDEType.from_string('invalid')      # IDEType.UNKNOWN
        """
        try:
            return cls(value.lower())
        except (ValueError, AttributeError):
            return cls.UNKNOWN
