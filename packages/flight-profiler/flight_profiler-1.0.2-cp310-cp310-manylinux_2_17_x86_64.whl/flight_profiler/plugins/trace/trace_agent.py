import asyncio
import functools
import importlib
import inspect
import pickle
import sys
import traceback
import types
from types import CodeType
from typing import Any, Callable, Dict, List, Optional, Union

from flight_profiler.common import aop_decorator
from flight_profiler.common.code_wrapper_entity import CodeWrapperResult
from flight_profiler.common.enter_exit_command import EnterExitCommand
from flight_profiler.common.expression_resolver import FilterExprResolver
from flight_profiler.common.system_logger import logger
from flight_profiler.ext.trace_profile_C import remove_trace_profile, set_trace_profile
from flight_profiler.plugins.server_plugin import Message, ServerQueue
from flight_profiler.plugins.trace.trace_frame import WrapTraceFrame
from flight_profiler.utils.render_util import (
    COLOR_END,
    COLOR_ORANGE,
    COLOR_RED,
    build_long_spy_command_hint,
)

# from flight_profiler.plugins.trace.trace_profiler import (
#     remove_trace_profile,
#     set_trace_profile,
# )


class TracePoint(EnterExitCommand):

    def __init__(
        self,
        module_name: str,
        class_name: Optional[str],
        method_name: str,
        interval: float,
        entrance_time: int,
        limits: int,
        depth: int,
        filter_expr: Optional[str] = None,
        out_q: ServerQueue = None,
        nested_method: str = None,
        need_wrap_nested_inplace: bool = False,
        nested_code_obj: CodeType = None
    ):
        super().__init__(limit=limits)
        self.module_name = module_name
        self.class_name = class_name
        self.method_name = method_name
        self.origin_code: Optional[CodeType] = None
        self.filter_expr = filter_expr
        self.filter = FilterExprResolver(expr=self.filter_expr)
        self.interval = interval
        self.entrance_time = entrance_time
        self.limits = limits
        self.depth = depth
        self.out_q = out_q
        self.nested_method = nested_method
        self.need_wrap_nested_inplace = need_wrap_nested_inplace
        self.nested_code_obj = nested_code_obj


    def child_clear_action(self):
        global_trace_agent.clear_auto_close(self.unique_key())


def c_bind_output_trace_frames(out_q: ServerQueue, sending_frames: List[str]) -> None:
    """
    response trace frames to client side
    """
    out_q.output_msg_nowait(
        Message(
            False, msg=pickle.dumps(WrapTraceFrame(sending_frames))
        )
    )


def generate_trace_wrapper(func_args: List[Union[Callable, Any]]) -> Callable:
    """
    func_args: [set_trace_profile, output_frames_function, trace_point,
                interval_ns, watch_filter, is_class_method, remove_trace_function]
    """

    def trace_decorator(func):
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                trace_point: TracePoint = func_args[2]
                if trace_point.enter():
                    trace_profiler = None
                    try:
                        is_class_method: bool = func_args[5]
                        out_q: ServerQueue = trace_point.out_q
                        target = None if not is_class_method or trace_point.nested_method is not None else args[0]
                        filter: FilterExprResolver = func_args[4]
                        can_pass: bool = False
                        try:
                            can_pass = filter.eval_filter(
                                target, None, 0, *args, **kwargs
                            )
                        except:
                            msg = traceback.format_exc()
                            out_q.output_msg_nowait(
                                Message(False, msg=msg + "\n")
                            )

                        if trace_point.need_wrap_nested_inplace:
                            current_frame = inspect.currentframe().f_back
                            func_name = trace_point.nested_method
                            target_func = current_frame.f_locals[func_name]
                            new_func = types.FunctionType(
                                trace_point.nested_code_obj, target_func.__globals__, func_name,
                                target_func.__defaults__, target_func.__closure__
                            )
                            target_func = new_func
                        else:
                            target_func = func
                        if can_pass:
                            trace_profiler = func_args[0](
                                func_args[1], out_q, func_args[3], True, trace_point.depth
                            )
                        return await target_func(*args, **kwargs)
                    except:
                        raise
                    finally:
                        func_args[6](trace_profiler)
                        trace_point.exit()
                else:
                    return await func(*args, **kwargs)

            return async_wrapper
        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                trace_point: TracePoint = func_args[2]
                if trace_point.enter():
                    trace_profiler = None
                    try:
                        is_class_method: bool = func_args[5]
                        out_q: ServerQueue = trace_point.out_q
                        target = None if not is_class_method or trace_point.nested_method is not None else args[0]
                        filter: FilterExprResolver = func_args[4]
                        can_pass: bool = False
                        try:
                            can_pass = filter.eval_filter(
                                target, None, 0, *args, **kwargs
                            )
                        except:
                            msg = traceback.format_exc()
                            out_q.output_msg_nowait(
                                Message(False, msg=msg + "\n")
                            )
                        if trace_point.need_wrap_nested_inplace:
                            current_frame = inspect.currentframe().f_back
                            func_name = trace_point.nested_method
                            target_func = current_frame.f_locals[func_name]
                            new_func = types.FunctionType(
                                trace_point.nested_code_obj, target_func.__globals__, func_name,
                                target_func.__defaults__, target_func.__closure__
                            )
                            target_func = new_func
                        else:
                            target_func = func
                        if can_pass:
                            trace_profiler = func_args[0](
                                func_args[1], out_q, func_args[3], False, trace_point.depth
                            )
                        return target_func(*args, **kwargs)
                    except:
                        raise
                    finally:
                        func_args[6](trace_profiler)
                        trace_point.exit()
                else:
                    return func(*args, **kwargs)

            return wrapper

    return trace_decorator


