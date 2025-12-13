import asyncio
import functools
import importlib
import inspect
import pickle
import traceback
import types
from typing import Any, Callable, List, Optional, Union

from flight_profiler.common import aop_decorator
from flight_profiler.common.code_wrapper_entity import CodeWrapperResult
from flight_profiler.plugins.server_plugin import Message
from flight_profiler.plugins.torch.torch_parser import (
    TORCH_ACTIONS,
    BaseTorchCommand,
    TorchMemoryCommand,
    TorchProfileCommand,
)
from flight_profiler.utils.render_util import (
    COLOR_END,
    COLOR_ORANGE,
    COLOR_RED,
    COLOR_WHITE_255,
    build_long_spy_command_hint,
)

TORCH_PROFILE_ENABLE = False
try:
    import torch
    from torch.cuda import synchronize
    from torch.profiler import ProfilerActivity, profile
    TORCH_PROFILE_ENABLE = torch.cuda.is_available()
except ImportError:
    pass


def generate_torch_profile_wrapper(torch_cmd: TorchProfileCommand):
    def torch_profile_decorator(func):
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    should_profile: bool = torch_cmd.enter()
                    if should_profile:
                        profile_failed: bool = False
                        profile_error_msg: str = None
                        biz_failed: bool = False
                        biz_error: Exception = None
                        return_obj: Any = None
                        prof = None
                        try:
                            activities = [ProfilerActivity.CPU, ProfilerActivity.CUDA]
                            prof = profile(activities=activities, with_stack=True, record_shapes=True)
                            prof.__enter__()
                            synchronize()
                        except:
                            profile_error_msg = traceback.format_exc()
                            profile_failed = True

                        if torch_cmd.need_wrap_nested_inplace:
                            current_frame = inspect.currentframe().f_back
                            func_name = torch_cmd.nested_method
                            target_func = current_frame.f_locals[func_name]
                            new_func = types.FunctionType(
                                torch_cmd.nested_code_obj, target_func.__globals__, func_name,
                                target_func.__defaults__, target_func.__closure__
                            )
                            target_func = new_func
                        else:
                            target_func = func

                        try:
                            return_obj = await target_func(*args, **kwargs)
                        except Exception as ex:
                            biz_error = ex
                            biz_failed = True

                        try:
                            if not profile_failed:
                                synchronize()
                                prof.__exit__(None, None, None)
                                prof.export_chrome_trace(torch_cmd.filepath)
                        except:
                            profile_error_msg = traceback.format_exc()
                            profile_failed = True

                        try:
                            if profile_failed:
                                torch_cmd.dump_error(profile_error_msg)
                            else:
                                torch_cmd.dump_success()
                        except:
                            pass

                        if not biz_failed:
                            return return_obj
                        else:
                            raise biz_error
                    else:
                        return func(*args, **kwargs)
                finally:
                    # recover
                    torch_cmd.recover_origin_code()

            return async_wrapper
        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    should_profile: bool = torch_cmd.enter()
                    if should_profile:
                        profile_failed: bool = False
                        profile_error_msg: str = None
                        biz_failed: bool = False
                        biz_error: Exception = None
                        return_obj: Any = None
                        prof = None
                        try:
                            activities = [ProfilerActivity.CPU, ProfilerActivity.CUDA]
                            prof = profile(activities=activities, with_stack=True, record_shapes=True)
                            prof.__enter__()
                        except:
                            profile_error_msg = traceback.format_exc()
                            profile_failed = True

                        if torch_cmd.need_wrap_nested_inplace:
                            current_frame = inspect.currentframe().f_back
                            func_name = torch_cmd.nested_method
                            target_func = current_frame.f_locals[func_name]
                            new_func = types.FunctionType(
                                torch_cmd.nested_code_obj, target_func.__globals__, func_name,
                                target_func.__defaults__, target_func.__closure__
                            )
                            target_func = new_func
                        else:
                            target_func = func

                        try:
                            return_obj = target_func(*args, **kwargs)
                        except Exception as ex:
                            biz_error = ex
                            biz_failed = True

                        try:
                            if not profile_failed:
                                prof.__exit__(None, None, None)
                                prof.export_chrome_trace(torch_cmd.filepath)
                        except:
                            profile_error_msg = traceback.format_exc()
                            profile_failed = True

                        try:
                            if profile_failed:
                                torch_cmd.dump_error(profile_error_msg)
                            else:
                                torch_cmd.dump_success()
                        except:
                            pass

                        if not biz_failed:
                            return return_obj
                        else:
                            raise biz_error
                    else:
                        return func(*args, **kwargs)
                finally:
                    # recover
                    torch_cmd.recover_origin_code()

            return wrapper

    return torch_profile_decorator


