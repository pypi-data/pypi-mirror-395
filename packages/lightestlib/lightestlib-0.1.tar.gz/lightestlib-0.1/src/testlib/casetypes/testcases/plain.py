"""
plain.py - Plain Test Case Implementation

This module provides the PlainTestCase class, which executes tests and passes if no exception is raised.

普通测试用例实现模块

该模块提供了PlainTestCase类，用于执行测试并在无异常时通过。
"""

from testlib.base import TestCase, TestMessageType


class PlainTestCase(TestCase):
    """
    Plain test case implementation.

    This test case executes the test function and passes if no exception is raised.
    It's the simplest form of test case in the testlib framework.

    普通测试用例实现

    该测试用例执行测试函数并在无异常时通过。
    这是testlib框架中最简单的测试用例形式。
    """

    style = "plain"

    def run_test(self) -> bool:
        """
        Run the plain test case.

        Executes the test function and returns True if no exception is raised,
        False otherwise. Outputs appropriate messages based on the test result.

        运行普通测试用例

        执行测试函数，如果无异常则返回True，否则返回False。
        根据测试结果输出适当的消息。

        Returns:
            bool: True if the test passes (no exception), False if it fails.

            bool: 如果测试通过（无异常）则返回True，失败则返回False。
        """
        try:
            self.test()
            self.output(
                TestMessageType.MESSAGE,
                f"{self.__name__} passed",
                details={"status": True, "name": str(self)},
            )
            return True
        except Exception as e:
            self.output(
                TestMessageType.MESSAGE,
                f"{self.__name__} failed: {e}",
                details={"status": False, "name": str(self)},
            )
            return False
