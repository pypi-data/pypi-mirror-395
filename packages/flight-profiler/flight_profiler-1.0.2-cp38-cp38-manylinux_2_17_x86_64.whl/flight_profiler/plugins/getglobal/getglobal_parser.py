import argparse
from argparse import RawTextHelpFormatter
from typing import Optional

from flight_profiler.common.expression_resolver import InstanceExprResolver
from flight_profiler.help_descriptions import GETGLOBAL_COMMAND_DESCRIPTION
from flight_profiler.utils.args_util import rewrite_args


class GetGlobalParams:

    def __init__(
        self,
        module_name: str,
        class_name: Optional[str],
        expr: str,
        variable: str,
        expand_level: int = 1,
        raw_output: bool = False,
        verbose: bool = False,
    ):
        self.module_name = module_name
        self.class_name = class_name
        self.variable = variable
        self.expr = expr
        self.verbose = verbose
        self.expand_level = expand_level
        if expand_level == -1:
            self.expand_level = None
        self.raw_output = raw_output
        self.expr_resolver: InstanceExprResolver = InstanceExprResolver(self.expr)


def check_expand(value):
    try:
        i_value = int(value)
        if i_value == -1:
            return -1
        if i_value < 1 or i_value > 6:
            raise argparse.ArgumentTypeError(f"{value} should be 1 to 6")
        # profile property contains two levels
        return i_value
    except:
        raise argparse.ArgumentTypeError(f"{value} is not a integer between 1 and 6.")


class GetGlobalParser(argparse.ArgumentParser):

    def __init__(self):
        super(GetGlobalParser, self).__init__(
            description=GETGLOBAL_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument("--mod", required=True, help="module package")
        self.add_argument("--cls", required=False, help="class name")
        self.add_argument("--var", required=True, help="variable name")
        self.add_argument(
            "-x",
            "--expand",
            required=False,
            type=check_expand,
            default=2,
            help="Object represent tree expand level(default 2), max_value is 6.",
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
            "-e",
            "--expr",
            required=False,
            type=str,
            default="target",
            help="instance expression",
        )

    def error(self, message):
        raise Exception(message)

    def parse_getglobal_params(self, arg_string: str) -> GetGlobalParams:
        new_args = rewrite_args(
            arg_string, unspec_names=["mod", "cls", "var"], omit_column="cls"
        )
        args = self.parse_args(args=new_args)
        return GetGlobalParams(
            module_name=getattr(args, "mod"),
            class_name=getattr(args, "cls"),
            variable=getattr(args, "var"),
            raw_output=getattr(args, "raw"),
            expand_level=getattr(args, "expand"),
            verbose=getattr(args, "verbose"),
            expr=getattr(args, "expr"),
        )
