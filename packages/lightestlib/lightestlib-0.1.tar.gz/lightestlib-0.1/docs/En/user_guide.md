# lightestlib User Guide

## Introduction

lightestlib is a lightweight testing framework for Python that emphasizes simplicity and flexibility. This guide will walk you through the core concepts and usage patterns of the framework.

## Core Concepts

### Test Suites

Test suites are containers for test cases. lightestlib provides two main types of test suites:

1. **PlainTestsuite**: Basic test suite with plain test support
2. **AssertTestsuite**: Advanced test suite with support for multiple test types

```python
from testlib.suites import PlainTestsuite, AssertTestsuite

# Basic test suite
plain_suite = PlainTestsuite()

# Advanced test suite with multiple test types
assert_suite = AssertTestsuite()
```

### Test Cases

Test cases are individual functions that are executed as tests. lightestlib supports several types of test cases:

1. **Plain Tests**: Execute a function and pass if no exception is raised
2. **Result Tests**: Verify that a function returns a specific value
3. **Exception Tests**: Verify that a function raises a specific exception
4. **Output Tests**: Verify that a function produces specific printed output

### Outputers

Outputers determine where test results are sent. Available outputers include:

1. **StdOutputer**: Outputs to the standard console
2. **FileOutputer**: Outputs to a file

### Formatters

Formatters control how test messages are formatted. Available formatters include:

1. **StdMessageFormatter**: Standard formatting with quiet, normal, and detail modes
2. **LogMessageFormatter**: Log-style formatting with dev and prod modes

## Detailed Usage

### Creating Test Suites

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

### Plain Tests

Plain tests execute a function and pass if no exception is raised:

```python
@suite.add["plain"]
def plain_test():
    print("This is a plain test")
    return "success"
```

### Result Tests

Result tests verify that a function returns a specific value:

```python
@suite.add["result"](42)
def result_test():
    print("This test should return 42")
    return 42
```

### Exception Tests

Exception tests verify that a function raises a specific exception:

```python
@suite.add["exception"](ValueError)
def exception_test():
    raise ValueError("This is expected")
```

You can also test for any exception:

```python
@suite.add["exception"]()
def any_exception_test():
    raise Exception("Any exception is expected")
```

### Output Tests

Output tests verify that a function produces specific printed output:

```python
@suite.add["output"]("Expected output")
def output_test():
    print("Expected output")
```

### Running Tests

Execute all tests in a suite:

```python
suite.run()
```

## Advanced Features

### Custom Test Types

You can create custom test types by extending the TestCase or TestcaseVar classes:

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

### Multiple Outputers

You can add multiple outputers to send test results to different destinations:

```python
suite.add_outputer(StdOutputer(), StdMessageFormatter("normal"))
suite.add_outputer(FileOutputer("results.log"), LogMessageFormatter("dev"))
```

### Custom Formatters

Create custom formatters by extending the TestMessageFormatter class:

```python
from testlib.base import TestMessageFormatter

class CustomFormatter(TestMessageFormatter):
    def format(self, message):
        # Custom formatting logic here
        return formatted_message
```

## Best Practices

1. **Use appropriate test types**: Choose the right test type for your specific testing needs
2. **Configure meaningful output**: Use appropriate outputers and formatters for your environment
3. **Handle exceptions properly**: Make sure your tests properly handle expected and unexpected exceptions
4. **Keep tests focused**: Each test should verify one specific behavior
5. **Use descriptive names**: Give your tests descriptive names to make results easier to understand

## Examples

See the `example/` directory for complete working examples:

- [example1.py]: Basic usage
- [example2.py]: Advanced usage with multiple test types
