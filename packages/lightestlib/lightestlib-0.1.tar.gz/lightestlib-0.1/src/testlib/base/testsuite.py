"""
testsuite.py - Test Suite Base Class

This module provides the base Testsuite class for creating test suites and managing test cases.

测试套件模块

该模块提供了创建测试套件和管理测试用例的基类Testsuite。
"""

from typing import Dict, Type, Optional, List, Callable, Tuple
from testlib.base.testcase import TestCase
from testlib.base.testcasevar import TestcaseVar
from testlib.base.testmessage import TestMessage, TestMessageType
from testlib.base.testoutputer import TestOutputer
from testlib.base.testmessageformatter import TestMessageFormatter
from datetime import datetime
from io import StringIO
import sys


class Testsuite(object):
    """
    Base class for test suites.

    This class provides the foundation for all test suites in the testlib framework.
    It manages test cases, outputers, and the execution of tests.

    测试套件基类

    该类为testlib框架中的所有测试套件提供了基础。
    它管理测试用例、输出器和测试的执行。
    """

    _test_types: Dict[str, Type[TestCase] | TestcaseVar]
    _outputers: List[
        Tuple[
            TestOutputer | Callable[[str], Optional[bool]],
            TestMessageFormatter | Callable[[TestMessage], str],
        ]
    ]
    _test_cases: List[TestCase]

    def __init__(
        self,
        name: Optional[str] = None,
        outputer: Optional[
            List[
                Tuple[
                    TestOutputer | Callable[[str], Optional[bool]],
                    TestMessageFormatter | Callable[[TestMessage], str],
                ]
            ]
        ] = None,
    ):
        """
        Initialize a Testsuite instance.

        Args:
            name (str, optional): The name of the test suite. Defaults to current timestamp.
            outputer (List[Tuple], optional): List of outputer-transformer pairs.

        初始化Testsuite实例。

        参数:
            name (str, optional): 测试套件的名称。默认为当前时间戳。
            outputer (List[Tuple], optional): 输出器-转换器对的列表。
        """
        if name is None:
            self.__name = str(datetime.now())
        else:
            self.__name = name

        self._test_cases = []
        self._test_types = {}
        self._outputers = []
        # 添加临时消息缓冲区
        self._temp_messages = []
        self.add = TestcaseManger(self)
        self.add_outputer = TestOutputerManager(self)
        if outputer is not None:
            for out, trans in outputer:
                self.add_outputer(out, trans)
        self.initialize()
        self.output(TestMessageType.DEBUG, f"{str(self)} initialized")

    def __str__(self):
        """
        Get string representation of the test suite.

        Returns:
            str: String representation of the test suite.

        获取测试套件的字符串表示。

        返回:
            str: 测试套件的字符串表示。
        """
        return f"<Testsuite {self.__name}>"

    def __repr__(self) -> str:
        """
        Get detailed string representation of the test suite.

        Returns:
            str: Detailed string representation of the test suite.

        获取测试套件的详细字符串表示。

        返回:
            str: 测试套件的详细字符串表示。
        """
        return f"<Testsuite {self.__name}>"

    def run(self):
        """
        Run all test cases in the test suite.

        Execute all test cases that have been added to this test suite,
        and output the results through the configured outputers.

        运行测试套件中的所有测试用例。

        执行已添加到此测试套件中的所有测试用例，
        并通过配置的输出器输出结果。
        """
        self.output(
            TestMessageType.INFO,
            f"{str(self)} starts running",
            details={
                "cases": len(self._test_cases),
                "name": str(self),
                "status": "start",
            },
        )
        # 保存当前的sys.stdout
        current_stdout = sys.stdout
        # 创建StringIO对象来捕获print输出
        captured_output = StringIO()

        try:
            # 只重定向sys.stdout到StringIO对象（不影响StdOutputer，因为它使用original_stdout）
            sys.stdout = captured_output
            passed = 0
            failed = 0
            skipped = 0
            # 执行测试
            for test_case in self._test_cases:
                # 清空之前的内容
                captured_output.seek(0)
                captured_output.truncate(0)

                # 执行单个测试
                r = test_case()
                match r:
                    case True:
                        passed += 1
                    case False:
                        failed += 1
                    case None:
                        skipped += 1
                    case _:
                        raise Exception(
                            f"Unexpected result from test case: {r}. Expected True, False or None."
                        )

                # 获取捕获的输出并将换行符转义为字面量字符串"\n"
                output_content = (
                    captured_output.getvalue().replace("\n", "\\n").replace("\r", "\\r")
                )

                # 如果有捕获的输出，将其作为测试消息输出
                if output_content.strip():
                    self.output(
                        TestMessageType.INFO,
                        "Captured output during test execution:",
                        details={
                            "output": output_content,
                            "name": str(test_case),
                            "status": "output",
                        },
                    )
            # 恢复sys.stdout
            sys.stdout = current_stdout
            self.output(
                TestMessageType.INFO,
                f"{str(self)} finished",
                details={
                    "status": "end",
                    "name": str(self),
                    "passed": passed,
                    "failed": failed,
                    "skipped": skipped,
                },
            )
        except Exception as e:
            # 即使出错也要恢复sys.stdout
            sys.stdout = current_stdout
            self.output(TestMessageType.WARNING, f"Error during test execution: {e}")
            # raise e
        finally:
            # 确保总是恢复sys.stdout
            sys.stdout = current_stdout

    def initialize(self):
        """
        Initialize the test suite. This method can be overridden by subclasses.

        初始化测试套件。此方法可由子类重写。
        """
        pass

    def output(self, *args, **kwargs):
        """
        Output a message through all configured outputers.

        Args:
            *args: Arguments for creating a TestMessage.
            **kwargs: Keyword arguments for creating a TestMessage.

        通过所有配置的输出器输出消息。

        参数:
            *args: 用于创建TestMessage的参数。
            **kwargs: 用于创建TestMessage的关键字参数。
        """
        if len(self._outputers) == 0:
            # 在没有输出器时，缓存DEBUG级别以下的消息
            message = TestMessage(*args, **kwargs)
            self._temp_messages.append(message)
            if args[0] == TestMessageType.DEBUG:
                return True
            # 对于其他级别的消息，缓存并输出到控制台
            print(f"Warning: {str(self)} does not have an outputer")
            print(message)
            return False
        # 当有输出器时，首先输出缓存的消息
        if self._temp_messages:
            for temp_msg in self._temp_messages:
                for outputer, transformer in self._outputers:
                    if isinstance(outputer, TestOutputer):
                        outputer.output(transformer(temp_msg))
                    else:
                        outputer(transformer(temp_msg))
            self._temp_messages.clear()

        # 正常输出当前消息
        for outputer, transformer in self._outputers:
            if isinstance(outputer, TestOutputer):
                outputer.output(transformer(TestMessage(*args, **kwargs)))
            else:
                outputer(transformer(TestMessage(*args, **kwargs)))
        return True

    def __call__(self):
        """
        Make the test suite callable, which runs all tests.

        Returns:
            The result of run().

        使测试套件可调用，用于运行所有测试。

        返回:
            run()的结果。
        """
        return self.run()

    def __add__(self, other: "Testsuite") -> "Testsuite":
        """
        Combine two test suites.

        Args:
            other (Testsuite): Another test suite to combine with this one.

        Returns:
            Testsuite: This test suite with the other's test cases, types, and outputers added.

        合并两个测试套件。

        参数:
            other (Testsuite): 要与此测试套件合并的另一个测试套件。

        返回:
            Testsuite: 添加了另一个测试套件的测试用例、类型和输出器的此测试套件。
        """
        self._test_cases.extend(other._test_cases)
        self._test_types.update(other._test_types)
        self._outputers.extend(other._outputers)
        other._test_cases = self._test_cases
        other._test_types = self._test_types
        other._outputers = self._outputers
        self.output(TestMessageType.DEBUG, f"{str(self)} added {str(other)}")
        return self


