"""
plainsuite.py - Plain Test Suite Implementation

This module provides the PlainTestsuite class, which is a basic test suite with plain test support.

普通测试套件实现模块

该模块提供了PlainTestsuite类，这是一个支持普通测试的基本测试套件。
"""

from testlib.base import Testsuite
from testlib.casetypes.testcases import PlainTestCase


class PlainTestsuite(Testsuite):
    """
    Plain test suite implementation.

    This test suite provides basic functionality for running plain tests.
    It supports only the plain test type, which passes if no exception is raised.

    普通测试套件实现

    该测试套件提供了运行普通测试的基本功能。
    它仅支持普通测试类型，即无异常时通过的测试。
    """

    def initialize(self):
        """
        Initialize the plain test suite.

        Registers the PlainTestCase type and sets it as the default test type.

        初始化普通测试套件

        注册PlainTestCase类型并将其设置为默认测试类型。
        """
        self.add("plain")(PlainTestCase)
        self.add.default(PlainTestCase)

    pass
