import sys


class BaseCliPlugin:

    def __init__(self, port, server_pid):
        self.port = port
        self.server_pid = server_pid

    def do_action(self, cmd):
        print(cmd)

    def on_interrupted(self):
        pass

    def get_help(self):
        return None


class QuitCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def do_action(self, cmd):
        sys.exit(1)

    def on_interrupted(self):
        pass
