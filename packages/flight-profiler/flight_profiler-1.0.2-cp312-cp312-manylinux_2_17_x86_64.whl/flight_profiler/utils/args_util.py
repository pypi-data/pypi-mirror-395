import re
from typing import Dict, List, Optional, Tuple


def split_regex(input_text: str) -> List[str]:
    """
    Split input string by whitespace characters.

    Args:
        input_text (str): The input string to split

    Returns:
        List[str]: A list of non-empty strings split by whitespace
    """
    input_text = input_text.strip()
    if len(input_text) == 0:
        return []
    input_split = re.split(r"\s+", input_text)
    ret = []
    for p in input_split:
        if len(p) > 0:
            ret.append(p)
    return ret


def split_space_brackets(text) -> List[str]:
    """
    Split text by spaces and brackets, preserving bracketed content.

    example:
        text: This is a {sunny } uday
        return: [This, is, a, {sunny } uday]

    :return: token list
    """
    pattern = r"""
        \s*
        (
            \{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}
            |
            \[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\]
            |
            [^\s\{\}\[\]]+
        )
        \s*
    """
    return re.findall(pattern, text, re.VERBOSE)

def rewrite_args(
    arg_string: str,
    unspec_names: List[str],
    omit_column: Optional[str],
    dash_combine_identifier_group: Dict[str, bool] = None,
) -> List[str]:
    """
    Rewrite input raw arg string to specified tokens, now only used by watch & getglobal parser.

    Args:
        arg_string (str): Input arguments
        unspec_names (List[str]): Unspecified args name, ordered
        omit_column (Optional[str]): At most one column can be omitted
        dash_combine_identifier_group (Dict[str, bool]): Identifier group that args should be combined

    Returns:
        List[str]: All specified args tokens
    """
    # divide arg_string to specified args and unspecified args
    arg_string = " " + arg_string
    try:
        unspecified_index = arg_string.index(" -")
    except ValueError:
        # no specified args, use total string as whole
        unspecified_index = len(arg_string)
    unspecified_args_str: str = ""
    if unspecified_index > 0:
        unspecified_args_str: str = arg_string[:unspecified_index]

    # specified args
    specified_args = []
    spec_kv: Dict[str, bool] = {}
    if unspecified_index >= 0 and unspecified_index < len(arg_string):
        # no specified args:
        spec_kv, specified_args = split_dash_args(
            arg_string[unspecified_index:], dash_combine_identifier_group
        )

    # unspecified args
    for idx in range(len(unspec_names) - 1, -1, -1):
        if unspec_names[idx] in spec_kv:
            unspec_names.pop(idx)
        else:
            # illegal to use --cls class_name func_name, so quit
            break
    new_unspecified_args: List[str] = []
    unspecified_args_str = unspecified_args_str.strip()
    if len(unspecified_args_str) > 0:
        unspecified_args: List[str] = split_space_brackets(unspecified_args_str)
        # cls can be omited
        if len(unspecified_args) == len(unspec_names):
            for idx in range(len(unspecified_args)):
                new_unspecified_args.append("--" + unspec_names[idx])
                new_unspecified_args.append(unspecified_args[idx])
        elif len(unspecified_args) == len(unspec_names) - 1:
            unspec_names.remove(omit_column)
            for idx in range(len(unspecified_args)):
                new_unspecified_args.append("--" + unspec_names[idx])
                new_unspecified_args.append(unspecified_args[idx])
        else:
            raise ValueError(
                "usage: command var1 var2 var3 or "
                "command var1 --name2 var2 --name3 var3"
            )

    return new_unspecified_args + specified_args


def split_dash_args(
    arg_str: str, dash_combine_identifier_group: Dict[str, bool]
) -> Tuple[Dict[str, bool], List[str]]:
    """
    Convert args concat by single dash or double dash to List args, combine args within dash which keys are in dash_combine_identifier_group.

    Example:
        --params_filter "args[0][\"hello\"] == \"wor ld\""
        -t module class method
    Return:
        ['--params_filter', 'args[0]["hello"] == "wor ld"']
        ['-t', 'module class method'] if 't' in #dash_combine_identifier_group

    Args:
        arg_str (str): Input arguments
        dash_combine_identifier_group (Dict[str, bool]): Identifier group that args should be combined

    Returns:
        Tuple[Dict[str, bool], List[str]]: All specified args tokens
    """
    return_args: List[str] = []
    idx = 0
    spec_kv: Dict[str, bool] = dict()

    while idx < len(arg_str):
        # extract one kv arg every loop
        if arg_str[idx].isspace():
            idx += 1
            continue

        # -key/--key
        if arg_str[idx] == "-":
            shift_idx = idx + 1
            while shift_idx < len(arg_str) and not arg_str[shift_idx].isspace():
                shift_idx += 1
            identifier = ""
            if idx + 1 < len(arg_str):
                if arg_str[idx + 1] == "-":
                    if idx + 2 < len(arg_str):
                        identifier = arg_str[(idx + 2) : shift_idx]
                else:
                    identifier = arg_str[(idx + 1) : shift_idx]
            return_args.append(arg_str[idx:shift_idx])
            idx = shift_idx
            if len(identifier) > 0:
                spec_kv[identifier] = True
                if (
                    dash_combine_identifier_group is not None
                    and identifier in dash_combine_identifier_group
                ):
                    # combine args until meet -
                    # remove space
                    shift_idx = idx
                    while shift_idx < len(arg_str) and arg_str[shift_idx].isspace():
                        shift_idx += 1
                    idx = shift_idx
                    while shift_idx < len(arg_str) and arg_str[shift_idx] != "-":
                        shift_idx += 1
                    if idx < len(arg_str):
                        return_args.append(arg_str[idx:shift_idx])
                    idx = shift_idx
            continue

        if arg_str[idx] == "'" or arg_str[idx] == '"':
            # in quotes
            shift_idx = idx + 1
            left_quote: str = arg_str[idx]
            while shift_idx < len(arg_str):
                # enable space
                if arg_str[shift_idx] == left_quote and arg_str[shift_idx - 1] != "\\":
                    break
                else:
                    shift_idx += 1
            if idx + 1 < shift_idx:
                return_args.append(
                    arg_str[(idx + 1) : shift_idx].encode().decode("unicode_escape")
                )
            idx = shift_idx + 1
        else:
            # normal character, cannot enable space
            shift_idx = idx + 1
            while shift_idx < len(arg_str) and not arg_str[shift_idx].isspace():
                shift_idx += 1
            return_args.append(arg_str[idx:shift_idx])
            idx = shift_idx

    return spec_kv, return_args
