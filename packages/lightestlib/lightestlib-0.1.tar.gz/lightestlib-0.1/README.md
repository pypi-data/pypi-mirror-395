# lightestlib

A simple, pythonic Python test framework implemented in Python.

## Overview

lightestlib is a lightweight testing framework designed for simplicity and ease of use. It provides a flexible architecture that allows you to define different types of tests and customize output formatting and reporting.

## Quick Start

### Installation

Install from PyPI:

```bash
pip install lightestlib
```

Or clone the repository:

```bash
git clone <repository-url>
cd testlib
```

Hence using the match-case sentences, only python 3.10 and above are supported

### Basic Usage

```python
from testlib.suites import PlainTestsuite
from testlib.outputers import StdOutputer
from testlib.formatters import StdMessageFormatter

# Create a test suite
suite = PlainTestsuite()
suite.add_outputer(StdOutputer(), StdMessageFormatter("normal"))

# Add a plain test
@suite.add["plain"]
def sample_test():
    print("Hello, pytestlib!")
    return True

# Run the tests
suite.run()
```

## Features

- Multiple test types: Plain, Result, Exception, and Output tests
- Flexible output system with support for console and file output
- Customizable message formatting
- Extensible architecture for adding new test types

## Documentation

For detailed usage instructions, please see the documentation in the `docs/` directory:

- User Guide
- API Reference
- Examples

## License

See the [LICENSE](LICENSE) file for details.

## Contact

For bug reports and feature requests, please use the [issue tracker](https://github.com/Alwaylone9801/testlib/issues).
For general questions and discussions, please use [GitHub Discussions](https://github.com/Alwaylone9801/testlib/discussions).
