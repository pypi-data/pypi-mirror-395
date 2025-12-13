import os
import sys

from flight_profiler.utils.render_util import (
    COLOR_END,
    COLOR_ORANGE,
    COLOR_RED,
    COLOR_WHITE_255,
)


class ModuleAgent:

    @classmethod
    def translate_filepath_to_module(cls, filepath: str):
        find: bool = False
        target_name = None
        # use list to prevent modules change
        for module_name, module in list(sys.modules.items()):
            if hasattr(module, "__file__"):
                if (
                    module.__file__ is not None
                    and os.path.abspath(module.__file__) == filepath
                ):
                    find = True
                    target_name = module.__name__

        if not find:
            return f"{COLOR_RED}filepath: {COLOR_ORANGE}{filepath}{COLOR_END}{COLOR_RED} is not imported in target process.{COLOR_END}"
        else:
            return f"{COLOR_WHITE_255}{target_name}{COLOR_END}"
