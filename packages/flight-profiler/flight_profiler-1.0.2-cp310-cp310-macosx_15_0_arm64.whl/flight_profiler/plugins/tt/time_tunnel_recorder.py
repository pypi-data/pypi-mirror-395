import asyncio
import importlib
import pickle
import time
import traceback
from argparse import ArgumentTypeError
from concurrent.futures import ThreadPoolExecutor
from types import CodeType
from typing import Any, Dict, List, Optional, Union

from flight_profiler.common.aop_decorator import (
    find_class_function,
    find_module_function,
)
from flight_profiler.common.dumps import encode_obj_to_transfer
from flight_profiler.common.enter_exit_command import EnterExitCommand
from flight_profiler.common.expression_resolver import FilterExprResolver
from flight_profiler.plugins.server_plugin import Message, ServerQueue
from flight_profiler.utils.args_util import split_regex


class TimeTunnelCmd(EnterExitCommand):

    def __init__(
        self,
        time_tunnel: Optional[str],
        limits: int,
        show_list: bool,
        index: Optional[int],
        expand_level: Optional[int],
        play: bool,
        delete: Optional[int],
        delete_all: bool,
        filter_expr: Optional[str],
        method_filter: Optional[str],
        out_q: Optional[ServerQueue] = None,
        raw_output: bool = False,
        verbose: bool = False,
        nested_method: str = None,
        need_wrap_nested_inplace: bool = False,
        nested_code_obj: CodeType = None
    ):
        super().__init__(limit=limits)
        self.time_tunnel = time_tunnel
        self.limits = limits
        self.show_list = show_list
        self.index = index
        self.expand_level = expand_level
        if self.expand_level == -1:
            self.expand_level = None
        self.raw_output = raw_output
        self.out_q = out_q
        self.origin_code: Optional[CodeType] = None
        self.delete_id = delete
        self.delete_all = delete_all
        self.filter_expr = filter_expr
        self.method_filter = method_filter
        self.verbose = verbose
        self.tt_filter: FilterExprResolver = FilterExprResolver(expr=filter_expr)
        self.global_instance = None
        self.play = play
        self.nested_method = nested_method
        self.need_wrap_nested_inplace = need_wrap_nested_inplace
        self.nested_code_obj = nested_code_obj

        if self.time_tunnel is not None:
            func_location = split_regex(self.time_tunnel)
            self.module_name = func_location[0]
            if len(func_location) == 2:
                self.class_name = None
                self.method_name = func_location[1]
            elif len(func_location) == 3:
                self.class_name = func_location[1]
                self.method_name = func_location[2]
            else:
                raise ArgumentTypeError(
                    f"invalid time tunnel format: {self.time_tunnel}"
                )

    def valid(self):
        violation = 1 if self.time_tunnel is not None else 0
        violation += 1 if self.show_list else 0
        violation += 1 if self.index is not None else 0
        violation += 1 if self.delete_id is not None else 0
        violation += 1 if self.delete_all else 0

        if violation != 1:
            raise ArgumentTypeError(
                "Invalid tt command format, you can only specify -t/-l/-i/-d/-da option!"
            )

    def dump_invocation(
        self,
        start_timestamp: int,
        cost_ms: float,
        return_obj: Any,
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> None:
        target_obj = None
        if self.class_name is not None and self.nested_method is None:
            filter_args = args[1:]
            target_obj = args[0]
        else:
            filter_args = args
        if self.tt_filter.eval_filter(
            target_obj, return_obj, cost_ms, *filter_args, **kwargs
        ):
            index = global_tt_indexer.get_index()
            record: FullInvocationRecord = global_time_tunnel_recorder.records(
                index,
                start_timestamp,
                cost_ms,
                True,
                False,
                self.module_name,
                self.class_name,
                self.method_name,
                args,
                kwargs,
                return_obj,
                None,
            )
            if self.out_q is not None:
                self.out_q.output_msg_nowait(
                    Message(
                        False, msg=pickle.dumps(record.base_record)
                    )
                )

    def dump_error(
        self,
        start_timestamp: int,
        cost_ms: float,
        exp_obj: Any,
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> None:
        target_obj = None
        if self.class_name is not None and self.nested_method is None:
            filter_args = args[1:]
            target_obj = args[0]
        else:
            filter_args = args
        if self.tt_filter.eval_filter(
            target_obj, None, cost_ms, *filter_args, **kwargs
        ):
            index = global_tt_indexer.get_index()
            record: FullInvocationRecord = global_time_tunnel_recorder.records(
                index,
                start_timestamp,
                cost_ms,
                False,
                True,
                self.module_name,
                self.class_name,
                self.method_name,
                args,
                kwargs,
                None,
                exp_obj,
            )
            if self.out_q is not None:
                self.out_q.output_msg_nowait(
                    Message(
                        False, msg=pickle.dumps(record.base_record)
                    )
                )

    def child_clear_action(self):
        if self.global_instance is not None:
            self.global_instance.clear_auto_close(self.unique_key())
            self.global_instance = None


class BaseInvocationRecord:

    def __init__(
        self,
        index: int,
        timestamp: int,
        cost_ms: float,
        is_ret: bool,
        is_exp: bool,
        module_name: str,
        class_name: str,
        method_name: str,
    ):
        self.index = index
        self.timestamp = timestamp
        self.cost_ms = cost_ms
        self.is_ret = is_ret
        self.is_exp = is_exp
        self.module_name = module_name
        self.class_name = class_name
        self.method_name = method_name


class FullInvocationRecord:

    def __init__(
        self,
        base_record: BaseInvocationRecord,
        args: Union[List[Any], str],
        kwargs: Union[Dict[str, Any], str],
        return_obj: Union[Any, str],
        exp_obj: Union[Any, str],
    ):
        self.base_record = base_record
        self.args = args
        self.kwargs = kwargs
        self.return_obj = return_obj
        self.exp_obj = exp_obj


class TimeTunnelIndexer:

    def __init__(self):
        self.index = 999

    def get_index(self) -> int:
        """
        increments index, and returns
        """
        self.index += 1
        return self.index

    def refresh(self):
        self.index = 999


global_tt_indexer = TimeTunnelIndexer()


class TimeTuneReplayExecutor:

    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=1)

    def execute_in_new_thread(self, method, *args, **kwargs):
        future = self.thread_pool.submit(self.__inner_execute, method, *args, **kwargs)
        return future.result()

    def __inner_execute(self, method, *args, **kwargs):
        asyncio.set_event_loop(asyncio.new_event_loop())
        s = time.time()
        try:
            if asyncio.iscoroutinefunction(method):
                return_obj = asyncio.run(method(*args, **kwargs))
            else:
                return_obj = method(*args, **kwargs)
            e = time.time()
            return False, int(s * 1000), (e - s) * 1000, return_obj
        except Exception as ex:
            e = time.time()
            msg = traceback.format_exc()
            return True, int(s * 1000), (e - s) * 1000, msg


global_replay_executor = TimeTuneReplayExecutor()


class TimeTunnelRecorder:

    def __init__(self):
        self.invocation_records: Dict[int, FullInvocationRecord] = {}

    def records(
        self,
        index: int,
        start_time: int,
        cost_ms: float,
        is_ret: bool,
        is_exp: bool,
        module_name: str,
        class_name: str,
        method_name: str,
        args: List[Any],
        kwargs: Dict[str, Any],
        return_obj: Any,
        exp_obj: Any,
    ) -> FullInvocationRecord:
        full_record: FullInvocationRecord = FullInvocationRecord(
            BaseInvocationRecord(
                index,
                start_time,
                cost_ms,
                is_ret,
                is_exp,
                module_name,
                class_name,
                method_name,
            ),
            args,
            kwargs,
            return_obj,
            exp_obj,
        )
        self.invocation_records[index] = full_record
        return full_record

    def show_list_records(self, cmd: TimeTunnelCmd) -> None:
        base_records = []
        for r in self.invocation_records.values():
            filter_args = r.args
            method_names = f"{r.base_record.module_name}.{r.base_record.class_name}.{r.base_record.method_name}"
            if cmd.method_filter is not None and cmd.method_filter != method_names:
                continue

            target_obj = None
            if r.base_record.class_name is not None:
                filter_args = r.args[1:]
                target_obj = r.args[0]

            if cmd.tt_filter.eval_filter(
                target_obj,
                r.return_obj,
                r.base_record.cost_ms,
                *filter_args,
                **r.kwargs,
            ):
                base_records.append(r.base_record)
        cmd.out_q.output_msg_nowait(
            Message(True, msg=pickle.dumps(base_records))
        )

    def show_indexed_record(self, cmd: TimeTunnelCmd) -> None:
        if cmd.index not in self.invocation_records:
            cmd.out_q.output_msg_nowait(
                Message(
                    True,
                    pickle.dumps(f"Couldn't find index for {cmd.index}!"),
                )
            )
            return
        full_record: FullInvocationRecord = self.invocation_records[cmd.index]
        self.__send_full_record_directly(full_record, cmd.out_q, cmd.expand_level,
                                         raw_output=cmd.raw_output, verbose=cmd.verbose)

    def __send_full_record_directly(
        self, full_record: FullInvocationRecord, out_q: ServerQueue, expand_level: int,
        raw_output: bool, verbose: bool
    ) -> None:
        cls_name = full_record.base_record.class_name
        origin_args = []
        if cls_name is not None:
            origin_args = full_record.args
            full_record.args = full_record.args[1:]
        out_q.output_msg_nowait(
            Message(
                True,
                msg=pickle.dumps(
                    FullInvocationRecord(
                        base_record=full_record.base_record,
                        args=encode_obj_to_transfer(full_record.args, max_depth=expand_level,
                                                    raw_output=raw_output, verbose=verbose),
                        kwargs=encode_obj_to_transfer(full_record.kwargs, max_depth=expand_level,
                                                      raw_output=raw_output, verbose=verbose),
                        return_obj=encode_obj_to_transfer(full_record.return_obj, max_depth=expand_level,
                                                          raw_output=raw_output, verbose=verbose),
                        exp_obj=encode_obj_to_transfer(full_record.exp_obj, max_depth=expand_level,
                                                       raw_output=raw_output, verbose=verbose),
                    )
                ),
            )
        )
        if cls_name is not None:
            full_record.args = origin_args

    def replay_time_fragment(self, cmd: TimeTunnelCmd) -> None:
        if cmd.index not in self.invocation_records:
            cmd.out_q.output_msg_nowait(
                Message(
                    True,
                    pickle.dumps(f"Couldn't find index for {cmd.index}!"),
                )
            )
            return

        record: FullInvocationRecord = self.invocation_records[cmd.index]
        cls_name: str = record.base_record.class_name
        module_name = record.base_record.module_name
        method_name = record.base_record.method_name
        module = importlib.import_module(module_name)
        method = None
        if cls_name is not None:
            cls = getattr(module, cls_name)
            if cls is not None:
                name, target_method, is_class_method = find_class_function(cls, method_name)
                method = target_method
        else:
            target_method, is_builtin = find_module_function(module, method_name)
            method = target_method
        if method is None:
            cmd.out_q.output_msg_nowait(
                Message(
                    True,
                    pickle.dumps(
                        f"Couldn't find target method for"
                        f"module: {module_name}, class: {cls_name}, "
                        f"function: {method_name}!"
                    )
                )
            )
            return
        # current in coroutine, if execute in here, may not satisfy async constrains
        is_exp, start_ms, cost_ms, ret_obj = (
            global_replay_executor.execute_in_new_thread(
                method, *record.args, **record.kwargs
            )
        )
        if not is_exp:
            index = global_tt_indexer.get_index()
            new_record: FullInvocationRecord = self.records(
                index,
                start_ms,
                cost_ms,
                True,
                False,
                module_name,
                cls_name,
                method_name,
                record.args,
                record.kwargs,
                ret_obj,
                None,
            )
            self.__send_full_record_directly(new_record, cmd.out_q, cmd.expand_level, cmd.raw_output, cmd.verbose)
        else:
            index = global_tt_indexer.get_index()
            new_record: FullInvocationRecord = self.records(
                index,
                start_ms,
                cost_ms,
                False,
                True,
                module_name,
                cls_name,
                method_name,
                record.args,
                record.kwargs,
                None,
                ret_obj,
            )
            self.__send_full_record_directly(new_record, cmd.out_q, cmd.expand_level, cmd.raw_output, cmd.verbose)

    def delete_specified_record(self, id) -> bool:
        if id in self.invocation_records:
            self.invocation_records.pop(id)
            return True
        return False

    def delete_all_records(self):
        self.invocation_records.clear()
        global_tt_indexer.refresh()


global_time_tunnel_recorder = TimeTunnelRecorder()
