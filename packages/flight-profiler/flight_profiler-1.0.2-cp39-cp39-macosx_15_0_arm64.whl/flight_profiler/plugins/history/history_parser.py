import argparse
from argparse import RawTextHelpFormatter

from flight_profiler.help_descriptions import HISTORY_COMMAND_DESCRIPTION
from flight_profiler.utils.args_util import rewrite_args


class HistoryParams:

    def __init__(self, clear: False, limits: int):
        self.clear = clear
        self.limits = limits


def check_limits(value):
    try:
        i_value = int(value)
        if i_value <= 0:
            raise argparse.ArgumentTypeError(f"{value} should be positive integer.")
        # profile property contains two levels
        return i_value
    except:
        raise argparse.ArgumentTypeError(f"{value} is not a integer between 1 and 6.")


class HistoryParser(argparse.ArgumentParser):

    def __init__(self):
        super(HistoryParser, self).__init__(
            description=HISTORY_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument(
            "-c",
            "--clear",
            required=False,
            action="store_true",
            default=False,
            help="clear all history commands.",
        )
        self.add_argument(
            "-n",
            "--limits",
            type=check_limits,
            required=False,
            help="limits the number of history commands.",
            default=20,
        )

    def error(self, message):
        raise Exception(message)

    def parse_history_params(self, arg_string: str) -> HistoryParams:
        new_args = rewrite_args(arg_string, unspec_names=[], omit_column=None)
        args = self.parse_args(args=new_args)
        return HistoryParams(
            clear=getattr(args, "clear"), limits=getattr(args, "limits")
        )
