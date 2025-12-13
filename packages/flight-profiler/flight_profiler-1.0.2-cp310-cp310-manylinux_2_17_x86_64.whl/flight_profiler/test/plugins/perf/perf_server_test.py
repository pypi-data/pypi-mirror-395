import os
import sys
import time
import unittest

from flight_profiler.test.plugins.profile_integration import ProfileIntegration
from flight_profiler.utils.env_util import is_linux


@unittest.skipIf(sys.version_info >= (3, 14), "Perf not supported in Python 3.14+")
class PerfPluginTest(unittest.TestCase):


    def test_perf(self):
        if not is_linux():
            # OSX need privilege, skip
            return
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "perf_plugin_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd(
                f"perf -d 5 -f {current_directory}/application.svg"
            )
            process = integration.client_process
            find = False
            start = time.time()
            target_literal: str = "Flamegraph data has been successfully"
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find(target_literal) >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
            os.remove(f"{current_directory}/application.svg")
        except:
            raise
        finally:
            integration.stop()


if __name__ == "__main__":
    test = PerfPluginTest()
    test.test_perf()
