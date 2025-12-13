from dataclasses import dataclass
from types import CodeType, FunctionType
from typing import Optional, Union


@dataclass
class NestedCodeWrapperResult:
    escaped_func: Optional[FunctionType]
    escaped_func_origin_code: Optional[CodeType]
    outer_func: FunctionType
    outer_func_origin_code: CodeType
    need_wrap_nested_inplace: bool = False
    nested_code_obj: Optional[CodeType] = None


@dataclass
class CodeWrapperResult:
    value: Union[Optional[Union[FunctionType, CodeType]], NestedCodeWrapperResult]
    failed: bool = False
    failed_reason: Optional[str] = None
