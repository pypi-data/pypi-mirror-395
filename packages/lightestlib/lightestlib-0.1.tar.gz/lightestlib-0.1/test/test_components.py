import sys
from pathlib import Path
import tempfile
import os

# 添加项目路径到sys.path以导入testlib
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from testlib.suites import AssertTestsuite, PlainTestsuite
from testlib.outputers import StdOutputer, FileOutputer
from testlib.formatters import StdMessageFormatter, LogMessageFormatter
from testlib.base import TestMessage, TestMessageType

# 创建测试套件
suite = AssertTestsuite()
suite.add_outputer(StdOutputer(), StdMessageFormatter("normal"))


# 测试基础测试套件功能
@suite.add["plain"]
def test_testsuite_creation():
    """测试Testsuite创建"""
    assert suite is not None
    assert hasattr(suite, "add")
    assert hasattr(suite, "add_outputer")


# 测试PlainTestsuite
@suite.add["plain"]
def test_plainsuite():
    """测试PlainTestsuite功能"""
    plain_suite = PlainTestsuite()
    assert plain_suite is not None

    # 添加测试用例
    @plain_suite.add["plain"]
    def simple_test():
        return True

    # 确保测试用例被添加
    assert len(plain_suite._test_cases) > 0


# 测试AssertTestsuite
@suite.add["plain"]
def test_assertsuite():
    """测试AssertTestsuite功能"""
    assert_suite = AssertTestsuite()
    assert assert_suite is not None

    # 检查是否注册了所有测试类型
    assert "plain" in assert_suite._test_types
    assert "result" in assert_suite._test_types
    assert "exception" in assert_suite._test_types
    assert "output" in assert_suite._test_types


# 测试StdOutputer
@suite.add["plain"]
def test_stdoutputer():
    """测试StdOutputer功能"""
    std_outputer = StdOutputer()
    assert std_outputer is not None
    assert hasattr(std_outputer, "output")


# 测试FileOutputer
@suite.add["plain"]
def test_fileoutputer():
    """测试FileOutputer功能"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        file_outputer = FileOutputer(tmp_path)
        assert file_outputer is not None
        assert hasattr(file_outputer, "output")

        # 测试写入功能
        file_outputer.output("test message\n")
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# 测试StdMessageFormatter
@suite.add["plain"]
def test_stdmessageformatter():
    """测试StdMessageFormatter功能"""
    formatter = StdMessageFormatter("normal")
    assert formatter is not None

    message = TestMessage(TestMessageType.INFO, "测试消息")
    formatted = formatter.format(message)
    assert isinstance(formatted, str)


# 测试LogMessageFormatter
@suite.add["plain"]
def test_logmessageformatter():
    """测试LogMessageFormatter功能"""
    formatter = LogMessageFormatter("dev")
    assert formatter is not None

    message = TestMessage(TestMessageType.INFO, "测试消息")
    formatted = formatter.format(message)
    assert isinstance(formatted, str)


# 测试测试消息
@suite.add["plain"]
def test_testmessage():
    """测试TestMessage功能"""
    message = TestMessage(TestMessageType.INFO, "测试内容")
    assert message.type == TestMessageType.INFO
    assert message.content == "测试内容"

    # 测试字典转换
    msg_dict = message.to_dict()
    assert "type" in msg_dict
    assert "content" in msg_dict

    # 测试JSON转换
    msg_json = message.to_json()
    assert isinstance(msg_json, str)


# 测试测试用例类型
@suite.add["plain"]
def test_testcase_types():
    """测试测试用例类型注册"""
    # 检查测试类型是否正确注册
    assert hasattr(suite._test_types, "__getitem__")

    # 检查默认测试类型
    assert "plain" in suite._test_types


# 测试添加输出器
@suite.add["plain"]
def test_add_outputer():
    """测试添加输出器功能"""
    initial_count = len(suite._outputers)

    # 添加新的输出器
    suite.add_outputer(StdOutputer(), StdMessageFormatter("quiet"))

    # 检查输出器是否添加成功
    assert len(suite._outputers) > initial_count

    # 恢复原状
    suite._outputers.pop()


# 运行测试
if __name__ == "__main__":
    suite.run()
