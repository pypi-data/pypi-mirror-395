"""
assertsuit.py - Assert Test Suite Implementation

This module provides the AssertTestsuite class, which is an advanced test suite with multiple test types support.

断言测试套件实现模块

该模块提供了AssertTestsuite类，这是一个支持多种测试类型的高级测试套件。
"""

from testlib.base import Testsuite
from testlib.casetypes.testcases import PlainTestCase
from testlib.casetypes.testcasevars import (
    ResultTestCaseVar,
    ExceptionTestCaseVar,
    OutputTestCaseVar,
)


class AssertTestsuite(Testsuite):
    """
    Assert test suite implementation.

    This test suite provides advanced functionality with support for multiple test types:
    plain, result, exception, and output tests.

    断言测试套件实现

    该测试套件提供了高级功能，支持多种测试类型：
    普通测试、结果测试、异常测试和输出测试。
    """

    def initialize(self):
        """
        Initialize the assert test suite.

        Registers all supported test types and sets PlainTestCase as the default test type.

        初始化断言测试套件

        注册所有支持的测试类型，并将PlainTestCase设置为默认测试类型。
        """
        self.add("plain")(PlainTestCase)
        self.add.default(PlainTestCase)
        self.add("result")(ResultTestCaseVar)
        self.add("exception")(ExceptionTestCaseVar)
        self.add("output")(OutputTestCaseVar)
