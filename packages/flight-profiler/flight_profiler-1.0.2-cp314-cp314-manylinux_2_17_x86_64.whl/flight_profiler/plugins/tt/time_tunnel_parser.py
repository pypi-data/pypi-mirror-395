import argparse
from argparse import RawTextHelpFormatter

from flight_profiler.help_descriptions import TIME_TUNNEL_COMMAND_DESCRIPTION
from flight_profiler.plugins.tt.time_tunnel_recorder import TimeTunnelCmd
from flight_profiler.utils.args_util import rewrite_args


def check_expand(value):
    try:
        i_value = int(value)
        if i_value == -1:
            return -1
        if i_value < 1 or i_value > 6:
            raise argparse.ArgumentError(f"{value} should be 1 to 6")
        # profile property contains two levels
        return i_value + 1
    except:
        raise argparse.ArgumentError(f"{value} is not a integer between 1 and 4.")


class TimeTunnelArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(TimeTunnelArgumentParser, self).__init__(
            description=TIME_TUNNEL_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument(
            "-t",
            "--time_tunnel",
            required=False,
            default=None,
            help="record the method invocation within time fragments, imply function location.",
        )

        self.add_argument("-nm", "--nested-method", required=False, help="nested method")
        self.add_argument(
            "-n",
            "--limits",
            required=False,
            default=50,
            type=int,
            help="threshold of execution times, default value 50.",
        )
        self.add_argument(
            "-l",
            "--list",
            required=False,
            default=False,
            action="store_true",
            help="list all the time fragments",
        )
        self.add_argument(
            "-p",
            "--play",
            required=False,
            default=False,
            action="store_true",
            help="replay the time fragment specified by index",
        )
        self.add_argument(
            "-i",
            "--index",
            required=False,
            default=None,
            type=int,
            help="display the detailed information from specified time fragment",
        )
        self.add_argument(
            "-d",
            "--delete",
            required=False,
            default=None,
            type=int,
            help="delete target invocation record from index",
        )
        self.add_argument(
            "-da",
            "--delete_all",
            required=False,
            default=False,
            action="store_true",
            help="delete all invocation records.",
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
            default=2,
            help="Object represent tree expand level(default 1), max_value is 6.",
        )
        self.add_argument(
            "-f",
            "--filter",
            required=False,
            default=None,
            help="params filter expression",
        )
        self.add_argument(
            "-m",
            "--method",
            required=False,
            default=None,
            help="method filter expression",
        )

    def error(self, message):
        raise Exception(message)

    def parse_time_tunnel_cmd(self, arg_string: str) -> TimeTunnelCmd:
        new_args = rewrite_args(
            arg_string,
            unspec_names=[],
            omit_column=None,
            dash_combine_identifier_group={"t": True, "time_tunnel": True},
        )
        args = self.parse_args(args=new_args)

        cmd: TimeTunnelCmd = TimeTunnelCmd(
            time_tunnel=getattr(args, "time_tunnel"),
            limits=getattr(args, "limits"),
            show_list=getattr(args, "list"),
            index=getattr(args, "index"),
            expand_level=getattr(args, "expand"),
            play=getattr(args, "play"),
            delete=getattr(args, "delete"),
            raw_output=getattr(args, "raw"),
            verbose=getattr(args, "verbose"),
            delete_all=getattr(args, "delete_all"),
            filter_expr=getattr(args, "filter"),
            method_filter=getattr(args, "method"),
            nested_method=getattr(args, "nested_method"),
        )
        return cmd
