"""
stdformatter.py - Standard Message Formatter Implementation

This module provides the StdMessageFormatter class, which formats messages in a standard style with different verbosity levels.

标准消息格式化器实现模块

该模块提供了StdMessageFormatter类，以具有不同详细级别的标准样式格式化消息。
"""

from testlib.base import TestMessageFormatter, TestMessageType, TestMessage


class StdMessageFormatter(TestMessageFormatter):
    """
    Standard message formatter.

    This formatter provides different verbosity levels: quiet, normal, and detail.
    Each level shows different amounts of information about the test execution.

    标准消息格式化器

    该格式化器提供不同的详细级别：安静、正常和详细。
    每个级别显示关于测试执行的不同数量的信息。
    """

    def __init__(self, mode: str = "quiet"):
        """
        Initialize a standard message formatter.

        Args:
            mode (str): Formatter mode. "quiet" for minimal output, "normal" for standard output, "detail" for detailed output.

        初始化标准消息格式化器

        参数:
            mode (str): 格式化器模式。"quiet"表示最小输出，"normal"表示标准输出，"detail"表示详细输出。
        """
        super().__init__()
        self.style = "std"
        match mode:
            case "quiet":
                self.format = _format_quiet
                self.mode = "quiet"
            case "detail":
                self.format = _format_detail
                self.mode = "detail"
            case "normal":
                self.format = _format_normal
                self.mode = "normal"
            case _:
                raise ValueError("Invalid mode")


def _format_quiet(message: TestMessage) -> str:
    """
    Format a message in quiet mode.

    Shows minimal information, typically just test results as single characters.

    以安静模式格式化消息

    显示最少的信息，通常只将测试结果显示为单个字符。

    Args:
        message (TestMessage): The message to format.

    Returns:
        str: The formatted message string.

    参数:
        message (TestMessage): 要格式化的消息

    返回:
        str: 格式化后的消息字符串
    """
    match message.type:
        case TestMessageType.INFO:
            match message.details.get("status"):
                case "start":
                    return f"{message.details.get('name')} started, {message.details.get('cases')} cases will be tested\n"
                case "end":
                    return f"\n{message.details.get('passed')} passed, {message.details.get('failed')} failed, {message.details.get('skipped')} skipped\n"
                case _:
                    return ""
        case TestMessageType.MESSAGE:
            match message.details.get("status"):
                case True:
                    return "P"
                case False:
                    return "F"
                case None:
                    return "S"
                case _:
                    return ""
        case _:
            return ""
    pass


def _format_normal(message: TestMessage) -> str:
    """
    Format a message in normal mode.

    Shows standard information about test execution, including pass/fail status.

    以正常模式格式化消息

    显示关于测试执行的标准信息，包括通过/失败状态。

    Args:
        message (TestMessage): The message to format.

    Returns:
        str: The formatted message string.

    参数:
        message (TestMessage): 要格式化的消息

    返回:
        str: 格式化后的消息字符串
    """
    match message.type:
        case TestMessageType.INFO:
            match message.details.get("status"):
                case "start":
                    return f"{message.details.get('name')} started\n{message.details.get('cases')} cases will be tested\n"  # type: ignore
                case "end":
                    return f"{message.details.get('passed')} passed, {message.details.get('failed')} failed, {message.details.get('skipped')} skipped\n{message.details.get('name')} ended"
                case _:
                    return ""
        case TestMessageType.MESSAGE:
            match message.details.get("status"):
                case True:
                    return f"{message.details.get('name')} passed\n"
                case False:
                    return f"{message.details.get('name')} failed\n"
                case None:
                    return f"{message.details.get('name')} skipped\n"
                case _:
                    return ""
        case _:
            return ""
    pass


def _format_detail(message: TestMessage) -> str:
    """
    Format a message in detail mode.

    Shows detailed information about test execution, including full messages and content.

    以详细模式格式化消息

    显示关于测试执行的详细信息，包括完整消息和内容。

    Args:
        message (TestMessage): The message to format.

    Returns:
        str: The formatted message string.

    参数:
        message (TestMessage): 要格式化的消息

    返回:
        str: 格式化后的消息字符串
    """
    match message.type:
        case TestMessageType.INFO:
            match message.details.get("status"):
                case "start":
                    return f"{message.details.get('name')} started\n{message.details.get('cases')} cases will be tested\n"  # type: ignore
                case "end":
                    return f"{message.details.get('passed')} passed, {message.details.get('failed')} failed, {message.details.get('skipped')} skipped\n{message.details.get('name')} ended"
                case _:
                    return ""
        case TestMessageType.MESSAGE:
            match message.details.get("status"):
                case True:
                    return f"{message.details.get('name')} :{message.content}\n"
                case False:
                    return f"{message.details.get('name')} :{message.content}\n"
                case None:
                    return f"{message.details.get('name')} :{message.content}\n"
                case _:
                    return ""
        case _:
            return ""
    pass
