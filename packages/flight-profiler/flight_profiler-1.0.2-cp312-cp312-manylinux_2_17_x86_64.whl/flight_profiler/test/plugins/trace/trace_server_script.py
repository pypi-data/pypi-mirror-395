import sys
import time


class A:
    cls_dict = {"hello": 33}

    def hello(self):
        time.sleep(0.1)
        return test_func("hello")


    def nested_hello(self, v):
        def nested_inner():
            time.sleep(0.1)
            test_func(v)
            return test_func("hello")
        return nested_inner()

    def depth_call3(self):
        return "hello world!"

    def depth_call2(self):
        return self.depth_call3()

    def depth_call1(self):
        return self.depth_call2()

    def depth_call(self):
        return self.depth_call1()


def test_func(name):
    print("hello func")
    return name + " " + "trace_agent"


print("plugin unit test script started\n")
sys.stdout.flush()

idx = 1
while True:
    A().hello()
    A().depth_call()
    A().nested_hello("hello")
    time.sleep(1)
    idx += 1
