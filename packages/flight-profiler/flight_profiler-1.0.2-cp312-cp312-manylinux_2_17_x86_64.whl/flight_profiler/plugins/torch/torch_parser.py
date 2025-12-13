import argparse
from argparse import ArgumentTypeError, RawTextHelpFormatter
from types import CodeType
from typing import Union

from flight_profiler.common.enter_exit_command import EnterExitCommand
from flight_profiler.help_descriptions import TORCH_COMMAND_DESCRIPTION
from flight_profiler.plugins.server_plugin import Message
from flight_profiler.utils.args_util import rewrite_args, split_regex
from flight_profiler.utils.render_util import (
    COLOR_END,
    COLOR_GREEN,
    COLOR_ORANGE,
    COLOR_RED,
    COLOR_WHITE_255,
)
from flight_profiler.utils.shell_util import complete_full_path

TORCH_ACTIONS: dict = {"profile": 1, "memory": 1}


class BaseTorchCommand(EnterExitCommand):

    def __init__(self, action: str):
        super().__init__(limit=1)
        self.action = action

        if action not in TORCH_ACTIONS:
            raise argparse.ArgumentTypeError(
                f"Invalid action: {self.action}, allowed values are "
                f"{COLOR_ORANGE}{'|'.join(TORCH_ACTIONS.keys())}{COLOR_END}{COLOR_RED}."
            )

    def is_profile(self) -> bool:
        return self.action == "profile"

    def is_memory(self) -> bool:
        return self.action == "memory"

    def dump_success(self):
        pass

    def dump_error(self, error_msg):
        pass


class TorchProfileCommand(BaseTorchCommand):

    def __init__(
        self, module_name: str, class_name: str, method_name: str, file_path: str,
        nested_method: str = None,
        need_wrap_nested_inplace: bool = False,
        nested_code_obj: CodeType = None
    ):
        super().__init__("profile")
        self.module_name = module_name
        self.class_name = class_name
        self.method_name = method_name
        self.filepath = complete_full_path(file_path, default_suffix="trace.json")
        self.nested_method = nested_method
        self.need_wrap_nested_inplace = need_wrap_nested_inplace
        self.nested_code_obj = nested_code_obj

        if not self.filepath.endswith(".json"):
            raise argparse.ArgumentTypeError(
                f"invalid filepath format, profile only supports dump to "
                f"{COLOR_ORANGE}.json{COLOR_END}{COLOR_RED} files."
            )

    def dump_error(self, error_msg: str):
        self.out_q.output_msg_nowait(
            Message(
                is_end=True, msg=f"{COLOR_RED}{error_msg}{COLOR_END}"
            )
        )

    def dump_success(self):
        self.out_q.output_msg_nowait(
            Message(
                is_end=True,
                msg=f"{COLOR_WHITE_255}"
                f"torch profile info has been written to {COLOR_GREEN}{self.filepath}{COLOR_END}{COLOR_WHITE_255} successfully.{COLOR_END}",
            )
        )


class TorchMemoryCommand(BaseTorchCommand):

    def __init__(self, snapshot: bool, record: str, file_path: str = None,
                 nested_method: str = None,
                 need_wrap_nested_inplace: bool = False,
                 nested_code_obj: CodeType = None
                 ):
        super().__init__("memory")
        self.snapshot = snapshot
        self.record = record
        self.filepath = complete_full_path(file_path, default_suffix="snapshot.pickle")
        self.nested_method = nested_method
        self.need_wrap_nested_inplace = need_wrap_nested_inplace
        self.nested_code_obj = nested_code_obj

        if not self.filepath.endswith(".pickle"):
            raise argparse.ArgumentTypeError(
                f"invalid filepath format, memory only supports dump to "
                f"{COLOR_ORANGE}.json{COLOR_END}{COLOR_RED} files."
            )

        self.__check()

    def __check(self):
        if self.snapshot and self.record is not None:
            raise argparse.ArgumentTypeError(
                "not allowed to specify -s and -r at the same time."
            )

        if not self.snapshot and self.record is None:
            raise argparse.ArgumentTypeError("please specifying -s or -r at least.")

        if self.record is not None:
            func_location = split_regex(self.record)
            self.module_name = func_location[0]
            if len(func_location) == 2:
                self.class_name = None
                self.method_name = func_location[1]
            elif len(func_location) == 3:
                self.class_name = func_location[1]
                self.method_name = func_location[2]
            else:
                raise argparse.ArgumentTypeError(
                    f"invalid record format: {self.record}"
                )

    def dump_error(self, error_msg: str):
        self.out_q.output_msg_nowait(
            Message(
                is_end=True, msg=f"{COLOR_RED}{error_msg}{COLOR_END}"
            )
        )

    def dump_success(self, m_type: str = ""):
        self.out_q.output_msg_nowait(
            Message(
                is_end=True,
                msg=f"{COLOR_WHITE_255}"
                f"torch memory {m_type} info has been written to {COLOR_GREEN}{self.filepath}{COLOR_END}{COLOR_WHITE_255} successfully.{COLOR_END}",
            )
        )


class TorchProfileArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(TorchProfileArgumentParser, self).__init__(
            description=TORCH_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument("--mod", required=True, help="module package")
        self.add_argument("--cls", required=False, help="class name")
        self.add_argument("--func", required=True, help="function name")

        self.add_argument("-nm", "--nested-method", required=False, help="nested method")
        self.add_argument(
            "-f",
            "--filepath",
            required=False,
            default=None,
            help="dump profile info to filepath.",
        )

    def error(self, message):
        raise Exception(message)

    def parse_profile_cmd(self, arg_string: str) -> TorchProfileCommand:
        new_args = rewrite_args(
            arg_string, unspec_names=["mod", "cls", "func"], omit_column="cls"
        )
        args = self.parse_args(args=new_args)
        cmd: TorchProfileCommand = TorchProfileCommand(
            module_name=getattr(args, "mod"),
            class_name=getattr(args, "cls"),
            method_name=getattr(args, "func"),
            file_path=getattr(args, "filepath"),
            nested_method=getattr(args, "nested_method"),
        )
        return cmd


class TorchMemoryArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(TorchMemoryArgumentParser, self).__init__(
            description=TORCH_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False


        self.add_argument("-nm", "--nested-method", required=False, help="nested method")
        self.add_argument(
            "-s",
            "--snapshot",
            required=False,
            action="store_true",
            default=False,
            help="capture torch memory snapshot.",
        )
        self.add_argument(
            "-r",
            "--record",
            required=False,
            default=None,
            help="record memory usage during method execution.",
        )
        self.add_argument(
            "-f",
            "--filepath",
            required=False,
            default=None,
            help="dump memory usage info to filepath.",
        )

    def error(self, message):
        raise Exception(message)

    def parse_memory_cmd(self, arg_string: str) -> TorchMemoryCommand:
        new_args = rewrite_args(
            arg_string,
            unspec_names=[],
            omit_column=None,
            dash_combine_identifier_group={"r": True, "record": True},
        )

        args = self.parse_args(args=new_args)
        cmd: TorchMemoryCommand = TorchMemoryCommand(
            snapshot=getattr(args, "snapshot"),
            record=getattr(args, "record"),
            file_path=getattr(args, "filepath"),
            nested_method=getattr(args, "nested_method"),
        )
        return cmd


def parse_torch_cmd(
    cmd: str,
) -> Union[BaseTorchCommand, TorchProfileCommand, TorchMemoryCommand]:
    cmd = cmd.strip()
    params = split_regex(cmd)
    if len(params) == 0:
        raise ArgumentTypeError(
            f"Invalid torch command format, type {COLOR_ORANGE}`torch -h`{COLOR_END}{COLOR_RED} for detail."
        )

    if params[0] == "profile":
        return TorchProfileArgumentParser().parse_profile_cmd(cmd[len(params[0]) :])
    elif params[0] == "memory":
        return TorchMemoryArgumentParser().parse_memory_cmd(cmd[len(params[0]) :])
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid action: {params[0]}, allowed values are "
            f"{COLOR_ORANGE}{'|'.join(TORCH_ACTIONS.keys())}{COLOR_END}{COLOR_RED}."
        )
