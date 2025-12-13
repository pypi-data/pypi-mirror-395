import sys
import time


class A:
    cls_dict = {"hello": 33}

    def hello(self):
        time.sleep(0.1)
        return test_func("hello")


def test_func(name):
    print("hello func")
    return name + " " + "trace_agent"


print("plugin unit test script started\n")
sys.stdout.flush()

idx = 1
a = A()
while True:
    a.hello()
    time.sleep(1)
    idx += 1
