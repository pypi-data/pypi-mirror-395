"""
testcasevars/__init__.py - Test Case Variables Module

This module provides implementations of different parameterized test case types.
Includes ResultTestCaseVar, ExceptionTestCaseVar, and OutputTestCaseVar.

泛测试用例变量模块

该模块提供了不同参数化测试用例类型的实现。
包括ResultTestCaseVar、ExceptionTestCaseVar和OutputTestCaseVar。
"""

from testlib.casetypes.testcasevars.result import ResultTestCaseVar
from testlib.casetypes.testcasevars.exception import ExceptionTestCaseVar
from testlib.casetypes.testcasevars.output import OutputTestCaseVar

__all__ = ["ResultTestCaseVar", "ExceptionTestCaseVar", "OutputTestCaseVar"]
