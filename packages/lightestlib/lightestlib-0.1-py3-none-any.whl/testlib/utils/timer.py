"""
timer.py - Execution Time Measurement Utility

This module provides a decorator for measuring function execution time.

执行时间测量工具模块

该模块提供了一个用于测量函数执行时间的装饰器。
"""

import time
from functools import wraps


def timer(func):
    """
    Decorator for measuring function execution time.

    This decorator measures and prints the execution time of the decorated function.

    测量函数执行时间的装饰器

    该装饰器测量并打印被装饰函数的执行时间。

    Args:
        func (Callable): The function to measure.

    Returns:
        Callable: The decorated function.

    参数:
        func (Callable): 要测量的函数

    返回:
        Callable: 装饰后的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            # 执行函数
            result = func(*args, **kwargs)
            return result
        finally:
            # 计算执行时间
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"函数 {func.__name__} 执行时间: {elapsed_time:.4f} 秒")

    return wrapper