class TestcaseManger:
    """
    Manager class for test cases in a test suite.

    This class handles the registration and management of test cases within a test suite.

    测试用例管理器类

    该类处理测试套件内测试用例的注册和管理。
    """

    def __init__(self, suit: Testsuite):
        """
        Initialize a TestcaseManger instance.

        Args:
            suit (Testsuite): The test suite this manager belongs to.

        初始化TestcaseManger实例。

        参数:
            suit (Testsuite): 此管理器所属的测试套件。
        """
        self.suit = suit
        pass

    def __call__(self, name: str):
        """
        Register a new test type with the given name.

        Args:
            name (str): The name of the test type to register.

        Returns:
            A function that registers the test type.

        注册具有给定名称的新测试类型。

        参数:
            name (str): 要注册的测试类型的名称。

        返回:
            注册测试类型的函数。
        """

        def _test_type_add(test_type: Type[TestCase | TestcaseVar]):
            test_type.style = name
            if issubclass(test_type, TestcaseVar):
                self.suit._test_types.update({name: test_type(self.suit)})
            elif issubclass(test_type, TestCase):
                self.suit._test_types.update({name: test_type})
            self.suit.output(
                TestMessageType.DEBUG,
                f"{str(self.suit)} add test type {name} : {test_type.style}",
            )
            return test_type

        return _test_type_add

    def __getitem__(self, name: str = "default"):
        """
        Get a test case by name.

        Args:
            name (str): The name of the test case to retrieve. Defaults to "default".

        Returns:
            The test case with the given name.

        根据名称获取测试用例。

        参数:
            name (str): 要检索的测试用例的名称。默认为"default"。

        返回:
            具有给定名称的测试用例。
        """
        test_type = self.suit._test_types.get(name)
        if test_type is None:
            raise KeyError(f"{name} is not a test type")
        if isinstance(test_type, TestcaseVar):
            return test_type
        elif issubclass(test_type, TestCase):

            def decorator(func):
                # 创建对应的测试用例实例并添加到测试套件中
                test_case_instance = test_type(func=func, suit=self.suit)
                self.suit._test_cases.append(test_case_instance)
                self.suit.output(
                    TestMessageType.DEBUG,
                    f"{str(self.suit)} add {test_type.style} test case {func.__name__}",
                )
                return test_case_instance

            return decorator
        else:
            raise TypeError("test_type must be a TestCase or TestcaseVar")

    def default(self, test_type: Type[TestCase | TestcaseVar]):
        """
        Set the default test type for the test suite.

        Args:
            test_type (Type[TestCase | TestcaseVar]): The test type to set as default.

        Returns:
            The test type that was set as default.

        为测试套件设置默认测试类型。

        参数:
            test_type (Type[TestCase | TestcaseVar]): 要设置为默认的测试类型。

        返回:
            被设置为默认的测试类型。
        """
        if issubclass(test_type, TestcaseVar):
            decorater = test_type(self.suit)
        elif issubclass(test_type, TestCase):
            decorater = test_type
        else:
            raise TypeError("test_type must be a TestCase or TestcaseVar")
        self.suit._test_types.update({"default": decorater})
        self.suit.output(
            TestMessageType.DEBUG,
            f"{str(self.suit)} set default test type {test_type.style}",
        )
        return test_type


