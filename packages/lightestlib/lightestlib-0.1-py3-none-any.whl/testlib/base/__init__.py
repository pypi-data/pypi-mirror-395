"""
__init__.py - Base Module for testlib

This module provides the foundational classes and components for the testlib framework.
It includes base classes for test cases, test suites, messages, outputers, and formatters.

基础模块

该模块为testlib框架提供了基础类和组件。
包括测试用例、测试套件、消息、输出器和格式化器的基类。
"""

from testlib.base.testcase import TestCase
from testlib.base.testcasevar import TestcaseVar
from testlib.base.testmessage import TestMessageType, TestMessage
from testlib.base.testoutputer import TestOutputer
from testlib.base.testmessageformatter import TestMessageFormatter
from testlib.base.testsuite import Testsuite

__all__ = [
    "TestCase",
    "TestcaseVar",
    "TestMessageType",
    "TestMessage",
    "TestOutputer",
    "TestMessageFormatter",
    "Testsuite",
]
