import sys
import time


class A:

    def forward(self):
        return 1


print("plugin unit test script started\n")
sys.stdout.flush()

instance = A()
while True:
    instance.forward()
    time.sleep(1)
