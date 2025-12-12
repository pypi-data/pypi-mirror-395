"""
testmessageformatter.py - Test Message Formatter Base Class

This module provides the base TestMessageFormatter class for formatting test messages.

测试消息格式化器模块

该模块提供了格式化测试消息的基类TestMessageFormatter。
"""

from .testmessage import TestMessage
from typing import Optional


class TestMessageFormatter:
    """
    Base class for test message formatters.

    This class provides the foundation for all message formatters in the testlib framework.
    Formatters are responsible for converting TestMessage objects into formatted strings.

    测试消息格式化器基类

    该类为testlib框架中的所有消息格式化程序提供了基础。
    格式化器负责将TestMessage对象转换为格式化的字符串。
    """

    style: str
    mode: Optional[str]

    def __init__(self):
        """
        Initialize a TestMessageFormatter instance.

        初始化TestMessageFormatter实例。
        """
        pass

    def __call__(self, message: TestMessage) -> str:
        """
        Make the formatter callable to format messages.

        Args:
            message (TestMessage): The message to format.

        Returns:
            str: The formatted message string.

        使格式化器可调用以格式化消息。

        参数:
            message (TestMessage): 要格式化的消息。

        返回:
            str: 格式化后的消息字符串。
        """
        return self.format(message)

    def format(self, message: TestMessage) -> str:
        """
        Format a message. This method should be implemented by subclasses.

        Args:
            message (TestMessage): The message to format.

        Returns:
            str: The formatted message string.

        格式化消息。此方法应由子类实现。

        参数:
            message (TestMessage): 要格式化的消息。

        返回:
            str: 格式化后的消息字符串。
        """
        return ""

    def __repr__(self) -> str:
        """
        Get string representation of the formatter.

        Returns:
            str: String representation of the formatter.

        获取格式化器的字符串表示。

        返回:
            str: 格式化器的字符串表示。
        """
        if self.mode:
            return f"<{self.style} TestMessageFormatter in {self.mode} mode>"
        return f"<{self.style} TestMessageFormatter>"
