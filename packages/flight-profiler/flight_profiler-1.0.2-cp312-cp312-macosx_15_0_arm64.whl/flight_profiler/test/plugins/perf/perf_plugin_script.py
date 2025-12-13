import math
import time


def process_func():
    time.sleep(1)


print("plugin unit test script started\n", flush=True)

while True:
    j = 0
    for i in range(100000):
        j += math.sqrt(i)
    process_func()
