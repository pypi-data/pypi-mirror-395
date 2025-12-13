import datetime
import decimal
import enum
import json
from typing import Any, List


def _make_iterencode(obj: Any, max_depth: int, current_indent_level: int, _indent: str = "  ", verbose: bool = False) -> str:
    """
    Generator function to recursively encode Python objects to a string representation with indentation.
    Supports various data types including basic types, collections, custom objects, and special types.

    Args:
        obj: The object to encode
        max_depth: Maximum depth for recursive encoding to prevent infinite recursion
        current_indent_level: Current indentation level for nested objects
        _indent: String used for indentation (default is 2 spaces)
        verbose: Whether to show all elements of collections or limit to first/last 10 with ... in between

    Yields:
        String fragments representing the encoded object
    """

    def iterate_dict(d, depth, _current_indent_level, verbose=False):
        """Helper function to encode dictionary objects with proper indentation."""
        if not d:
            yield '{}'
            return
        if depth <= 0:
            yield repr(d)
            return
        yield '{'
        _current_indent_level += 1
        newline_indent = '\n' + _indent * _current_indent_level + ""
        item_separator = ", " + newline_indent
        yield newline_indent
        first = True
        items = sorted(d.items())

        # If verbose is False and the dictionary is large, show only first 10 and last 10 items
        verbose_thresholds: List[int] = [20, 10]
        for thresh in verbose_thresholds:
            half: int = thresh // 2
            if not verbose and len(items) > thresh:  # If more than 20 items, show first 10 + ... + last 10
                for i, (key, value) in enumerate(items):
                    if i < half:  # First 10 items
                        if first:
                            first = False
                        else:
                            yield item_separator
                        # Handle non-string keys in dictionaries
                        yield f"\"{str(key)}\": "
                        yield from _make_iterencode(value, max_depth=depth - 1,
                                                    current_indent_level=_current_indent_level, verbose=verbose)
                    elif i == half:  # Add ... after the first 10 items
                        yield item_separator
                        yield '...'
                    elif i >= len(items) - half:  # Last 10 items
                        yield item_separator
                        # Handle non-string keys in dictionaries
                        yield f"\"{str(key)}\": "
                        yield from _make_iterencode(value, max_depth=depth - 1,
                                                    current_indent_level=_current_indent_level, verbose=verbose)
                    else:
                        continue  # Skip items in the middle
                break
        else:
            for key, value in items:
                if first:
                    first = False
                else:
                    yield item_separator
                # Handle non-string keys in dictionaries
                yield f"\"{str(key)}\": "
                yield from _make_iterencode(value, max_depth=depth - 1, current_indent_level=_current_indent_level,
                                            verbose=verbose)

        _current_indent_level -= 1
        yield '\n' + _indent * _current_indent_level
        yield '}'

    def _iterencode_listable(lst, depth, _current_indent_level, prefix: str, suffix: str, verbose=False):
        """Helper function to encode list-like objects (list, tuple, set) with proper indentation."""
        if not lst:
            yield f'{prefix}{suffix}'
            return
        if depth <= 0:
            yield repr(lst)
            return
        yield prefix
        _current_indent_level += 1
        newline_indent = '\n' + _indent * _current_indent_level
        _item_separator = "," + newline_indent
        yield newline_indent
        first = True

        # If verbose is False and the list is large, show only first 10 and last 10 items
        verbose_thresholds: List[int] = [20, 10]
        for thresh in verbose_thresholds:
            half: int = thresh // 2
            if not verbose and len(lst) > thresh:  # If more than 20 items, show first 10 + ... + last 10
                for i, value in enumerate(lst):
                    if i < half:  # First 10 items
                        if first:
                            first = False
                        else:
                            yield _item_separator
                        yield from _make_iterencode(value, max_depth=depth - 1, current_indent_level=_current_indent_level, verbose=verbose)
                    elif i == half:  # Add ... after the first 10 items
                        yield _item_separator
                        yield '...'
                    elif i >= len(lst) - half:  # Last 10 items
                        yield _item_separator
                        yield from _make_iterencode(value, max_depth=depth - 1, current_indent_level=_current_indent_level, verbose=verbose)
                    else:
                        continue  # Skip items in the middle
                break
        else:  # If verbose is True or less than 10 items, show all items
            for value in lst:
                if first:
                    first = False
                else:
                    yield _item_separator
                yield from _make_iterencode(value, max_depth=depth - 1, current_indent_level=_current_indent_level, verbose=verbose)

        _current_indent_level -= 1
        yield '\n' + _indent * _current_indent_level
        yield suffix

    # Handle string objects - wrap in single quotes
    if isinstance(obj, str):
        if not verbose and len(obj) > 256:
            yield f'"{obj[:128]}...{obj[-128:]}"'
        else:
            yield f'"{obj}"'
    # Handle dictionary objects
    elif isinstance(obj, dict):
        yield from iterate_dict(obj, depth=max_depth, _current_indent_level=current_indent_level, verbose=verbose)
    # Handle list, tuple, and set objects
    elif isinstance(obj, list):
        yield from _iterencode_listable(list(obj), depth=max_depth, _current_indent_level=current_indent_level, prefix="[", suffix="]", verbose=verbose)
    elif isinstance(obj, tuple):
        yield from _iterencode_listable(list(obj), depth=max_depth, _current_indent_level=current_indent_level, prefix="(", suffix=")", verbose=verbose)
    elif isinstance(obj, set):
        yield from _iterencode_listable(list(obj), depth=max_depth, _current_indent_level=current_indent_level, prefix="set(", suffix=")", verbose=verbose)
    elif obj is True:
        yield 'True'
    elif obj is False:
        yield 'False'
    elif obj is None:
        yield 'None'
    # Handle numeric types (int, float, complex, decimal)
    elif isinstance(obj, (int, float)):
        yield str(obj)
    elif isinstance(obj, complex):
        yield f"{obj}"
    elif isinstance(obj, decimal.Decimal):
        yield f'Decimal("{obj}")'
    # Handle datetime objects
    elif isinstance(obj, datetime.datetime):
        yield f'datetime.datetime.fromisoformat("{obj.isoformat()}")'
    elif isinstance(obj, datetime.date):
        yield f'datetime.date.fromisoformat("{obj.isoformat()}")'
    elif isinstance(obj, datetime.time):
        yield f'datetime.time.fromisoformat("{obj.isoformat()}")'
    # Handle enum objects
    elif isinstance(obj, enum.Enum):
        yield f"{type(obj).__name__}.{obj.name}"
    # Handle custom objects with __dict__ attribute
    elif hasattr(obj, '__dict__'):
        obj_type = type(obj).__name__
        yield f"{obj_type}("
        # Encode the object's attributes as a dictionary
        obj_dict = {k: v for k, v in obj.__dict__.items()}  # Skip private attributes
        yield from iterate_dict(obj_dict, depth=max_depth, _current_indent_level=current_indent_level, verbose=verbose)
        yield ")"
    # Handle bytes objects
    elif isinstance(obj, bytes):
        yield f"b'{obj.decode('utf-8', errors='ignore')}'"
    # Handle callable objects (functions, methods)
    elif callable(obj) and hasattr(obj, '__name__'):
        yield f"<function {obj.__name__}>"
    # Fallback: try json serialization, then repr
    else:
        try:
            yield json.dumps(obj)
        except (TypeError, ValueError):
            yield repr(obj)

def encode_obj_to_transfer(obj: Any, max_depth: int = 3, raw_output: bool = False, indent: str = "  ", verbose: bool = False) -> str:
    """
    Encode Python objects to a string representation suitable for transfer between server and client.
    This function is designed to handle small sets of objects for debugging/inspection purposes.


    Args:
        obj: The Python object to encode
        max_depth: Maximum depth for recursive encoding (default: 3)
        raw_output: Uses repr() to represent obj if True
        indent: String to use for indentation (default: 2 spaces)


    Returns:
        A string representation of the input object with proper indentation
    """
    if not raw_output:
        def _iterencode_with_indent(obj: Any, max_depth: int, current_indent_level: int, verbose: bool) -> str:
            return _make_iterencode(obj, max_depth, current_indent_level, indent, verbose)

        return "".join(_iterencode_with_indent(obj, max_depth, 0, verbose))
    else:
        return repr(obj)
