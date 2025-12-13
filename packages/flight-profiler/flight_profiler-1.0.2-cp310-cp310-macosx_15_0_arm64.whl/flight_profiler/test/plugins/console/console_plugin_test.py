import os
import time
import unittest

from flight_profiler.test.plugins.profile_integration import ProfileIntegration


class ConsolePluginTest(unittest.TestCase):

    def test_console(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "console_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd("console")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("RemoteInteractiveConsole") >= 0:
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
    test = ConsolePluginTest()
    test.test_console()
