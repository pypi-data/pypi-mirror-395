from testlib.suites import AssertTestsuite
from testlib.outputers import FileOutputer, StdOutputer
from testlib.formatters import LogMessageFormatter, StdMessageFormatter

sample = AssertTestsuite()
sample.add_outputer(FileOutputer(), LogMessageFormatter("prod"))
sample.add_outputer(StdOutputer(), StdMessageFormatter("quiet"))


@sample.add["plain"]
def sample_test1():
    print("sample_test1")
    return 1


@sample.add["result"](2)  # type: ignore
def sample_test2():
    print("sample_test2")
    return 2


@sample.add["result"](result=2)  # type: ignore
def sample_test3():
    print("sample_test3")
    return 3


@sample.add["exception"]()  # type: ignore
def sample_test4():
    print("sample_test4")
    raise Exception("sample_test4")


@sample.add["exception"](ZeroDivisionError)  # type: ignore
def sample_test5():
    print("sample_test5")
    i = 1 / 0
    return i


@sample.add["exception"](KeyError)  # type: ignore
def sample_test6():
    print("sample_test6")
    i = 1 / 0
    return i


@sample.add["output"]("sample_test6")  # type: ignore
def sample_test7():
    print("sample_test7")
    i = 1 / 0
    return i


@sample.add["output"]("sample_test8")  # type: ignore
def sample_test8():
    print("sample_test8")


sample()
