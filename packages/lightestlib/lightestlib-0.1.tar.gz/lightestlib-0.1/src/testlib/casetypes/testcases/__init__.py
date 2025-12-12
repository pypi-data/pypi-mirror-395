"""
testcases/__init__.py - Test Cases Module

This module provides implementations of different test case types.
Currently includes PlainTestCase for basic test execution.

测试用例模块

该模块提供了不同测试用例类型的实现。
目前包括用于基本测试执行的PlainTestCase。
"""

from testlib.casetypes.testcases.plain import PlainTestCase

__all__ = [
    "PlainTestCase",
]
