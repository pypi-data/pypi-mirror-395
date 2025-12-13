import sys
import time

from flight_profiler.test.plugins.module.module_byimport_script import target_func


def process_func():
    target_func()
    time.sleep(3)
    return 1


print("plugin unit test script started\n")
sys.stdout.flush()

while True:
    process_func()
