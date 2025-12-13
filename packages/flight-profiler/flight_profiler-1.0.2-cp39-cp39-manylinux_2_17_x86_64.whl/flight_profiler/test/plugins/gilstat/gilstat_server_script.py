import concurrent.futures
import sys
import time


def test_func(i):
    return i + 1


def process_func():
    i = 0
    for j in range(5):
        t = time.time()
        while (time.time() - t) * 1000 < 2:
            i = test_func(i)
    time.sleep(3)


executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

print("plugin unit test script started\n")
sys.stdout.flush()

while True:
    future1 = executor.submit(process_func)
    future2 = executor.submit(process_func)
    future3 = executor.submit(process_func)
    future1.result()
    future2.result()
    future3.result()
