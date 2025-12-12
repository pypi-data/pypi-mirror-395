"""
logformatter.py - Log Message Formatter Implementation

This module provides the LogMessageFormatter class, which formats messages in a log style.

日志消息格式化器实现模块

该模块提供了LogMessageFormatter类，以日志样式格式化消息。
"""

from testlib.base import TestMessageFormatter, TestMessageType, TestMessage


class LogMessageFormatter(TestMessageFormatter):
    """
    Log-style message formatter.

    This formatter formats messages in a log style, with options for development and production modes.
    In development mode, detailed information is included. In production mode, only essential information is shown.

    日志样式消息格式化器

    该格式化器以日志样式格式化消息，提供开发和生产模式选项。
    在开发模式下，包含详细信息。在生产模式下，仅显示基本信息。
    """

    def __init__(self, mode: str = "prod"):
        """
        Initialize a log message formatter.

        Args:
            mode (str): Formatter mode. "dev" for development (detailed), "prod" for production (essential).

        初始化日志消息格式化器

        参数:
            mode (str): 格式化器模式。"dev"表示开发模式（详细），"prod"表示生产模式（基本信息）。
        """
        self.mode = mode
        self.style = "log"
        match mode:
            case "dev":
                self.format = _format_dev
            case "prod":
                self.format = _format_prod
            case _:
                raise ValueError("Invalid mode")
        super().__init__()


def _format_dev(message: TestMessage) -> str:
    """
    Format a message in development mode.

    Includes timestamp, message type, content, and all details.

    以开发模式格式化消息

    包含时间戳、消息类型、内容和所有详细信息。

    Args:
        message (TestMessage): The message to format.

    Returns:
        str: The formatted message string.

    参数:
        message (TestMessage): 要格式化的消息

    返回:
        str: 格式化后的消息字符串
    """
    s = [f"{message.timestamp} [{message.type}] {message.content} "]
    if message.details:
        details_str = " ".join(
            f"| {key}: {value}" for key, value in message.details.items()
        )
        s.append(details_str)
    s.append("\n")
    return "".join(s)


def _format_prod(message: TestMessage) -> str:
    """
    Format a message in production mode.

    Includes timestamp, message type, and content. Debug messages are suppressed.

    以生产模式格式化消息

    包含时间戳、消息类型和内容。调试消息会被抑制。

    Args:
        message (TestMessage): The message to format.

    Returns:
        str: The formatted message string, or empty string for debug messages.

    参数:
        message (TestMessage): 要格式化的消息

    返回:
        str: 格式化后的消息字符串，调试消息返回空字符串
    """
    match message.type:
        case TestMessageType.DEBUG:
            return ""
        case _:
            s = [f"{message.timestamp} [{message.type}] {message.content} "]
            s.append("\n")
            return "".join(s)
