import sys
import time

print("plugin unit test script started\n")
sys.stdout.flush()

s = time.time()
while time.time() - s < 60:
    kv = dict()
    kv["k1"] = list()
    for i in range(1000):
        kv["k1"].append(i)
    for i in range(100):
        kv[str(i)] = str(i)
    time.sleep(1)
