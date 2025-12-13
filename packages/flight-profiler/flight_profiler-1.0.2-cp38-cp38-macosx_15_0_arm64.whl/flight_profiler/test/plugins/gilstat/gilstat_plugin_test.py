import os
import time
import unittest

from flight_profiler.test.plugins.profile_integration import ProfileIntegration


class GilStatPluginTest(unittest.TestCase):

    def test_gil_stat(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "gilstat_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 20)
        try:
            integration.execute_profile_cmd("gilstat on 1000 1000 2")
            process = integration.client_process

            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("gil statistics report:") >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
        except:
            raise
        finally:
            integration.stop()

    def test_gil_warning(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "gilstat_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 20)
        try:
            integration.execute_profile_cmd("gilstat on 1 1 2")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 20:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("gil warning report:") >= 0:
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
    test = GilStatPluginTest()
    test.test_gil_stat()
    test.test_gil_warning()
