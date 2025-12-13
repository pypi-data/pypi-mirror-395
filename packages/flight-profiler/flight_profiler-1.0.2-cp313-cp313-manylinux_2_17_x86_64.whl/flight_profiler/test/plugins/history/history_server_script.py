import sys
import time


class A:
    cls_dict = {"hello": 33}

    def __init__(self):
        pass


global_a = 10

print("plugin unit test script started\n")
sys.stdout.flush()

idx = 1
while True:
    A()
    time.sleep(1)
    idx += 1
