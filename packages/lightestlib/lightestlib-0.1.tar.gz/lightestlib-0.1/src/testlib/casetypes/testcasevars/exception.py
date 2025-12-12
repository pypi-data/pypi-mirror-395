"""
exception.py - Exception Test Case Variable Implementation

This module provides the ExceptionTestCaseVar class, which tests if a function raises a specific exception.

异常测试用例实现模块

该模块提供了ExceptionTestCaseVar类，用于测试函数是否引发特定异常。
"""

from typing import Callable, Type, Optional
from testlib.base import TestcaseVar, TestCase, TestMessageType


class ExceptionTestCaseVar(TestcaseVar):
    """
    Exception test case variable implementation.

    This test case variable checks if a function raises a specific exception.
    It can test for any exception or a specific type of exception.

    异常测试用例实现

    该泛测试用例检查函数是否引发特定异常。
    它可以测试任何异常或特定类型的异常。
    """

    style = "exception"

    class _ExceptionTestCase(TestCase):
        """
        Internal exception test case implementation.

        This internal class implements the actual exception checking logic.

        内部异常测试用例实现

        该内部类实现了实际的异常检查逻辑。
        """

        def __init__(
            self,
            func: Callable,
            suit=None,
            exception: Optional[Type[Exception]] = None,
        ):
            """
            Initialize an exception test case.

            Args:
                func (Callable): The test function to execute.
                suit (Testsuite, optional): The test suite this test case belongs to.
                exception (Type[Exception], optional): The expected exception type.

            初始化异常测试用例

            参数:
                func (Callable): 要执行的测试函数。
                suit (Testsuite, optional): 此测试用例所属的测试套件。
                exception (Type[Exception], optional): 预期的异常类型。
            """
            self.exception = exception
            super().__init__(func, suit)

        def run_test(self) -> Optional[bool]:
            """
            Run the exception test case.

            Executes the test function and checks if it raises the expected exception.
            Returns True if the expected exception is raised, False if not,
            or None if an unexpected exception occurs.

            运行异常测试用例

            执行测试函数并检查是否引发预期异常。
            如果引发预期异常则返回True，未引发则返回False，
            发生意外异常则返回None。

            Returns:
                Optional[bool]: True if expected exception is raised, False if not, None if unexpected exception.

                Optional[bool]: 引发预期异常返回True，未引发返回False，意外异常返回None。
            """
            if self.exception is None:
                try:
                    self.test()
                    self.output(
                        TestMessageType.MESSAGE,
                        f"Assert Exception {self.__name__} failed : No Exception raised",
                        details={"status": False, "name": str(self)},
                    )
                    return False
                except Exception as e:
                    self.output(
                        TestMessageType.MESSAGE,
                        f"Assert Exception {self.__name__} successfully raised: {e}",
                        details={"status": True, "name": str(self)},
                    )
                    return True
            else:
                try:
                    self.test()
                    self.output(
                        TestMessageType.MESSAGE,
                        f"Assert Exception {self.__name__} failed : No Exception raised",
                        details={"status": False, "name": str(self)},
                    )
                    return False
                except Exception as e:
                    if isinstance(e, self.exception):
                        self.output(
                            TestMessageType.MESSAGE,
                            f"Assert Exception {self.__name__} successfully raised: {e}",
                            details={"status": True, "name": str(self)},
                        )
                        return True
                    else:
                        self.output(
                            TestMessageType.MESSAGE,
                            f"Assert Exception {self.__name__} failed: raised: {e}",
                            details={"status": False, "name": str(self)},
                        )
                        return False

    def generate_test_case(
        self, exception: Optional[Type[Exception]] = None
    ) -> Callable:
        """
        Generate an exception test case with the specified expected exception.

        Args:
            exception (Type[Exception], optional): The expected exception type. If None, any exception is accepted.

        Returns:
            Callable: A decorator function that creates an exception test case.

        根据指定的预期异常生成异常测试用例

        参数:
            exception (Type[Exception], optional): 预期的异常类型。如果为None，则接受任何异常。

        返回:
            Callable: 创建异常测试用例的装饰器函数
        """

        def decorator(func: Callable) -> TestCase:
            test_case_instance = self._ExceptionTestCase(func, self.suit, exception)
            test_case_instance.style = self.style
            if self.suit:
                self.suit._test_cases.append(test_case_instance)
            return test_case_instance

        return decorator
