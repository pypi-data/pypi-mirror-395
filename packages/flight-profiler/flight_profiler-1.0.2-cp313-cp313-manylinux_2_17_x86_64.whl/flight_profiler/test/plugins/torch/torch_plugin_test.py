import os
import time
import unittest

from flight_profiler.test.plugins.profile_integration import ProfileIntegration


def torch_profiler_enable() -> bool:
    try:
        from torch.profiler import ProfilerActivity, profile
        assert ProfilerActivity is not None and profile is not None
        import torch
        return torch.cuda.is_available()
    except:
        return False

def torch_memory_snapshot_enable() -> bool:
    try:
        from torch.cuda.memory import memory_snapshot as mm_snapshot
        mm_snapshot()
        return True
    except:
        return False

def torch_memory_record_enable() -> bool:
    try:
        from torch.cuda.memory import _record_memory_history as record_memory_history
        record_memory_history(enabled=None)

        return True
    except:
        return False


class TorchPluginTest(unittest.TestCase):

    @unittest.skipIf(not torch_profiler_enable(), "torch profiler is not enabled")
    def test_torch_profile(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "torch_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd(
                f"torch profile __main__ A forward -f {current_directory}/trace.json"
            )
            process = integration.client_process
            find = False
            start = time.time()
            target_literal: str = "torch profile info has been written to"
            while time.time() - start < 15:
                output = process.stdout.readline()
                if output:
                    line = str(output)
                    if line.find(target_literal) >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
            if os.path.exists(f"{current_directory}/trace.json"):
                os.remove(f"{current_directory}/trace.json")
        except:
            raise
        finally:
            integration.stop()

    @unittest.skipIf(torch_profiler_enable(), "torch profiler is enabled")
    def test_profile_wo_torch(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "torch_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd(
                f"torch profile __main__ A forward -f {current_directory}/trace.json"
            )
            process = integration.client_process
            find = False
            start = time.time()
            target_literal: str = "torch profile is not enabled"
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find(target_literal) >= 0:
                        find = True
                        break

            self.assertTrue(find)
            if os.path.exists(f"{current_directory}/trace.json"):
                os.remove(f"{current_directory}/trace.json")
        except:
            raise
        finally:
            integration.stop()

    @unittest.skipIf(not torch_memory_snapshot_enable(), "torch memory is not enabled.")
    def test_memory_snapshot(self):

        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "torch_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        exp_literal = "not exist"
        try:
            integration.execute_profile_cmd(
                f"torch memory -s -f {current_directory}/snapshot.pickle"
            )
            process = integration.client_process
            find = False
            start = time.time()
            target_literal: str = "torch memory snapshot info has been written to"
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find(target_literal) >= 0 or line.find(exp_literal) >= 0:
                        find = True
                        break

            self.assertTrue(find)
            if os.path.exists(f"{current_directory}/snapshot.pickle"):
                os.remove(f"{current_directory}/snapshot.pickle")
        except:
            raise
        finally:
            integration.stop()

    @unittest.skipIf(torch_memory_snapshot_enable(), "torch memory is enabled.")
    def test_memory_snapshot_wo_torch(self):

        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "torch_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        try:
            integration.execute_profile_cmd(
                f"torch memory -s -f {current_directory}/snapshot.pickle"
            )
            process = integration.client_process
            find = False
            start = time.time()
            target_literal: str = "torch memory snapshot is not enabled"
            exp_literal = "Traceback"
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find(target_literal) >= 0 or line.find(exp_literal) >= 0:
                        find = True
                        break
            self.assertTrue(find)
            if os.path.exists(f"{current_directory}/snapshot.pickle"):
                os.remove(f"{current_directory}/snapshot.pickle")
        except:
            raise
        finally:
            integration.stop()

    @unittest.skipIf(not torch_memory_record_enable(), "torch memory is not enabled.")
    def test_memory_record(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "torch_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        exp_literal = "not_exit"
        try:
            integration.execute_profile_cmd(
                f"torch memory -r __main__ A forward -f {current_directory}/snapshot.pickle"
            )
            process = integration.client_process
            find = False
            start = time.time()
            target_literal: str = "torch memory record info has been written to"
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find(target_literal) >= 0 or line.find(exp_literal) >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
            if os.path.exists(f"{current_directory}/snapshot.pickle"):
                os.remove(f"{current_directory}/snapshot.pickle")
        except:
            raise
        finally:
            integration.stop()

    @unittest.skipIf(torch_memory_record_enable(), "torch memory is enabled.")
    def test_memory_record_wo_torch(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(current_directory, "torch_server_script.py")
        integration = ProfileIntegration()
        integration.start(file, 15)
        exp_literal = "not_exit"
        try:
            integration.execute_profile_cmd(
                f"torch memory -r __main__ A forward -f {current_directory}/snapshot.pickle"
            )
            process = integration.client_process
            find = False
            start = time.time()
            exp_literal = "Traceback"
            target_literal: str = "torch memory record is not enabled"
            while time.time() - start < 15:
                output = process.stdout.readline()
                print(output)
                if output:
                    line = str(output)
                    if line.find(target_literal) >= 0 or line.find(exp_literal) >= 0:
                        find = True
                        break
                else:
                    break

            self.assertTrue(find)
            if os.path.exists(f"{current_directory}/snapshot.pickle"):
                os.remove(f"{current_directory}/snapshot.pickle")
        except:
            raise
        finally:
            integration.stop()
