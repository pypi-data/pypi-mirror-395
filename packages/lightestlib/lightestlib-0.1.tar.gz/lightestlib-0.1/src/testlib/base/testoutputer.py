"""
testoutputer.py - Test Outputer Base Class

This module provides the base TestOutputer class for creating output handlers.

测试输出器模块

该模块提供了创建输出处理程序的基类TestOutputer。
"""

from typing import Optional


class TestOutputer:
    """
    Base class for test outputers.

    This class provides the foundation for all output handlers in the testlib framework.
    Outputers are responsible for directing test results and messages to various destinations.

    测试输出器基类

    该类为testlib框架中的所有输出处理程序提供了基础。
    输出器负责将测试结果和消息定向到各种目标。
    """

    style: str
    mode: Optional[str]

    def __init__(self):
        """
        Initialize a TestOutputer instance.

        初始化TestOutputer实例。
        """
        pass

    def __call__(self, message: str) -> Optional[bool]:
        """
        Make the outputer callable to output messages.

        Args:
            message (str): The message to output.

        Returns:
            Optional[bool]: True if output was successful, False otherwise.

        使输出器可调用以输出消息。

        参数:
            message (str): 要输出的消息。

        返回:
            Optional[bool]: 如果输出成功则返回True，否则返回False。
        """
        return self.output(message)

    def output(self, message: str) -> Optional[bool]:
        """
        Output a message. This method should be implemented by subclasses.

        Args:
            message (str): The message to output.

        Returns:
            Optional[bool]: True if output was successful, False otherwise.

        输出消息。此方法应由子类实现。

        参数:
            message (str): 要输出的消息。

        返回:
            Optional[bool]: 如果输出成功则返回True，否则返回False。
        """
        pass

    def __repr__(self) -> str:
        """
        Get string representation of the outputer.

        Returns:
            str: String representation of the outputer.

        获取输出器的字符串表示。

        返回:
            str: 输出器的字符串表示。
        """
        if self.mode:
            return f"<{self.style} TestMessageFormatter in {self.mode} mode>"
        return f"<{self.style} TestMessageFormatter>"
