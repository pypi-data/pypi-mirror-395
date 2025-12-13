import sys
import time

st = time.time()


print("plugin unit test script started\n")
sys.stdout.flush()
while time.time() - st < 60:
    time.sleep(1)
