"""
casetypes/__init__.py - Test Case Types Module

This module provides the main entry point for different types of test cases in the testlib framework.
It imports and exports the various test case implementations.

测试用例类型模块

该模块为testlib框架中的不同类型测试用例提供了主入口点。
它导入并导出各种测试用例实现。
"""

import testlib.casetypes.testcases as testcases
import testlib.casetypes.testcasevars as testcasevars

__all__ = [
    "testcases",
    "testcasevars",
]
