import argparse
from argparse import RawTextHelpFormatter

from flight_profiler.common.expression_resolver import InstanceListExprResolver
from flight_profiler.help_descriptions import VMTOOL_COMMAND_DESCRIPTION
from flight_profiler.utils.args_util import rewrite_args, split_regex
from flight_profiler.utils.render_util import COLOR_END, COLOR_ORANGE, COLOR_RED

VMTOOL_ACTION = {"getInstances": True, "forceGc": True}


class VmtoolParams:

    def __init__(
        self, action: str, class_location: str, expr: str, expand: int, limit: int,
        raw_output: bool = False, verbose: bool = False
    ):
        self.action = action
        self.expr = expr
        self.expand = expand
        self.class_location = class_location
        self.limit = limit
        self.raw_output = raw_output
        self.verbose = verbose
        if class_location is None and action == "getInstances":
            raise argparse.ArgumentTypeError(
                f"Invalid class format: {self.class_location}"
            )
        if class_location is not None:
            try:
                class_parts = split_regex(self.class_location)
                self.module_name = class_parts[0]
                self.class_name = class_parts[1]
            except:
                raise argparse.ArgumentTypeError(
                    f"Invalid class format: {self.class_location}"
                )

        if self.action not in VMTOOL_ACTION:
            raise argparse.ArgumentTypeError(
                f"Invalid action: {self.action}, allowed values are "
                f"{COLOR_ORANGE}{'|'.join(VMTOOL_ACTION.keys())}{COLOR_END}{COLOR_RED}."
            )

        self.expression_resolver: InstanceListExprResolver = InstanceListExprResolver(
            self.expr
        )


def check_expand(value):
    try:
        i_value = int(value)
        if i_value < 1 or i_value > 6:
            raise argparse.ArgumentTypeError(f"{value} should be 1 to 6")
        return i_value
    except:
        raise argparse.ArgumentTypeError(f"{value} is not a integer between 1 and 6.")


def check_limit(value):
    try:
        i_value = int(value)
        if i_value < -1:
            raise argparse.ArgumentTypeError(
                f"{value} should be an integer larger than -1."
            )
        return i_value
    except:
        raise argparse.ArgumentTypeError(
            f"{value} should be an integer larger than -1."
        )


class VmtoolArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(VmtoolArgumentParser, self).__init__(
            description=VMTOOL_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument(
            "-a", "--action", required=True, default=None, help="Action to execute."
        )
        self.add_argument(
            "-e",
            "--expr",
            required=False,
            type=str,
            help="instances description expression",
            default="instances",
        )
        self.add_argument(
            "-c", "--class", required=False, default=None, help="instance class type."
        )
        self.add_argument(
            "-x",
            "--expand",
            required=False,
            type=check_expand,
            default=1,
            help="Object represent tree expand level(default 1), max_value is 6.",
        )
        self.add_argument(
            "-r",
            "--raw",
            action="store_true",
            default=False,
            help="display raw format instead of json format.",
        )
        self.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            default=False,
            help="display all the nested items in target list or dict.",
        )
        self.add_argument(
            "-n",
            "--limit",
            required=False,
            type=check_limit,
            default=10,
            help="maximum number of instances to show, -1 means showing all instances.",
        )

    def error(self, message):
        raise Exception(message)

    def parse_params(self, arg_string: str) -> VmtoolParams:
        new_args = rewrite_args(
            arg_string,
            unspec_names=[],
            omit_column=None,
            dash_combine_identifier_group={"c": True, "class": True},
        )
        args = self.parse_args(args=new_args)

        param: VmtoolParams = VmtoolParams(
            action=getattr(args, "action"),
            verbose=getattr(args, "verbose"),
            raw_output=getattr(args, "raw"),
            class_location=getattr(args, "class"),
            expr=getattr(args, "expr"),
            expand=getattr(args, "expand"),
            limit=getattr(args, "limit"),
        )
        return param
