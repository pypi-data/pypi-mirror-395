from testlib.suites import PlainTestsuite
from testlib.outputers import StdOutputer, FileOutputer
from testlib.formatters import logformatter


sample = PlainTestsuite(None, [(StdOutputer(), logformatter.LogMessageFormatter())])
sample = PlainTestsuite()
sample.add_outputer(FileOutputer())


@sample.add["plain"]
def sample_test1():
    print("sample_test1")
    return 1


sample()
