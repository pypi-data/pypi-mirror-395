import argparse
from argparse import RawTextHelpFormatter

from flight_profiler.help_descriptions import WATCH_COMMAND_DESCRIPTION
from flight_profiler.plugins.watch import watch_agent
from flight_profiler.utils.args_util import rewrite_args


def check_expand(value):
    try:
        i_value = int(value)
        if i_value == -1:
            return -1
        if i_value < 1 or i_value > 4:
            raise argparse.ArgumentTypeError(f"{value} should be 1 to 4, or -1")
        # profile property contains two levels
        return i_value + 2
    except:
        raise argparse.ArgumentTypeError(f"{value} is not a integer between 1 and 4.")


class WatchArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(WatchArgumentParser, self).__init__(
            description=WATCH_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument("--pkg", required=True, help="module package")
        self.add_argument("--cls", required=False, help="class name")
        self.add_argument("--func", required=True, help="function name")
        self.add_argument("-nm", "--nested-method", required=False, help="nested method")
        self.add_argument(
            "--expr", required=False, help="watch expression", default="args,kwargs"
        )
        self.add_argument("-f", "--filter", required=False, help="filter expression")
        self.add_argument(
            "-e",
            "--exception",
            action="store_true",
            default=False,
            help="record when method throws exception",
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
            "-x",
            "--expand",
            required=False,
            type=check_expand,
            default=1 + 2,
            help="Object represent tree expand level(default 1), max_value is 4.",
        )
        self.add_argument(
            "-n",
            "--limits",
            required=False,
            type=int,
            default=10,
            help="max display count",
        )

    def error(self, message):
        raise Exception(message)

    def parse_watch_setting(self, arg_string: str):
        new_args = rewrite_args(
            arg_string, unspec_names=["pkg", "cls", "func"], omit_column="cls"
        )
        args = self.parse_args(args=new_args)
        watch_setting = watch_agent.WatchSetting(
            module_name=getattr(args, "pkg"),
            class_name=getattr(args, "cls"),
            method_name=getattr(args, "func"),
            nested_method=getattr(args, "nested_method"),
            watch_expr=getattr(args, "expr"),
            raw_output=getattr(args, "raw"),
            filter_expr=getattr(args, "filter"),
            record_on_exception=getattr(args, "exception"),
            expand_level=getattr(args, "expand"),
            verbose=getattr(args, "verbose"),
            max_count=getattr(args, "limits"),
        )
        return watch_setting
