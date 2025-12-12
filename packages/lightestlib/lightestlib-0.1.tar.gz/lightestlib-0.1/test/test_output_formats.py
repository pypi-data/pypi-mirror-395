import sys
from pathlib import Path
import tempfile
import os

# 添加项目路径到sys.path以导入testlib
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from testlib.suites import AssertTestsuite
from testlib.outputers import StdOutputer, FileOutputer
from testlib.formatters import StdMessageFormatter, LogMessageFormatter


# 测试不同格式化器的效果
def test_different_formatters():
    """测试不同格式化器"""
    print("=== 测试不同格式化器 ===")

    # 创建测试套件
    AssertTestsuite()

    # 测试标准格式化器的不同模式
    print("\n1. 标准格式化器 - 安静模式:")
    suiteQuiet = AssertTestsuite()
    suiteQuiet.add_outputer(StdOutputer(), StdMessageFormatter("quiet"))

    @suiteQuiet.add["result"](4)  # type: ignore
    def test_add_quiet():
        return 2 + 2

    suiteQuiet.run()

    print("\n2. 标准格式化器 - 正常模式:")
    suiteNormal = AssertTestsuite()
    suiteNormal.add_outputer(StdOutputer(), StdMessageFormatter("normal"))

    @suiteNormal.add["result"](4)  # pyright: ignore[reportCallIssue]
    def test_add_normal():
        return 2 + 2

    suiteNormal.run()

    print("\n3. 标准格式化器 - 详细模式:")
    suiteDetail = AssertTestsuite()
    suiteDetail.add_outputer(StdOutputer(), StdMessageFormatter("detail"))

    @suiteDetail.add["result"](4)  # type: ignore
    def test_add_detail():
        return 2 + 2

    suiteDetail.run()

    print("\n4. 日志格式化器 - 开发模式:")
    suiteLogDev = AssertTestsuite()
    suiteLogDev.add_outputer(StdOutputer(), LogMessageFormatter("dev"))

    @suiteLogDev.add["result"](4)  # type: ignore
    def test_add_logdev():
        return 2 + 2

    suiteLogDev.run()

    print("\n5. 日志格式化器 - 生产模式:")
    suiteLogProd = AssertTestsuite()
    suiteLogProd.add_outputer(StdOutputer(), LogMessageFormatter("prod"))

    @suiteLogProd.add["result"](4)  # type: ignore
    def test_add_logprod():
        return 2 + 2

    suiteLogProd.run()


# 测试文件输出
def test_file_output():
    """测试文件输出功能"""
    print("\n=== 测试文件输出 ===")

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".log") as tmp:
        tmp_path = tmp.name

    try:
        suite = AssertTestsuite()
        suite.add_outputer(FileOutputer(tmp_path), StdMessageFormatter("normal"))

        @suite.add["result"](4)  # type: ignore
        def test_file_output_case():
            return 2 + 2

        suite.run()

        # 检查文件是否创建并包含内容
        with open(tmp_path, "r") as f:
            content = f.read()
            print(f"文件内容:\n{content}")

    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


if __name__ == "__main__":
    test_different_formatters()
    test_file_output()
    print("\n所有测试完成!")
