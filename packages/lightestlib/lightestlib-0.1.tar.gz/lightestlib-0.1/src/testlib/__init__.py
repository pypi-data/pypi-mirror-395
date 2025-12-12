"""
__init__.py - Main Module for testlib

This is the main entry point for the testlib framework.
It imports and exports all major components of the testing framework including:
- suites: Test suite implementations
- casetypes: Test case type implementations
- outputers: Output handler implementations
- formatters: Message formatter implementations
- utils: Utility functions and decorators
- base: Base classes for the framework

testlib主模块

这是testlib框架的主入口点。
它导入并导出测试框架的所有主要组件，包括：
- suites: 测试套件实现
- casetypes: 测试用例类型实现
- outputers: 输出处理器实现
- formatters: 消息格式化器实现
- utils: 实用函数和装饰器
- base: 框架的基类
"""

import testlib.suites as suites
import testlib.casetypes as casetypes
import testlib.outputers as outputers
import testlib.utils as utils
import testlib.base as base
import testlib.formatters as formatters

__all__ = ["suites", "casetypes", "outputers", "utils", "base", "formatters"]