class TestOutputerManager:
    """
    Manager class for outputers in a test suite.

    This class handles the registration and management of outputers within a test suite.

    测试输出器管理器类

    该类处理测试套件内输出器的注册和管理。
    """

    def __init__(self, suit: Testsuite):
        """
        Initialize a TestOutputerManager instance.

        Args:
            suit (Testsuite): The test suite this manager belongs to.

        初始化TestOutputerManager实例。

        参数:
            suit (Testsuite): 此管理器所属的测试套件。
        """
        self.suit = suit
        pass

    def __call__(
        self,
        outputer: Optional[TestOutputer | Callable[[str], Optional[bool]]] = None,
        transformer: Optional[
            TestMessageFormatter | Callable[[TestMessage], str]
        ] = None,
    ):
        """
        Register a new outputer with the test suite.

        Args:
            outputer (TestOutputer | Callable, optional): The outputer to register. Defaults to print.
            transformer (TestMessageFormatter | Callable, optional): The message formatter. Defaults to str.

        Returns:
            The registered outputer.

        为测试套件注册新输出器。

        参数:
            outputer (TestOutputer | Callable, optional): 要注册的输出器。默认为print。
            transformer (TestMessageFormatter | Callable, optional): 消息格式化器。默认为str。

        返回:
            已注册的输出器。
        """
        if outputer is None:
            outputer = print
        if transformer is None:
            transformer = str
        self.suit._outputers.append((outputer, transformer))

        self.suit.output(
            TestMessageType.DEBUG,
            f"{str(self.suit)} add outputer {repr(outputer)} with format {repr(transformer)}",
        )
        return outputer
