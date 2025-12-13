import unittest
from copy import deepcopy

from flight_profiler.utils.args_util import rewrite_args


class ShellTest(unittest.TestCase):

    def test_split_space_bracket(self):

        target_arg_token = [
            "--pkg",
            "__main__",
            "--cls",
            "Cls",
            "--func",
            "test_func",
            "--expr",
            "{return_obj,args}",
        ]

        self.assertEqual(
            rewrite_args(
                "--pkg __main__ --cls Cls --func test_func --expr {return_obj,args}",
                ["pkg", "cls", "func", "expr"],
                omit_column="cls",
            ),
            target_arg_token,
        )
        self.assertEqual(
            rewrite_args(
                "__main__ --cls Cls --func test_func --expr {return_obj,args}",
                ["pkg", "cls", "func", "expr"],
                omit_column="cls",
            ),
            target_arg_token,
        )
        self.assertEqual(
            rewrite_args(
                "__main__ Cls --func test_func --expr {return_obj,args}",
                ["pkg", "cls", "func", "expr"],
                omit_column="cls",
            ),
            target_arg_token,
        )
        self.assertEqual(
            rewrite_args(
                "__main__ Cls test_func {return_obj,args}",
                ["pkg", "cls", "func", "expr"],
                omit_column="cls",
            ),
            target_arg_token,
        )

        no_cls_tokens = deepcopy(target_arg_token)
        no_cls_tokens.pop(2)
        no_cls_tokens.pop(2)
        self.assertEqual(
            rewrite_args(
                "__main__ test_func {return_obj,args}",
                ["pkg", "cls", "func", "expr"],
                omit_column="cls",
            ),
            no_cls_tokens,
        )
