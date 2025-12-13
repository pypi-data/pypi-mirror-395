import os
from types import FrameType
from typing import Dict


class FilePathOperator:
    """Operator to shorten file paths for better readability."""

    def __init__(self, sys_path: str = ""):
        """
        Initialize FilePathOperator.

        Args:
            sys_path (str): System path for relative calculations
        """
        self.sys_path = sys_path
        self.file_path_cache: Dict[str, str] = dict()

    def set_sys_path(self, sys_path: str) -> None:
        """
        Set the system path.

        Args:
            sys_path (str): System path for relative calculations
        """
        self.sys_path = sys_path

    def shorten_filepath(self, filepath: str) -> str:
        """
        Shorten a filepath to a more readable form, relative to sys_path.

        Args:
            filepath (str): File path to shorten

        Returns:
            str: Shortened file path
        """
        if filepath in self.file_path_cache:
            return self.file_path_cache[filepath]

        result = filepath
        if len(filepath.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                try:
                    candidate = os.path.relpath(filepath, sys_path_entry)
                except ValueError:
                    continue

                if not result or (
                    len(candidate.split(os.sep)) < len(result.split(os.sep))
                ):
                    result = candidate

        self.file_path_cache[filepath] = result
        return result

    def clear(self) -> None:
        """Clear the file path cache."""
        self.file_path_cache.clear()


global_filepath_operator = FilePathOperator()


def get_class_name(frame: FrameType) -> str:
    """
    Get class name from Frame by self & cls arg.

    Args:
        frame (FrameType): Target frame

    Returns:
        str: Class name or None if not found
    """
    class_name = None
    # instance method
    try:
        self = frame.f_locals.get("self", None)
        if (
            self
            and hasattr(self, "__class__")
            and hasattr(self.__class__, "__qualname__")
        ):
            class_name = self.__class__.__qualname__
        else:
            # class method
            cls = frame.f_locals.get("cls", None)
            if cls and hasattr(cls, "__qualname__"):
                class_name = cls.__qualname__
    except:
        pass

    return class_name
