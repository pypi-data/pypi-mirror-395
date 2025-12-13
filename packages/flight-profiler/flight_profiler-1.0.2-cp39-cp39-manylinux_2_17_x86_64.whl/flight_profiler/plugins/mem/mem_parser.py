import argparse
from argparse import RawTextHelpFormatter

from flight_profiler.help_descriptions import MEM_COMMAND_DESCRIPTION

mem_summary_help_message = """
        mem summary usage:\n
        mem summary: will print 10 top size object type \n
        mem summary --limit 100: will print 100 top size object type \n
        mem summary --limit 10 --order descending: will print 10 top size object type\n
        mem summary --limit 10 --order ascending: will print 10 bottom size object type\n
        """

mem_diff_help_message = """
        mem diff usage:\n
        mem diff: will diff memory after 15 second \n
        mem diff --interval 10 --limit 100: will print 100 top size object type \n
        mem diff --interval 10 --limit 10 --order descending: will print 10 top size object type\n
        mem diff --interval 10 --limit 10 --order ascending: will print 10 bottom size object type\n
        """


class MemSummaryArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(MemSummaryArgumentParser, self).__init__(
            description=mem_summary_help_message,
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument(
            "--limit", required=False, type=int, default=10, help="limit type count"
        )
        self.add_argument(
            "--order",
            required=False,
            type=str,
            default="descending",
            help="descending or ascending",
        )


class MemDiffArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(MemDiffArgumentParser, self).__init__(
            description=mem_diff_help_message,
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument(
            "--limit", required=False, type=int, default=10, help="limit type count"
        )
        self.add_argument(
            "--order",
            required=False,
            type=str,
            default="descending",
            help="descending or ascending",
        )
        self.add_argument(
            "--interval", required=False, type=int, default=15, help="diff interval"
        )

    def error(self, message):
        raise Exception(message)


class MemCmd:
    def __init__(self, params):
        self.params = params
        self.is_summary_cmd = False
        self.is_diff_cmd = False
        self.is_valid = True
        self.valid_message = None
        self.valid()

    def valid(self):
        if len(self.params) == 0:
            self.is_valid = False
            self.valid_message = MEM_COMMAND_DESCRIPTION.help_hint()
        elif self.params[0] == "summary":
            self.is_summary_cmd = True
        elif self.params[0] == "diff":
            self.is_diff_cmd = True
        else:
            self.is_valid = False
            self.valid_message = MEM_COMMAND_DESCRIPTION.help_hint()
