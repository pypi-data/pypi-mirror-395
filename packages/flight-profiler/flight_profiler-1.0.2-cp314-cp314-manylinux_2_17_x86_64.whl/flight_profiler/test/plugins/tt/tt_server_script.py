import sys
import time


class A:

    def hello(self):
        time.sleep(0.1)
        return func("hello")

    def nested_func(self, v):
        def nested_inner():
            return func(v)
        return nested_inner()



def func(name):
    print("hello func")
    return name + " " + "tt_agent"


print("plugin unit test script started\n")
sys.stdout.flush()

idx = 1
while True:
    A().hello()
    A().nested_func("hello")
    time.sleep(1)
    idx += 1
