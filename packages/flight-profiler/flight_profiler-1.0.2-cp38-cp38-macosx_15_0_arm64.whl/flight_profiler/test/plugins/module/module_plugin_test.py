import os
import time
import unittest

from flight_profiler.test.plugins.profile_integration import ProfileIntegration


class ModulePluginTest(unittest.TestCase):

    def test_module(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "module_server_script.py")
        byimport_file: str = os.path.join(
            current_directory, "module_byimport_script.py"
        )
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd(f"module {byimport_file}")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("module_byimport_script") >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
        except:
            raise
        finally:
            integration.stop()

    def test_module_main(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "module_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd(f"module {file}")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find("__main__") >= 0:
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
    test = ModulePluginTest()
    test.test_module()
