"""
testcase.py - Test Case Base Class

This module provides the base TestCase class for creating test cases in the testlib framework.

测试用例模块

该模块提供了testlib框架中创建测试用例的基类TestCase。
"""

from typing import Callable, Optional


class TestCase:
    """
    Base class for all test cases.

    This class serves as the foundation for all test cases in the testlib framework.
    It provides basic functionality for running tests and outputting results.

    测试用例基类

    该类是testlib框架中所有测试用例的基础类。
    它提供了运行测试和输出结果的基本功能。
    """

    style = ""

    def __init__(self, func: Callable, suit=None) -> None:
        """
        Initialize a TestCase instance.

        Args:
            func (Callable): The test function to be executed.
            suit (Testsuite, optional): The test suite this test case belongs to.

        初始化TestCase实例。

        参数:
            func (Callable): 要执行的测试函数。
            suit (Testsuite, optional): 此测试用例所属的测试套件。
        """
        self.__name__ = func.__name__
        self.test = func
        self.suit = suit
        pass

    def output(self, *args, **kwargs) -> None:
        """
        Output test messages through the test suite's output system.

        Args:
            *args: Arguments to pass to the output system.
            **kwargs: Keyword arguments to pass to the output system.

        通过测试套件的输出系统输出测试消息。

        参数:
            *args: 传递给输出系统的参数。
            **kwargs: 传递给输出系统的关键字参数。
        """
        if self.suit:
            self.suit.output(*args, **kwargs, suit=self.suit)
        else:
            print(f"Warning:Testsuit{self.suit} does not have an outputer")
            print(*args, **kwargs)

    def run_test(self) -> Optional[bool]:
        """
        Run the test case. This method should be implemented by subclasses.

        Returns:
            Optional[bool]: True if the test passes, False if it fails, None if skipped.

        运行测试用例。此方法应由子类实现。

        返回:
            Optional[bool]: True表示测试通过，False表示测试失败，None表示跳过测试。
        """
        return False

    def __call__(self):
        """
        Make the test case callable, which runs the test.

        Returns:
            The result of run_test().

        使测试用例可调用，用于运行测试。

        返回:
            run_test()的结果。
        """
        return self.run_test()

    def __str__(self) -> str:
        """
        Get string representation of the test case.

        Returns:
            str: String representation of the test case.

        获取测试用例的字符串表示。

        返回:
            str: 测试用例的字符串表示。
        """
        return f"<{self.style} Testcase {self.__name__}>"

    def __repr__(self) -> str:
        """
        Get detailed string representation of the test case.

        Returns:
            str: Detailed string representation of the test case.

        获取测试用例的详细字符串表示。

        返回:
            str: 测试用例的详细字符串表示。
        """
        return f"<{self.style} Testcase {self.__name__}>"
