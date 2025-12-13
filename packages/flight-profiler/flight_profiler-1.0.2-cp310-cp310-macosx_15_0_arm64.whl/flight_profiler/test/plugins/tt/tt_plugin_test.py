import os
import time
import unittest

from flight_profiler.test.plugins.profile_integration import ProfileIntegration


class TimeTunnelPluginTest(unittest.TestCase):

    def test_tt_module_method(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "tt_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd("tt -t __main__ func")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if (
                        line.find("INDEX") >= 0
                        and line.find("COST") >= 0
                        and line.find("MODULE") >= 0
                        and line.find("METHOD") >= 0
                    ):
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
        except:
            raise
        finally:
            integration.stop()

    def test_tt_class_method(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "tt_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd("tt -t __main__ A hello")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if (
                        line.find("INDEX") >= 0
                        and line.find("COST") >= 0
                        and line.find("MODULE") >= 0
                        and line.find("METHOD") >= 0
                    ):
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
        except:
            raise
        finally:
            integration.stop()

    def test_tt_class_nested_method(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "tt_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd("tt -t __main__ A nested_func -nm nested_inner")
            process = integration.client_process
            find = False
            start = time.time()
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if (
                        line.find("INDEX") >= 0
                        and line.find("COST") >= 0
                        and line.find("MODULE") >= 0
                        and line.find("METHOD") >= 0
                    ):
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
        except:
            raise
        finally:
            integration.stop()
