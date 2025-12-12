from testlib.utils.runner import plainrun, tryrun
from testlib.utils import timer, memory_monitor


@plainrun
def create_large_list0():
    return [i for i in range(100000)]


print(create_large_list0())


@tryrun
def create_large_list_number():
    large_list = [i for i in range(100000)]
    return large_list[1000001]


print(create_large_list_number())


@memory_monitor
def create_large_list1():
    return [i for i in range(100000)]


large_list = create_large_list1()


@timer
def create_large_list2():
    return [i for i in range(100000)]


large_list = create_large_list2()
