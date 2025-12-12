"""
suites/__init__.py - Test Suites Module

This module provides the main entry point for different test suites in the testlib framework.
It imports and exports the various test suite implementations.

测试套件模块

该模块为testlib框架中的不同测试套件提供了主入口点。
它导入并导出各种测试套件实现。
"""

from testlib.suites.plainsuite import PlainTestsuite
from testlib.suites.assertsuit import AssertTestsuite

__all__ = ["PlainTestsuite", "AssertTestsuite"]
