import os
import time
import unittest

from flight_profiler.test.plugins.profile_integration import ProfileIntegration


class HelpPluginTest(unittest.TestCase):

    def test_help(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "help_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd("help")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("NAME") >= 0 and line.find("DESCRIPTION") >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
        except:
            raise
        finally:
            integration.stop()

    def test_help_command(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "help_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd("help watch")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("USAGE") >= 0:
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
    test = HelpPluginTest()
    test.test_help()
    test.test_help_command()
