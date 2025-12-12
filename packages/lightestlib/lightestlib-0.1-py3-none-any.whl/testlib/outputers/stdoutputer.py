"""
stdoutputer.py - Standard Outputer Implementation

This module provides the StdOutputer class, which outputs messages to the standard output (console).

标准输出器实现模块

该模块提供了StdOutputer类，用于将消息输出到标准输出（控制台）。
"""

import sys
from testlib.base import TestOutputer
from typing import Optional


class StdOutputer(TestOutputer):
    """
    Standard outputer implementation.

    This outputer writes messages to the standard output (console).
    It can optionally flush the output buffer after each write.

    标准输出器实现

    该输出器将消息写入标准输出（控制台）。
    它可以在每次写入后可选地刷新输出缓冲区。
    """

    def __init__(self, mode: Optional[str] = None):
        """
        Initialize a standard outputer.

        Args:
            mode (str, optional): Output mode. Use "flush" to flush the output buffer after each write.

        初始化标准输出器

        参数:
            mode (str, optional): 输出模式。使用"flush"在每次写入后刷新输出缓冲区。
        """
        self.style = "stdout"
        self.original_stdout = sys.stdout
        match mode:
            case "flush":
                self.mode = mode

                def output(message: str) -> bool | None:
                    self.original_stdout.write(message)
                    if self.mode is not None:
                        self.original_stdout.flush()
                    return True
            case _:
                self.mode = None

                def output(message: str) -> bool | None:
                    self.original_stdout.write(message)
                    return True

        self.output = output
