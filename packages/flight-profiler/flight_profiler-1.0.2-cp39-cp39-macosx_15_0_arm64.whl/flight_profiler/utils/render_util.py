import os
import shutil
from importlib.metadata import version
from typing import List, Optional, Tuple

from flight_profiler.common.expression_result import ExpressionResult

""" Colors
"""
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BOLD = "\033[1m"
COLOR_FAINT = "\033[2m"
COLOR_BG_DARK_BLUE_255 = "\033[48;5;24m"
COLOR_WHITE_255 = "\033[38;5;255m"
COLOR_FUNCTION = COLOR_BG_DARK_BLUE_255 + COLOR_WHITE_255
COLOR_BG_DARK_BROWN_255 = "\033[48;5;94m"
COLOR_AWAIT = COLOR_BG_DARK_BROWN_255 + COLOR_WHITE_255
COLOR_BRIGHT_GREEN = "\033[92m"
COLOR_END = "\033[0m"
COLOR_ORANGE = "\033[38;5;214m"
BANNER_COLOR_RED = "\033[38;5;196m"
BANNER_COLOR_GREEN = "\033[38;5;46m"
BANNER_COLOR_YELLOW = "\033[38;5;226m"
BANNER_COLOR_BLUE = "\033[38;5;39m"
BANNER_COLOR_ORANGE = "\033[38;5;208m"
BANNER_COLOR_PURPLE = "\033[38;5;141m"
BANNER_COLOR_PINK = "\033[38;5;207m"
BANNER_COLOR_CYAN = "\033[38;5;87m"
BANNER_COLOR_LIST = [
    BANNER_COLOR_RED,
    BANNER_COLOR_YELLOW,
    BANNER_COLOR_GREEN,
    BANNER_COLOR_CYAN,
    BANNER_COLOR_PINK,
    BANNER_COLOR_ORANGE,
    BANNER_COLOR_BLUE,
    BANNER_COLOR_PURPLE
]


ENTRANCE_HINTS = [
    ("wiki", "https://github.com/alibaba/PyFlightProfiler/blob/main/docs/WIKI.md"),
    ("version", version("flight_profiler")),
]

EXIT_CODE_HINTS = [
    "SUCCESS",
    "ATTACH_FAILED",
    "GET_REGISTERS_AFTER_ATTACH_FAILED",
    "SET_INJECTED_SHELLCODE_REGISTERS_FAILED",
    "READ_TARGET_MEMORY_FAILED",
    "WRITE_SHELLCODE_TO_TARGET_MEMORY_FAILED",
    "ERROR_IN_EXECUTE_MALLOC",
    "GET_MALLOC_REGISTERS_FAILED",
    "MALLOC_RETURN_ZERO",
    "WRITE_LIBRARY_STR_TO_TARGET_MEMORY_FAILED",
    "ERROR_IN_EXECUTE_DLOPEN",
    "GET_DLOPEN_REGISTERS_FAILED",
    "DLOPEN_RETURN_ZERO",
    "ERROR_IN_EXECUTE_FREE",
    "ERROR_IN_RECOVER_INJECTION",
    "ERROR_IN_VERIFY_SO_LOCATION",
    "ERROR_FLIGHT_SERVER_NO_RESPONSE"
]



def align_prefix(prefix_width: int, source: str, first_line_prefix=None) -> str:
    """
    Transform source string with a constant prefix width from second line.

    Args:
        prefix_width (int): Width of the prefix for alignment
        source (str): Source string to align
        first_line_prefix (Optional[int]): Prefix width for the first line, defaults to prefix_width

    Returns:
        str: Aligned string with proper prefix width
    """
    if first_line_prefix is None:
        first_line_prefix = prefix_width
    terminal_width = shutil.get_terminal_size().columns
    max_length = max(20, terminal_width - prefix_width)
    first_line_max_length = max(20, terminal_width - first_line_prefix)
    space_prefix = " " * prefix_width
    line_source = ""
    for i in range(0, len(source), max_length):
        if i == 0:
            line_source += source[i : min(i + first_line_max_length, len(source))]
        else:
            line_source += space_prefix + source[i : min(i + max_length, len(source))]
    return line_source


def align_json_lines(
    prefix_width: int,
    source: str,
    is_exp_stack: bool = False,
    split_internal_line: bool = True,
) -> str:
    """
    Split multiple lines source and shift all lines with fixed offset.

    Args:
        prefix_width (int): Width of the prefix for alignment
        source (str): Source string to align
        is_exp_stack (bool): Whether the source is an exception stack trace
        split_internal_line (bool): Whether to split internal lines

    Returns:
        str: Aligned string with proper line breaks and prefixes
    """
    lines = source.splitlines()
    terminal_width = shutil.get_terminal_size().columns
    ret = ""
    space_prefix = " " * prefix_width
    for idx, line in enumerate(lines):
        if idx == 0:
            if split_internal_line:
                ret += align_prefix(prefix_width, line)
            else:
                ret += line
        else:
            shift = 0
            while shift < len(line) - 1 and line[shift].isspace():
                shift += 1
            if is_exp_stack:
                ret += f"{' ' * (max(0, min(prefix_width + shift, terminal_width - 20)))}{align_prefix(prefix_width, line[shift:], prefix_width + shift)}"
            else:
                if split_internal_line:
                    ret += f"{' ' * (max(0, min(prefix_width + shift, terminal_width - 20)))}{align_prefix(prefix_width + shift, line[shift:])}"
                else:
                    ret += space_prefix + line
        if idx != len(lines) - 1:
            ret += "\n"
    return ret


