import os
import time
import unittest

from flight_profiler.client import READLINE_AVAILABLE
from flight_profiler.test.plugins.profile_integration import ProfileIntegration

try:
    import readline
    READLINE_AVAILABLE = readline is not None
except ImportError:
    READLINE_AVAILABLE = False

@unittest.skipIf(not READLINE_AVAILABLE, "readline is not enabled in current python env.")
class HistoryPluginTest(unittest.TestCase):

    def test_history(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "history_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd("history -n 1")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("history -n 1") >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
        except:
            raise
        finally:
            integration.stop()


if __name__ == "__main__":
    test = HistoryPluginTest()
    test.test_history()
