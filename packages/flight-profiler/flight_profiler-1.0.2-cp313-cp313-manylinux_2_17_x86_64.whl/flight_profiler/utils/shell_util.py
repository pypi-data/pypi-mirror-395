import os
import subprocess
from subprocess import CalledProcessError
from typing import List, Optional, Union


def execute_process(cmds: List[str]):
    """
    Execute a process with the given commands.

    Args:
        cmds (List[str]): Command list to execute

    Returns:
        subprocess.CompletedProcess or CalledProcessError: Process result or error
    """
    try:
        result = subprocess.run(cmds, check=True, capture_output=True, text=True)
    except CalledProcessError as ex:
        return ex
    if result is None:
        return None
    return result


def execute_shell(shell_path: str, cmds: List[str]) -> Optional[str]:
    """
    Execute shell commands.

    Args:
        shell_path (str): Path to the shell script
        cmds (List[str]): Commands to execute

    Returns:
        Optional[str]: Standard output of the command or None if failed
    """
    if not os.path.exists(shell_path):
        return None
    result = execute_process(cmds)
    if result is None:
        return None
    return result.stdout


def get_py_bin_path(target_pid: Union[int, str]) -> str:
    """
    Get Python binary path for the target process.

    Args:
        target_pid (Union[int, str]): Target process ID

    Returns:
        str: Python binary path
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    shell_path = os.path.join(current_directory, "../shell/resolve_bin_path.sh")
    # get current python binary path
    py_bin_path = execute_shell(shell_path, [str(shell_path), str(target_pid)])
    return str(py_bin_path).strip()


def complete_full_path(filepath: str, default_suffix: str) -> str:
    """
    Expand filepath with absolute path.

    Args:
        filepath (str): File path to expand
        default_suffix (str): Default suffix to append if filepath is None

    Returns:
        str: Absolute file path
    """
    if filepath is not None:
        return os.path.abspath(os.path.expanduser(filepath))
    else:
        cwd_path: str = os.getcwd()
        if cwd_path.endswith("/"):
            return f"{cwd_path}{default_suffix}"
        else:
            return f"{cwd_path}/{default_suffix}"

def resolve_symbol_address(symbol: str, pid: int) -> Optional[int]:
    """
    Resolve symbol address for the given symbol and process ID.

    Args:
        symbol (str): Symbol to resolve
        pid (int): Process ID

    Returns:
        Optional[int]: Symbol address or None if not found
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    shell_path = os.path.join(current_directory, "../shell/resolve_symbol.sh")
    # get symbol address like: 0000000100181050
    output = execute_shell(shell_path, [str(shell_path), str(pid), str(symbol)])
    if output is None:
        return None
    return int(output, 16)
