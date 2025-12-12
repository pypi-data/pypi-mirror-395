"""
runner.py - Function Runner Utilities

This module provides utility functions for running functions in different modes.

函数运行器工具模块

该模块提供了以不同模式运行函数的实用工具。
"""

from typing import Callable
from functools import wraps


def plainrun(func: Callable):
    """
    Decorator that converts a function to plain run mode.

    The decorated function will return True if it executes without raising an exception,
    or False if an exception is raised.

    将函数转换为普通运行模式的装饰器

    装饰后的函数在无异常执行时返回True，
    在引发异常时返回False。

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.

    参数:
        func (Callable): 要装饰的函数

    返回:
        Callable: 装饰后的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except Exception as e:  # noqa: F841
            return False

    return wrapper


def tryrun(func: Callable):
    """
    Decorator that converts a function to try run mode.

    The decorated function will return its result if it executes without raising an exception,
    or return the exception if one is raised.

    将函数转换为尝试运行模式的装饰器

    装饰后的函数在无异常执行时返回其结果，
    在引发异常时返回该异常。

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.

    参数:
        func (Callable): 要装饰的函数

    返回:
        Callable: 装饰后的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return e

    return wrapper