class TraceAgent:

    def __init__(self):
        self.aop_points: Dict[str, TracePoint] = dict()

    def set_point(self, point: TracePoint) -> None:
        """
        wrap target trace function
        """
        key: str = point.unique_key()
        old_point = self.aop_points.get(key, None)
        if old_point is not None:
            self.clear_point(old_point)

        point.out_q.output_msg_nowait(
            Message(is_end=False, msg=pickle.dumps(sys.path))
        )

        try:
            module = importlib.import_module(point.module_name)
        except Exception as e:
            point.out_q.output_msg_nowait(
                Message(
                    True,
                    pickle.dumps(
                        f"{COLOR_RED}Error in locating module named "
                        f"{COLOR_ORANGE}{point.module_name}{COLOR_END}{COLOR_RED}. Type: {type(e)}, details: {str(e)}!{COLOR_END}"
                    ),
                )
            )
            return

        wrapper_result: CodeWrapperResult = aop_decorator.add_func_wrapper(
            module,
            point.class_name,
            point.method_name,
            generate_trace_wrapper,
            [
                set_trace_profile,
                c_bind_output_trace_frames,
                point,
                int(point.interval * 1000000),
                point.filter,
                point.class_name is not None,
                remove_trace_profile,
            ],
            ["sys", "traceback", "inspect", "types"],
            nested_method=point.nested_method,
            module_name=point.module_name
        )
        if wrapper_result.failed:
            point.out_q.output_msg_nowait(
                Message(
                    True,
                    pickle.dumps(f"{COLOR_RED}{wrapper_result.failed_reason}{COLOR_END}"),
                )
            )
        else:
            if point.nested_method is not None and wrapper_result.value.need_wrap_nested_inplace:
                # used to construct new code at runtime
                point.need_wrap_nested_inplace = True
                point.nested_code_obj = wrapper_result.value.nested_code_obj
            point.origin_code = wrapper_result.value
            point.out_q.output_msg_nowait(
                Message(
                    False,
                    pickle.dumps(
                        build_long_spy_command_hint(
                            point.module_name, point.class_name, point.method_name,
                            point.nested_method
                        )
                    ),
                )
            )
            self.aop_points[key] = point

    def clear_point(self, point: TracePoint) -> None:
        """
        clear point replace
        """
        old_point: TracePoint = self.aop_points.get(point.unique_key(), None)
        if old_point is None:
            logger.warning(
                f"class function {point.unique_key()} "
                f"not watched, will skip clear"
            )
            return None
        self.aop_points.pop(point.unique_key())

        if old_point.origin_code is not None:
            module = importlib.import_module(old_point.module_name)
            aop_decorator.clear_func_wrapper(
                module,
                old_point.class_name,
                old_point.method_name,
                old_point.origin_code,
            )
            old_point.origin_code = None
            old_point.out_q.output_msg_nowait(Message(is_end=True, msg=""))

    def clear_auto_close(self, unique_key: str):
        self.aop_points.pop(unique_key, None)

global_trace_agent: TraceAgent = TraceAgent()
