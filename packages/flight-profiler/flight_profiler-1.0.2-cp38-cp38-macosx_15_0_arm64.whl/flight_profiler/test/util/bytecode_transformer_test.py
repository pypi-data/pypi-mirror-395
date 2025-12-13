import unittest
from types import CodeType, FunctionType

import opcode

from flight_profiler.common.bytecode_transformer import (
    transform_normal_method_by_aop_wrapper,
)


class BytecodeTransformerTest(unittest.TestCase):

    def test_transform_watch_func(self):
        def test_func(x):
            return x

        def watch_wrap(watch_settings) -> FunctionType:
            def wrapper(func: FunctionType):
                def wrap_func(*args, **kwargs):
                    print(watch_settings)
                    return func(*args, **kwargs)

                return wrap_func

            return wrapper

        watch_func = watch_wrap(None)(test_func)
        origin_code = watch_func.__code__
        deref_opcode = bytes([opcode.opmap["LOAD_DEREF"]])

        self.assertTrue(deref_opcode in origin_code.co_code)

        transform_normal_method_by_aop_wrapper(
            test_func, watch_wrap, "watch_setting", ["time"]
        )
        transformed_code: CodeType = test_func.__code__
        self.assertTrue(deref_opcode not in transformed_code.co_code)
        self.assertEqual(
            "watch_setting",
            transformed_code.co_consts[len(transformed_code.co_consts) - 2],
        )


if __name__ == "__main__":
    unittest.main()