def build_long_spy_command_hint(
    module_name: str, class_name: Optional[str], method_name: str, nested_method: Optional[str] = None
) -> str:
    """
    Build a spy command hint message for long-running operations.

    Args:
        module_name (str): Name of the module being spied on
        class_name (Optional[str]): Name of the class being spied on
        method_name (str): Name of the method being spied on
        nested_method (Optional[str]): Name of the nested method being spied on

    Returns:
        str: Formatted spy command hint message
    """
    if class_name is None:
        return f"{COLOR_WHITE_255}Spy was successfully added on [MODULE]: {module_name} [METHOD]: {method_name}, press Ctrl-C to stop.{COLOR_END}"
    else:
        if nested_method is None:
            method_id = f"{method_name}"
        else:
            method_id = f"{method_name}.{nested_method}"
        return (
            f"{COLOR_WHITE_255}Spy was successfully added on [MODULE]: {module_name} [CLASS]: {class_name} [METHOD]: {method_id}"
            f", press Ctrl-C to stop.{COLOR_END}"
        )

def build_colorful_banners() -> None:
    """
    Build and display colorful banners from the banner description file.

    Reads the banner.desc file and renders it with colorful formatting
    using the BANNER_COLOR_LIST colors.
    """
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(os.path.dirname(file_path))
    with open(os.path.join(dir_path, "banner.desc"), "r") as f:
        desc = f.read()
    lines = desc.splitlines()
    space_indices = [0]
    for idx in range(1, len(lines[0])):
        all_space: bool = True
        for j in range(0, len(lines)):
            if idx < len(lines[j]) and lines[j][idx] != " ":
                all_space = False
                break
        if all_space:
            space_indices.append(idx)

    final_rendered_results = []
    for line in lines:
        rendered_display_line = ""
        for idx in range(len(space_indices)):
            if space_indices[idx] >= len(line):
                continue
            if idx < len(space_indices) - 1:
                rendered_display_line += f"{BANNER_COLOR_LIST[idx]}{COLOR_BOLD}{line[space_indices[idx]:space_indices[idx + 1]]}{COLOR_END}"
            else:
                rendered_display_line += f"{BANNER_COLOR_LIST[idx]}{COLOR_BOLD}{line[space_indices[idx]:]}{COLOR_END}"
        final_rendered_results.append(rendered_display_line)
    for line in final_rendered_results:
        print(line)
    print()

def build_title_hints(additional_hints: List[Tuple[str, str]] = None) -> None:
    """
    Build and display title hints with proper alignment.

    Args:
        additional_hints (List[Tuple[str, str]], optional): Additional hints to display
    """
    hints = ENTRANCE_HINTS
    if additional_hints is not None:
        hints.extend(additional_hints)
    max_key_le = 0
    for hint in hints:
        max_key_le = max(max_key_le, len(hint[0]))
    for hint in hints:
        needed_space_cnt = max_key_le - len(hint[0])
        print(f"{COLOR_WHITE_255}{hint[0]}:{' ' * needed_space_cnt} {hint[1]}{COLOR_END}")
    print()


def render_expression_result(result: ExpressionResult) -> str:
    left_offset: int = 20

    if result.failed:
        value_str = (
            f"{COLOR_WHITE_255}  {'EXPR:'.ljust(left_offset)}{align_prefix(left_offset + 2, result.expr)}{COLOR_END}\n"
            f"{COLOR_WHITE_255}  {'FAILED_REASON:'.ljust(left_offset)}{COLOR_END}"
            f"{COLOR_RED}{align_json_lines(left_offset + 2, result.failed_reason, True)}{COLOR_END}"
        )
        return value_str

    value = result.value
    left_offset: int = 12
    value_str = (
        f"{COLOR_WHITE_255}  {'EXPR:'.ljust(left_offset)}{align_prefix(left_offset + 2, result.expr)}{COLOR_END}\n"
        f"{COLOR_WHITE_255}  {'TYPE:'.ljust(left_offset)}{align_prefix(left_offset + 2, result.type)}{COLOR_END}\n"
        f"{COLOR_WHITE_255}  {'VALUE:'.ljust(left_offset)}"
        f"{align_json_lines(left_offset + 2, value, split_internal_line=False)}{COLOR_END}"
    )
    return value_str
