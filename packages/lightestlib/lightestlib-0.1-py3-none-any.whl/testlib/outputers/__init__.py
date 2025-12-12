"""
outputers/__init__.py - Outputers Module

This module provides the main entry point for different outputers in the testlib framework.
It imports and exports the various outputer implementations.

输出器模块

该模块为testlib框架中的不同输出器提供了主入口点。
它导入并导出各种输出器实现。
"""

from testlib.outputers.stdoutputer import StdOutputer
from testlib.outputers.fileoutputer import FileOutputer

__all__ = [
    "StdOutputer",
    "FileOutputer",
]
