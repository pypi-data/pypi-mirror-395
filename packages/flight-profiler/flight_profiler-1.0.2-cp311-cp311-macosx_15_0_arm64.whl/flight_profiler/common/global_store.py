GLOBAL_INJECT_SERVER_PID = -1
GLOBAL_HISTORY_FILE_PATH = ""

FORBIDDEN_COMMANDS_IN_PY314 = {
    "perf"
}

def set_history_file_path(path: str):
    """
    init history file path
    """
    global GLOBAL_HISTORY_FILE_PATH
    GLOBAL_HISTORY_FILE_PATH = path


def get_history_file_path() -> str:
    global GLOBAL_HISTORY_FILE_PATH
    return GLOBAL_HISTORY_FILE_PATH


def set_inject_server_pid(pid: int):
    """
    based on session
    """
    global GLOBAL_INJECT_SERVER_PID
    GLOBAL_INJECT_SERVER_PID = pid


def get_inject_server_pid() -> int:
    """
    return current session pid
    """
    global GLOBAL_INJECT_SERVER_PID
    return GLOBAL_INJECT_SERVER_PID
