"""
memory_monitor.py - Memory Usage Monitoring Utility

This module provides a decorator for monitoring memory usage during function execution.

内存使用监控工具模块

该模块提供了一个用于监控函数执行过程中内存使用的装饰器。
"""

import tracemalloc
from functools import wraps


def memory_monitor(func):
    """
    Decorator for monitoring memory usage during function execution.

    This decorator tracks and prints memory usage information of the decorated function.

    监控函数执行过程中内存使用的装饰器

    该装饰器跟踪并打印被装饰函数的内存使用信息。

    Args:
        func (Callable): The function to monitor.

    Returns:
        Callable: The decorated function.

    参数:
        func (Callable): 要监控的函数

    返回:
        Callable: 装饰后的函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 开始追踪
        tracemalloc.start()
        start_current, start_peak = tracemalloc.get_traced_memory()

        try:
            # 执行函数
            result = func(*args, **kwargs)
            return result
        finally:
            # 结束追踪并输出内存使用情况
            end_current, end_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print(f"函数 {func.__name__} 内存使用情况:")
            print(f"  当前内存增加: {(end_current - start_current) / 1024:.2f} KB")
            print(f"  峰值内存增加: {(end_peak - start_peak) / 1024:.2f} KB")

    return wrapper
