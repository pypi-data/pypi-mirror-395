"""
fileoutputer.py - File Outputer Implementation

This module provides the FileOutputer class, which outputs messages to a file.

文件输出器实现模块

该模块提供了FileOutputer类，用于将消息输出到文件。
"""

from testlib.base import TestOutputer
from datetime import datetime
from typing import Optional
from pathlib import Path


class FileOutputer(TestOutputer):
    """
    File outputer implementation.

    This outputer writes messages to a file. It supports both append and write modes.

    文件输出器实现

    该输出器将消息写入文件。它支持追加和写入模式。
    """

    style = "file"

    def __init__(self, path: Optional[str] = None, mode: Optional[str] = "a"):
        """
        Initialize a file outputer.

        Args:
            path (str, optional): Path to the output file. If None, a default path with timestamp is used.
            mode (str, optional): File open mode. "a" for append (default), "w" for write/overwrite.

        初始化文件输出器

        参数:
            path (str, optional): 输出文件的路径。如果为None，则使用带有时间戳的默认路径。
            mode (str, optional): 文件打开模式。"a"表示追加（默认），"w"表示写入/覆盖。
        """
        if mode not in ["a", "w"]:  # pragma: no cover
            raise ValueError("mode must be 'a' or 'w'")
        self.mode = mode
        if path is None:
            formatted_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = f"./log/{formatted_time} test.log"

        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def output(self, message: str) -> bool | None:
        """
        Output a message to the file.

        Args:
            message (str): The message to output.

        Returns:
            bool | None: True if output was successful.

        将消息输出到文件

        参数:
            message (str): 要输出的消息

        返回:
            bool | None: 如果输出成功则返回True
        """
        if self.mode is None:  # pragma: no cover
            self.mode = "a"
        with open(file=self.path, mode=self.mode) as f:
            f.write(message)
        return True