def generate_torch_memory_wrapper(func_args: List[Any]):
    """
    func_args: [TorchMemoryCommand, new_version_record: bool, record_function, dump_function],
    """

    def torch_memory_decorator(func):
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    cmd: TorchMemoryCommand = func_args[0]
                    new_version_record: bool = func_args[1]
                    record_function: Callable = func_args[2]
                    dump_function: Callable = func_args[3]
                    should_profile: bool = cmd.enter()
                    if should_profile:
                        record_msg: Optional[str] = None
                        dump_err_msg: Optional[str] = None
                        biz_error: Optional[Exception] = None
                        return_obj: Any = None
                        try:
                            if new_version_record:
                                record_function()
                            else:
                                record_function(
                                    enabled=True,
                                    trace_alloc_max_entries=100_000,
                                    trace_alloc_record_context=True,
                                )
                            synchronize()
                        except:
                            record_msg = traceback.format_exc()

                        if cmd.need_wrap_nested_inplace:
                            current_frame = inspect.currentframe().f_back
                            func_name = cmd.nested_method
                            target_func = current_frame.f_locals[func_name]
                            new_func = types.FunctionType(
                                cmd.nested_code_obj, target_func.__globals__, func_name,
                                target_func.__defaults__, target_func.__closure__
                            )
                            target_func = new_func
                        else:
                            target_func = func

                        try:
                            return_obj = await target_func(*args, **kwargs)
                        except Exception as ex:
                            biz_error = ex

                        if record_msg is None:
                            try:
                                synchronize()
                                with open(cmd.filepath, "wb") as f:
                                    pickle.dump(dump_function(), f)
                            except:
                                dump_err_msg = traceback.format_exc()

                        try:
                            if record_msg is not None:
                                cmd.dump_error(record_msg)
                            elif dump_err_msg is not None:
                                cmd.dump_error(dump_err_msg)
                            else:
                                cmd.dump_success("record")
                        except:
                            pass

                        try:
                            if new_version_record:
                                record_function(enabled=None)
                            else:
                                record_function(enabled=False)
                        except:
                            pass

                        if biz_error is None:
                            return return_obj
                        else:
                            raise biz_error
                    else:
                        return func(*args, **kwargs)
                finally:
                    # recover
                    func_args[0].recover_origin_code()

            return async_wrapper
        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    cmd: TorchMemoryCommand = func_args[0]
                    new_version_record: bool = func_args[1]
                    record_function: Callable = func_args[2]
                    dump_function: Callable = func_args[3]
                    should_profile: bool = cmd.enter()
                    if should_profile:
                        record_msg: Optional[str] = None
                        dump_err_msg: Optional[str] = None
                        biz_error: Optional[Exception] = None
                        return_obj: Any = None
                        try:
                            if new_version_record:
                                record_function()
                            else:
                                record_function(
                                    enabled=True,
                                    trace_alloc_max_entries=100_000,
                                    trace_alloc_record_context=True,
                                )
                        except:
                            record_msg = traceback.format_exc()

                        if cmd.need_wrap_nested_inplace:
                            current_frame = inspect.currentframe().f_back
                            func_name = cmd.nested_method
                            target_func = current_frame.f_locals[func_name]
                            new_func = types.FunctionType(
                                cmd.nested_code_obj, target_func.__globals__, func_name,
                                target_func.__defaults__, target_func.__closure__
                            )
                            target_func = new_func
                        else:
                            target_func = func

                        try:
                            return_obj = target_func(*args, **kwargs)
                        except Exception as ex:
                            biz_error = ex

                        if record_msg is None:
                            try:
                                with open(cmd.filepath, "wb") as f:
                                    pickle.dump(dump_function(), f)
                            except:
                                dump_err_msg = traceback.format_exc()

                        try:
                            if record_msg is not None:
                                cmd.dump_error(record_msg)
                            elif dump_err_msg is not None:
                                cmd.dump_error(dump_err_msg)
                            else:
                                cmd.dump_success("record")
                        except:
                            pass

                        try:
                            if new_version_record:
                                record_function(enabled=None)
                            else:
                                record_function(enabled=False)
                        except:
                            pass

                        if biz_error is None:
                            return return_obj
                        else:
                            raise biz_error
                    else:
                        return func(*args, **kwargs)
                finally:
                    # recover
                    func_args[0].recover_origin_code()

            return wrapper

    return torch_memory_decorator


