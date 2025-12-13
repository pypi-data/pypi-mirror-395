import importlib
import sys
from typing import Optional

from flight_profiler.common import aop_decorator
from flight_profiler.common.system_logger import logger
from flight_profiler.plugins.server_plugin import Message, ServerQueue


class EnterExitCommand:

    def __init__(self, limit: int):
        self.__count = 0
        self.__finished = 0
        self.limit = limit
        self.out_q: Optional[ServerQueue] = None
        self.origin_code = None
        self.module_name = None
        self.method_name = None
        self.class_name = None

    def enter(self) -> bool:
        """
        only execute method only and avoids self inject
        """
        self_injected: bool = False
        try:
            # f_back must be non-null because enter is called by flight-profiler internal method
            f = sys._getframe().f_back.f_back
            if f is None or (
                "flight_profiler" in f.f_code.co_filename
                and "test" not in f.f_code.co_filename
            ):
                self_injected = True
        except:
            self_injected = True
        if self_injected:
            return False

        if self.__count < self.limit:
            self.__count += 1
            return True
        else:
            return False

    def exit(self):
        """
        calls on target method exit
        """
        try:
            self.__finished += 1
            if self.__finished >= self.limit:
                self.recover_origin_code()
                self.child_clear_action()
        except:
            logger.exception("error on exit")

    def recover_origin_code(self):
        if self.origin_code is not None:
            try:
                module = importlib.import_module(self.module_name)
                aop_decorator.clear_func_wrapper(
                    module, self.class_name, self.method_name, self.origin_code
                )
            except:
                logger.exception("clear func wrapper failed.")
            self.origin_code = None

        if self.out_q is not None:
            self.out_q.output_msg_nowait(Message(is_end=True, msg=None))

    def child_clear_action(self):
        pass

    def unique_key(self):
        if hasattr(self, "nested_method"):
            return f"{self.module_name}&{self.class_name}&{self.method_name}&{self.nested_method}"
        else:
            return f"{self.module_name}&{self.class_name}&{self.method_name}"
