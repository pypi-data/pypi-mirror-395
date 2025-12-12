"""
output.py - Output Test Case Variable Implementation

This module provides the OutputTestCaseVar class, which tests if a function produces specific output.

输出测试用例实现模块

该模块提供了OutputTestCaseVar类，用于测试函数是否产生特定输出。
"""

from typing import Callable, Optional
from testlib.base import TestcaseVar, TestCase, TestMessageType
from io import StringIO
import sys


class OutputTestCaseVar(TestcaseVar):
    """
    Output test case variable implementation.

    This test case variable checks if a function produces specific printed output.
    It captures the function's stdout output and compares it with the expected output.

    输出测试用例实现

    该泛测试用例检查函数是否产生特定的打印输出。
    它捕获函数的stdout输出并将其与预期输出进行比较。
    """

    style = "output"

    class _OutputTestCase(TestCase):
        """
        Internal output test case implementation.

        This internal class implements the actual output checking logic.

        内部输出测试用例实现

        该内部类实现了实际的输出检查逻辑。
        """

        def __init__(self, func: Callable, suit=None, result: object = None) -> None:
            """
            Initialize an output test case.

            Args:
                func (Callable): The test function to execute.
                suit (Testsuite, optional): The test suite this test case belongs to.
                result (object, optional): The expected output of the test function.

            初始化输出测试用例

            参数:
                func (Callable): 要执行的测试函数。
                suit (Testsuite, optional): 此测试用例所属的测试套件。
                result (object, optional): 测试函数的预期输出。
            """
            self.result = result
            super().__init__(func, suit)

        def run_test(self) -> Optional[bool]:
            """
            Run the output test case.

            Executes the test function, captures its stdout output, and asserts
            that it matches the expected output. Returns True if assertion passes,
            False if fails, or None if an exception occurs.

            运行输出测试用例

            执行测试函数，捕获其stdout输出，并断言其与预期输出匹配。
            如果断言通过则返回True，失败则返回False，发生异常则返回None。

            Returns:
                Optional[bool]: True if output matches, False if not, None if exception.

                Optional[bool]: 输出匹配返回True，不匹配返回False，异常返回None。
            """
            # 保存当前的sys.stdout
            current_stdout = sys.stdout
            # 创建StringIO对象来捕获print输出
            captured_output = StringIO()
            # 只重定向sys.stdout到StringIO对象（不影响StdOutputer，因为它使用original_stdout）
            sys.stdout = captured_output
            # 清空之前的内容
            captured_output.seek(0)
            captured_output.truncate(0)
            try:
                self.test()
                assert self.result == captured_output.getvalue().strip()
                self.output(
                    TestMessageType.MESSAGE,
                    f"Assert output {self.__name__}() = {self.result} passed",
                    details={
                        "output": captured_output.getvalue().strip(),
                        "status": True,
                        "name": str(self),
                    },
                )
                return True
            except AssertionError:
                self.output(
                    TestMessageType.MESSAGE,
                    f"Assert output {self.__name__}() = {self.result} failed:output:{captured_output.getvalue().strip()}",
                    details={
                        "output": captured_output.getvalue().strip(),
                        "status": False,
                        "name": str(self),
                    },
                )
                return False
            except Exception as e:
                self.output(
                    TestMessageType.MESSAGE,
                    f"{self.__name__} skipped due to exception:{e}",
                    details={"raised exception": e, "status": None, "name": str(self)},
                )
                return None
            finally:
                # 恢复sys.stdout
                sys.stdout = current_stdout

    def generate_test_case(self, result: object = None) -> Callable:
        """
        Generate an output test case with the specified expected output.

        Args:
            result (object, optional): The expected output of the test function.

        Returns:
            Callable: A decorator function that creates an output test case.

        根据指定的预期输出生成输出测试用例

        参数:
            result (object, optional): 测试函数的预期输出

        返回:
            Callable: 创建输出测试用例的装饰器函数
        """

        def decorator(func: Callable) -> TestCase:
            test_case_instance = self._OutputTestCase(func, self.suit, result)
            test_case_instance.style = self.style
            if self.suit:
                self.suit._test_cases.append(test_case_instance)
            return test_case_instance

        return decorator