def _post_process_transform(module, cmd: BaseTorchCommand) -> None:
    """
    check module function or module class function can correspond
    """
    if cmd.origin_code is None:
        if cmd.class_name is not None:
            if getattr(module, cmd.class_name, None) is not None:
                err_msg = (
                    f"No method named {COLOR_ORANGE}{cmd.method_name}{COLOR_END}{COLOR_RED}"
                    f" is found in class {cmd.class_name}!"
                )
            else:
                err_msg = (
                    f"No class named {COLOR_ORANGE}{cmd.class_name}{COLOR_END}{COLOR_RED}"
                    f" is found in module {cmd.module_name}!"
                )
        else:
            err_msg = (
                f"No method named {COLOR_ORANGE}{cmd.method_name}{COLOR_END}{COLOR_RED}"
                f" is found in module {cmd.module_name}!"
            )
        cmd.out_q.output_msg_nowait(
            Message(True, msg=f"{COLOR_RED}{err_msg}{COLOR_END}")
        )
        return


class TorchProfileAgent:

    def __init__(self):
        self.cmd: Optional[Union[TorchProfileCommand, TorchMemoryCommand]] = None

    def on_action(
        self, cmd: Union[BaseTorchCommand, TorchProfileCommand, TorchMemoryCommand]
    ) -> None:
        """
        support profile command
        """
        if cmd.is_profile():
            if not TORCH_PROFILE_ENABLE:
                cmd.out_q.output_msg_nowait(
                    Message(
                        is_end=True,
                        msg=f"{COLOR_RED}torch profile is not enabled, you can examine by "
                        f"  {COLOR_ORANGE}from torch.profiler import profile, ProfilerActivity && torch.cuda.is_available(){COLOR_RED}{COLOR_RED}. {COLOR_END}",
                    )
                )
                return

            try:
                module = importlib.import_module(cmd.module_name)
            except Exception as e:
                cmd.out_q.output_msg_nowait(
                    Message(
                        True,
                        pickle.dumps(
                            f"{COLOR_RED}Error in locating module named "
                            f"{COLOR_ORANGE}{cmd.module_name}{COLOR_END}{COLOR_RED}. Type: {type(e)}, details: {str(e)}!{COLOR_END}"
                        ),
                    )
                )
                return

            wrapper_result: CodeWrapperResult = aop_decorator.add_func_wrapper(
                module,
                cmd.class_name,
                cmd.method_name,
                generate_torch_profile_wrapper,
                cmd,
                ["importlib", "traceback"],
                {
                    "torch.profiler": ["profile", "ProfilerActivity"],
                    "torch.cuda": ["synchronize"],
                },
                module_name=cmd.module_name,
                nested_method=cmd.nested_method
            )
            if wrapper_result.failed:
                cmd.out_q.output_msg_nowait(
                    Message(True, msg=f"{COLOR_RED}{wrapper_result.failed_reason}{COLOR_END}")
                )
            else:
                if cmd.nested_method is not None and wrapper_result.value.need_wrap_nested_inplace:
                    # used to construct new code at runtime
                    cmd.need_wrap_nested_inplace = True
                    cmd.nested_code_obj = wrapper_result.value.nested_code_obj
                cmd.origin_code = wrapper_result.value
                cmd.out_q.output_msg_nowait(
                    Message(
                    False,
                        build_long_spy_command_hint(
                            cmd.module_name,
                            cmd.class_name,
                            cmd.method_name,
                            cmd.nested_method
                        )
                    )
                )
                self.cmd = cmd
        elif cmd.is_memory():
            memory_cmd: TorchMemoryCommand = cmd
            if memory_cmd.snapshot:
                try:
                    from torch.cuda.memory import _snapshot as mm_snapshot
                except:
                    try:
                        from torch.cuda.memory import memory_snapshot as mm_snapshot
                    except:
                        memory_cmd.out_q.output_msg_nowait(
                            Message(
                                is_end=True,
                                msg=f"{COLOR_RED}torch memory snapshot is not enabled, you can examine by "
                                f"  {COLOR_ORANGE}from torch.cuda.memory import memory_snapshot{COLOR_RED}{COLOR_RED}. {COLOR_END}",
                            )
                        )
                        return
                try:
                    with open(memory_cmd.filepath, "wb") as f:
                        pickle.dump(mm_snapshot(), f)
                except:
                    memory_cmd.dump_error(traceback.format_exc())
                    return
                memory_cmd.dump_success("snapshot")
            else:
                # record situation
                try:
                    from torch.cuda.memory import (
                        _record_memory_history as record_memory_history,
                    )
                    from torch.cuda.memory import _snapshot as dump_snapshot
                except:
                    memory_cmd.out_q.output_msg_nowait(
                        Message(
                            is_end=True,
                            msg=f"{COLOR_RED}torch memory record is not enabled, you can examine by "
                            f"  {COLOR_ORANGE}from torch.cuda.memory import _record_memory_history, _snapshot{COLOR_RED}{COLOR_RED}. {COLOR_END}",
                        )
                    )
                    return

                # torch version >= 2.1.0
                # old version torch uses enabled as bool, raise Exception when input str
                # new version torch uses enabled as str
                new_version_record: bool = True
                try:
                    record_memory_history(enabled="all")
                    record_memory_history(enabled=None)
                except:
                    new_version_record = False

                try:
                    module = importlib.import_module(cmd.module_name)
                except Exception as e:
                    cmd.out_q.output_msg_nowait(
                        Message(
                            True,
                            pickle.dumps(
                                f"{COLOR_RED}Error in locating module named "
                                f"{COLOR_ORANGE}{cmd.module_name}{COLOR_END}{COLOR_RED}. Type: {type(e)}, details: {str(e)}!{COLOR_END}"
                            ),
                        )
                    )
                    return

                wrapper_result: CodeWrapperResult = aop_decorator.add_func_wrapper(
                    module,
                    cmd.class_name,
                    cmd.method_name,
                    generate_torch_memory_wrapper,
                    [cmd, new_version_record, record_memory_history, dump_snapshot],
                    ["importlib", "traceback", "pickle", "inspect", "types"],
                    {
                        "torch.cuda.memory": ["_record_memory_history", "_snapshot"],
                        "torch.cuda": ["synchronize"],
                    },
                    module_name=cmd.module_name,
                    nested_method=cmd.nested_method
                )
                if wrapper_result.failed:
                    cmd.out_q.output_msg_nowait(
                        Message(True, msg=f"{COLOR_RED}{wrapper_result.failed_reason}{COLOR_END}")
                    )
                else:
                    if cmd.nested_method is not None and wrapper_result.value.need_wrap_nested_inplace:
                        # used to construct new code at runtime
                        cmd.need_wrap_nested_inplace = True
                        cmd.nested_code_obj = wrapper_result.value.nested_code_obj
                    cmd.origin_code = wrapper_result.value
                    cmd.out_q.output_msg_nowait(
                        Message(
                    False,
                            build_long_spy_command_hint(
                                cmd.module_name,
                                cmd.class_name,
                                cmd.method_name,
                                cmd.nested_method
                            )
                        )
                    )
                    self.cmd = cmd
        else:
            cmd.out_q.output_msg_nowait(
                Message(
                    is_end=True,
                    msg=f"{COLOR_RED} Unsupported torch command action type {cmd.action}, allowed values are "
                    f"{COLOR_ORANGE}{'|'.join(TORCH_ACTIONS.keys())}{COLOR_END}{COLOR_RED}.{COLOR_END}",
                )
            )

    def clear_spy(self, cmd: Union[TorchProfileCommand, TorchMemoryCommand]):
        """
        called in case spied method is always not called
        """
        if self.cmd is not None:
            self.cmd.recover_origin_code()
            if self.cmd.out_q is not None:
                self.cmd.out_q.output_msg_nowait(
                    Message(
                        is_end=True,
                        msg=f"{COLOR_WHITE_255}Canceled by user interrupt, target method is not called during spy.{COLOR_END}",
                    )
                )


global_torch_agent = TorchProfileAgent()
