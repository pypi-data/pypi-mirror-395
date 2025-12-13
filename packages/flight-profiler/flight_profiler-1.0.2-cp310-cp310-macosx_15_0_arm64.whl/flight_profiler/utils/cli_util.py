import pickle
import sys
from typing import Union

from flight_profiler.common.expression_result import ExpressionResult
from flight_profiler.communication.flight_client import FlightClient
from flight_profiler.utils.render_util import (
    COLOR_BRIGHT_GREEN,
    COLOR_END,
    COLOR_RED,
    COLOR_WHITE_255,
    EXIT_CODE_HINTS,
    render_expression_result,
)


def show_error_info(msg: str) -> None:
    """
    Display error information with red color.

    Args:
        msg (str): Error message to display
    """
    print(f"{COLOR_RED}{msg}{COLOR_END}")


def show_normal_info(msg: str) -> None:
    """
    Display normal information with white color.

    Args:
        msg (str): Message to display
    """
    print(f"{COLOR_WHITE_255}{msg}{COLOR_END}")

def verify_exit_code(exit_code: int, pid: Union[int, str]) -> None:
    """
    Verify the exit code and display appropriate error messages.

    Args:
        exit_code (int): Exit code from the process
        pid (Union[int, str]): Process ID for error context
    """
    if exit_code == 0:
        return

    print(f"[ERROR]❌ PyFlightProfiler attach failed, reason: {COLOR_RED}{EXIT_CODE_HINTS[exit_code]}{COLOR_END}!")
    if exit_code == 10 or exit_code == 16:
        print(f"\nHint: This error is likely due to target process holds global interpreter lock and never releases it. We highly recommend you to use \n  `{COLOR_BRIGHT_GREEN}pystack remote "
              f"{pid}{COLOR_END}` or \n  `{COLOR_BRIGHT_GREEN}pystack remote {pid} --native{COLOR_END}` to find out which thread is stuck in gil scope.\n")
    exit(1)

def common_plugin_execute_routine(
    cmd: str,
    param: str,
    port: int,
    raw_text: bool = False,
    expression_result: bool = False,
) -> None:
    """
    Performs normal cli plugin request and render routines, should be called at the end of plugin action.

    Args:
        cmd (str): Command to execute
        param (str): Parameters for the command
        port (int): Port number for the flight client
        raw_text (bool): Whether to treat response as raw text
        expression_result (bool): Whether to process as expression result
    """
    body = {
        "target": cmd,
        "param": param
    }
    try:
        client = FlightClient(host="localhost", port=port)
    except:
        show_error_info("Target process exited!")
        return
    try:
        for line in client.request_stream(body):
            if not expression_result:
                if line:
                    if raw_text:
                        line = line.decode("utf-8")
                    else:
                        line = pickle.loads(line)
                    # Handle newline messages
                    show_normal_info(line)
            else:
                result: Union[ExpressionResult, str] = pickle.loads(
                    line
                )
                if type(result) is str:
                    print(result)
                else:
                    print(
                        render_expression_result(
                            result
                        )
                    )
            sys.stdout.flush()
    finally:
        client.close()
