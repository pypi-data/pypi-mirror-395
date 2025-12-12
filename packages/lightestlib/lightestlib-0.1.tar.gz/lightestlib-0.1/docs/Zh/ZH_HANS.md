# lightestlib 用户指南

## 介绍

lightestlib 是一个轻量级的 Python 测试框架，强调简单性和灵活性。本指南将引导您了解该框架的核心概念和使用模式。

## 核心概念

### 测试套件

测试套件是测试用例的容器。lightestlib 提供了两种主要类型的测试套件：

1. **PlainTestsuite**：支持基本测试的简单测试套件
2. **AssertTestsuite**：支持多种测试类型的高级测试套件

```python
from testlib.suites import PlainTestsuite, AssertTestsuite

# Basic test suite
plain_suite = PlainTestsuite()

# Advanced test suite with multiple test types
assert_suite = AssertTestsuite()
```

### 测试用例

测试用例是作为测试执行的独立函数。lightestlib 支持几种类型的测试用例：

1. **普通测试**：执行一个函数，如果没有抛出异常则通过
2. **结果测试**：验证一个函数返回特定值
3. **异常测试**：验证一个函数抛出特定异常
4. **输出测试**：验证一个函数产生特定的打印输出

### 输出器

输出器决定测试结果的发送位置。可用的输出器包括：

1. **StdOutputer**：输出到标准控制台
2. **FileOutputer**：输出到文件

### 格式化器

格式化器控制测试消息的格式。可用的格式化器包括：

1. **StdMessageFormatter**：标准格式，具有安静、正常和详细模式
2. **LogMessageFormatter**：日志风格格式，具有开发和生产模式

## 详细用法

### 创建测试套件

```python
from testlib.suites import AssertTestsuite
from testlib.outputers import StdOutputer, FileOutputer
from testlib.formatters import StdMessageFormatter, LogMessageFormatter

# Create a test suite
suite = AssertTestsuite()

# Add outputers
suite.add_outputer(StdOutputer(), StdMessageFormatter("normal"))
suite.add_outputer(FileOutputer("test_results.log"), LogMessageFormatter("dev"))
```

### 普通测试

普通测试执行一个函数，如果没有抛出异常则通过：

```python
@suite.add["plain"]
def plain_test():
    print("This is a plain test")
    return "success"
```

### 结果测试

结果测试验证一个函数是否返回特定的值：

```python
@suite.add["result"](42)
def result_test():
    print("This test should return 42")
    return 42
```

### 异常测试

异常测试验证一个函数是否引发特定的异常：

```python
@suite.add["exception"](ValueError)
def exception_test():
    raise ValueError("This is expected")
```

您也可以测试任何异常：

```python
@suite.add["exception"]()
def any_exception_test():
    raise Exception("Any exception is expected")
```

### 输出测试

输出测试验证一个函数是否产生特定的打印输出：

```python
@suite.add["output"]("Expected output")
def output_test():
    print("Expected output")
```

### 运行测试

在一个测试套件中执行所有测试：

```python
suite.run()
```

## 高级功能

### 自定义测试类型

您可以通过扩展 TestCase 或 TestcaseVar 类来创建自定义测试类型：

```python
from testlib.base import TestCase, TestcaseVar

class CustomTestCase(TestCase):
    style = "custom"
    
    def run_test(self):
        # Custom test logic here
        pass

class CustomTestVar(TestcaseVar):
    style = "custom"
    
    def generate_test_case(self, *args, **kwargs):
        # Custom test case generation logic here
        pass
```

### 多个输出器

您可以添加多个输出器，将测试结果发送到不同的目的地：

```python
suite.add_outputer(StdOutputer(), StdMessageFormatter("normal"))
suite.add_outputer(FileOutputer("results.log"), LogMessageFormatter("dev"))
```

### 自定义格式化器

通过扩展 TestMessageFormatter 类来创建自定义格式化器：

```python
from testlib.base import TestMessageFormatter

class CustomFormatter(TestMessageFormatter):
    def format(self, message):
        # Custom formatting logic here
        return formatted_message
```

## 最佳实践

1. **使用适当的测试类型**：选择适合您特定测试需求的测试类型
2. **配置有意义的输出**：为您的环境使用合适的输出器和格式化工具
3. **正确处理异常**：确保您的测试能够正确处理预期和意外的异常
4. **保持测试专注**：每个测试应验证一个特定的行为
5. **使用描述性名称**：为您的测试提供描述性名称，以便更容易理解结果

## 示例

请查看 `example/` 目录以获取完整的工作示例：

- [example1.py]：基本用法
- [example2.py]：使用多种测试类型的高级用法
