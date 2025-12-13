import sys
import time


def func(name):
    print("hello func")
    time.sleep(3)
    return name + " " + "console_plugin"


print("plugin unit test script started\n")
sys.stdout.flush()

while True:
    time.sleep(1)
    func("console")
