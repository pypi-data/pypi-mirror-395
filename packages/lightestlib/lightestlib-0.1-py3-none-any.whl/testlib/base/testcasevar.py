"""
testcasevar.py - Test Case Variable Base Class

This module provides the base TestcaseVar class for creating parameterized test cases.

泛测试用例模块

该模块提供了创建参数化测试用例的基类TestcaseVar。
"""

from .testcase import TestCase
from typing import Callable
from testlib.base.testmessage import TestMessageType


class TestcaseVar(object):
    """
    Base class for test case variables.

    This class provides functionality for creating parameterized test cases,
    allowing tests to be generated with different parameters.

    测试用例变量基类

    该类提供了创建参数化测试用例的功能，
    允许生成具有不同参数的测试。
    """

    style = ""

    def __init__(self, suit=None):
        """
        Initialize a TestcaseVar instance.

        Args:
            suit (Testsuite, optional): The test suite this test case variable belongs to.

        初始化TestcaseVar实例。

        参数:
            suit (Testsuite, optional): 此测试用例变量所属的测试套件。
        """
        self.suit = suit

    def __call__(self, *args, **kwargs) -> Callable:
        """
        Make the test case variable callable to generate test cases.

        Args:
            *args: Positional arguments for test case generation.
            **kwargs: Keyword arguments for test case generation.

        Returns:
            Callable: A decorator function for creating test cases.

        使测试用例变量可调用以生成测试用例。

        参数:
            *args: 用于生成测试用例的位置参数。
            **kwargs: 用于生成测试用例的关键字参数。

        返回:
            Callable: 用于创建测试用例的装饰器函数。
        """
        return self.generate_test_case(*args, **kwargs)

    def __repr__(self):
        """
        Get string representation of the test case variable.

        Returns:
            str: String representation of the test case variable.

        获取测试用例变量的字符串表示。

        返回:
            str: 测试用例变量的字符串表示。
        """
        return f"<TestcaseVar{self.style}>"

    def __str__(self):
        """
        Get string representation of the test case variable.

        Returns:
            str: String representation of the test case variable.

        获取测试用例变量的字符串表示。

        返回:
            str: 测试用例变量的字符串表示。
        """
        return self.__repr__()

    def generate_test_case(self, *args, **kwargs) -> Callable:
        """
        Generate a test case with the given parameters.

        Args:
            *args: Positional arguments for test case configuration.
            **kwargs: Keyword arguments for test case configuration.

        Returns:
            Callable: A decorator function that creates a test case instance.

        根据给定参数生成测试用例。

        参数:
            *args: 用于测试用例配置的位置参数。
            **kwargs: 用于测试用例配置的关键字参数。

        返回:
            Callable: 创建测试用例实例的装饰器函数。
        """

        def decorator(func: Callable) -> TestCase:
            test_case_instance = TestCase(func, self.suit)
            test_case_instance.style = self.style
            if self.suit:
                self.suit._test_cases.append(test_case_instance)
                self.suit.output(
                    TestMessageType.DEBUG,
                    f"Testsuite {self.suit.__name} add {self.style} test case {func.__name__} with args {args, kwargs}",
                )
            return test_case_instance

        return decorator
