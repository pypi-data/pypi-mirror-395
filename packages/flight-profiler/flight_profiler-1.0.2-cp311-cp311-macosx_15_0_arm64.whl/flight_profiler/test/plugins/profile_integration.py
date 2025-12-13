import os
import threading
import time
import traceback
from subprocess import PIPE, Popen

from flight_profiler.utils.shell_util import get_py_bin_path


class ProfileIntegration:

    def __init__(self):
        self.server_thread = None
        self.server_process = None
        self.client_process = None

    def run_in_thread(self, py_bin_path: str, file: str, timeout: int):
        try:
            self.server_process = Popen(
                [py_bin_path, file],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                bufsize=1,
                text=True,
            )
            self.server_process.wait(timeout=timeout)
        except:
            print(traceback.format_exc())

    def start(self, file: str, timeout: int):
        py_bin_path = get_py_bin_path(os.getpid())
        self.server_thread = threading.Thread(
            target=self.run_in_thread, args=(py_bin_path, file, timeout)
        )
        self.server_thread.start()
        s = time.time()
        while True:
            if self.server_process is not None:
                started = False
                while True:
                    output = self.server_process.stdout.readline()
                    if output:
                        line = str(output)
                        if line.find("plugin unit test script started") >= 0:
                            print()
                            started = True
                            break
                    else:
                        break
                if started:
                    break
            if time.time() - s > timeout:
                raise Exception("start server python process timeout")
            time.sleep(1)

    def stop(self):
        if self.server_process is not None:
            Popen(["kill", "-9", str(self.server_process.pid)]).wait()
        if self.client_process is not None:
            Popen(["kill", "-9", str(self.client_process.pid)]).wait()

    def execute_profile_cmd(self, cmd: str):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        client_py_path = os.path.join(current_directory, "../../client.py")
        py_bin_path = get_py_bin_path(os.getpid())
        self.client_process = Popen(
            [
                py_bin_path,
                str(client_py_path),
                str(self.server_process.pid),
                "--cmd",
                cmd,
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            bufsize=1,
            text=True,
        )
