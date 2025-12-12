import sys
from pathlib import Path
import tempfile
import os

# 添加项目路径到sys.path以导入testlib
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from testlib.suites import AssertTestsuite
from testlib.outputers import StdOutputer
from testlib.formatters import StdMessageFormatter
from testlib.suites import PlainTestsuite
from testlib.outputers import FileOutputer
from testlib.formatters import LogMessageFormatter
from testlib.base import TestMessage, TestMessageType

# 创建测试套件
suite = AssertTestsuite()
suite.add_outputer(StdOutputer(), StdMessageFormatter("normal"))


@suite.add["plain"]
def test_framework_core_components():
    """测试框架核心组件"""
    print("=== 测试框架核心组件 ===")

    # 测试测试套件创建
    suite = AssertTestsuite(name="CoreComponentTest")
    assert suite is not None
    print("✓ 测试套件创建成功")

    # 测试PlainTestsuite
    plain_suite = PlainTestsuite()
    assert plain_suite is not None
    print("✓ PlainTestsuite创建成功")

    # 测试测试套件名称
    assert "CoreComponentTest" in str(suite)
    print("✓ 测试套件名称正确")


@suite.add["plain"]
def test_test_types_functionality():
    """测试各种测试类型的功能"""
    print("\n=== 测试各种测试类型的功能 ===")

    suite = AssertTestsuite()
    suite.add_outputer(StdOutputer(), StdMessageFormatter("quiet"))

    # 测试普通测试 - 成功
    @suite.add["plain"]
    def plain_success():
        return "success"

    # 测试结果测试 - 成功
    @suite.add["result"]("expected")  # type: ignore
    def result_success():
        return "expected"

    # 测试异常测试 - 成功
    @suite.add["exception"](ValueError)  # type: ignore
    def exception_success():
        raise ValueError("expected exception")

    # 测试输出测试 - 成功
    @suite.add["output"]("test output")  # type: ignore
    def output_success():
        print("test output")

    # 运行测试
    suite.run()
    print("✓ 各种测试类型功能正常")


@suite.add["plain"]
def test_outputers_and_formatters():
    """测试输出器和格式化器"""
    print("\n=== 测试输出器和格式化器 ===")

    # 测试StdOutputer
    std_outputer = StdOutputer()
    assert std_outputer is not None
    print("✓ StdOutputer创建成功")

    # 测试FileOutputer
    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tmp:
        tmp_path = tmp.name

    try:
        file_outputer = FileOutputer(tmp_path)
        assert file_outputer is not None
        print("✓ FileOutputer创建成功")

        # 测试文件写入
        test_message = "测试消息内容"
        file_outputer.output(test_message)

        # 验证文件内容
        with open(tmp_path, "r") as f:
            content = f.read()
        assert test_message in content
        print("✓ FileOutputer写入功能正常")

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    # 测试格式化器
    std_formatter = StdMessageFormatter("normal")
    log_formatter_dev = LogMessageFormatter("dev")
    log_formatter_prod = LogMessageFormatter("prod")

    test_msg = TestMessage(TestMessageType.INFO, "测试消息")

    formatted_std = std_formatter.format(test_msg)
    formatted_log_dev = log_formatter_dev.format(test_msg)
    formatted_log_prod = log_formatter_prod.format(test_msg)

    assert isinstance(formatted_std, str)
    assert isinstance(formatted_log_dev, str)
    assert isinstance(formatted_log_prod, str)
    print("✓ 各种格式化器工作正常")


@suite.add["plain"]
def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")

    suite = AssertTestsuite()
    suite.add_outputer(StdOutputer(), StdMessageFormatter("quiet"))

    # 测试空测试套件
    empty_suite = AssertTestsuite()
    empty_suite.add_outputer(StdOutputer(), StdMessageFormatter("quiet"))
    empty_suite.run()
    print("✓ 空测试套件运行正常")

    # 测试无输出器的情况
    no_output_suite = PlainTestsuite()

    @no_output_suite.add["plain"]
    def test_no_output():
        return True

    no_output_suite.run()
    print("✓ 无输出器测试套件运行正常")


@suite.add["plain"]
def test_message_system():
    """测试消息系统"""
    print("\n=== 测试消息系统 ===")

    # 测试TestMessage创建
    msg = TestMessage(TestMessageType.INFO, "测试内容")
    assert msg.type == TestMessageType.INFO
    assert msg.content == "测试内容"
    print("✓ TestMessage创建正常")

    # 测试消息转换
    msg_dict = msg.to_dict()
    assert "type" in msg_dict
    assert "content" in msg_dict
    print("✓ TestMessage字典转换正常")

    msg_json = msg.to_json()
    assert isinstance(msg_json, str)
    print("✓ TestMessage JSON转换正常")


# 运行测试
if __name__ == "__main__":
    suite.run()
