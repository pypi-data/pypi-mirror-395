"""
result.py - Result Test Case Variable Implementation

This module provides the ResultTestCaseVar class, which tests if a function returns a specific value.

结果测试用例实现模块

该模块提供了ResultTestCaseVar类，用于测试函数是否返回特定值。
"""

from typing import Callable, Optional
from testlib.base import TestcaseVar, TestCase, TestMessageType


class ResultTestCaseVar(TestcaseVar):
    """
    Result test case variable implementation.

    This test case variable checks if a function returns a specific expected result.
    It creates test cases that assert the function's return value equals the expected value.

    结果测试用例实现

    该泛测试用例检查函数是否返回特定的预期结果。
    它创建断言函数返回值等于预期值的测试用例。
    """

    style = "result"

    class _ResultTestCase(TestCase):
        """
        Internal result test case implementation.

        This internal class implements the actual result checking logic.

        内部结果测试用例实现

        该内部类实现了实际的结果检查逻辑。
        """

        def __init__(self, func: Callable, suit=None, result: object = None) -> None:
            """
            Initialize a result test case.

            Args:
                func (Callable): The test function to execute.
                suit (Testsuite, optional): The test suite this test case belongs to.
                result (object, optional): The expected result of the test function.

            初始化结果测试用例

            参数:
                func (Callable): 要执行的测试函数。
                suit (Testsuite, optional): 此测试用例所属的测试套件。
                result (object, optional): 测试函数的预期结果。
            """
            self.result = result
            super().__init__(func, suit)

        def run_test(self) -> Optional[bool]:
            """
            Run the result test case.

            Executes the test function and asserts that its return value equals
            the expected result. Returns True if assertion passes, False if fails,
            or None if an exception occurs.

            运行结果测试用例

            执行测试函数并断言其返回值等于预期结果。
            如果断言通过则返回True，失败则返回False，发生异常则返回None。

            Returns:
                Optional[bool]: True if test passes, False if fails, None if exception.

                Optional[bool]: 测试通过返回True，失败返回False，异常返回None。
            """
            try:
                assert self.test() == self.result
                self.output(
                    TestMessageType.MESSAGE,
                    f"Assertion {self.__name__}() = {self.result} passed",
                    details={"result": self.result, "status": True, "name": str(self)},
                )
                return True
            except AssertionError:
                self.output(
                    TestMessageType.MESSAGE,
                    f"Assertion {self.__name__}() = {self.result} failed",
                    details={"result": self.result, "status": False, "name": str(self)},
                )
                return False
            except Exception as e:
                self.output(
                    TestMessageType.MESSAGE,
                    f"{self.__name__} skipped with exception:{e}",
                    details={"exception": e, "status": None, "name": str(self)},
                )
                return None

    def generate_test_case(self, result: object = None) -> Callable:
        """
        Generate a result test case with the specified expected result.

        Args:
            result (object, optional): The expected result of the test function.

        Returns:
            Callable: A decorator function that creates a result test case.

        根据指定的预期结果生成结果测试用例

        参数:
            result (object, optional): 测试函数的预期结果

        返回:
            Callable: 创建结果测试用例的装饰器函数
        """

        def decorator(func: Callable) -> TestCase:
            test_case_instance = self._ResultTestCase(func, self.suit, result)
            test_case_instance.style = self.style
            if self.suit:
                self.suit._test_cases.append(test_case_instance)
            return test_case_instance

        return decorator
