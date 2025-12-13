import concurrent.futures
import sys
import time


def process_func():
    time.sleep(3)
    return 1


executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

print("plugin unit test script started\n")
sys.stdout.flush()

while True:
    future1 = executor.submit(process_func)
    future1.result()
