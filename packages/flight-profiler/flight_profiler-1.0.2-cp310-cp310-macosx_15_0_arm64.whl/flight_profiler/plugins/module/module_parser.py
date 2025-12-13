import argparse
import os.path
from argparse import ArgumentTypeError, RawTextHelpFormatter

from flight_profiler.help_descriptions import MODULE_COMMAND_DESCRIPTION
from flight_profiler.utils.args_util import rewrite_args
from flight_profiler.utils.render_util import COLOR_END, COLOR_ORANGE, COLOR_RED


class ModuleArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(ModuleArgumentParser, self).__init__(
            description=MODULE_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument(
            "--filepath", type=str, required=True, help="target filepath."
        )

    def error(self, message):
        raise Exception(message)

    def parse_full_filepath(self, arg_string: str) -> str:
        new_args = rewrite_args(arg_string, unspec_names=["filepath"], omit_column=None)
        args = self.parse_args(args=new_args)
        filepath = getattr(args, "filepath")
        filepath = os.path.abspath(os.path.expanduser(filepath))
        if not os.path.exists(filepath):
            raise ArgumentTypeError(
                f"filepath {COLOR_ORANGE}{filepath}{COLOR_END}{COLOR_RED} does not exist.{COLOR_END}"
            )
        return filepath
