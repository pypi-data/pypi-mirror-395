import pickle
import traceback
from typing import Any, Optional

from flight_profiler.common.dumps import encode_obj_to_transfer
from flight_profiler.common.expression_resolver import MethodInvocationExprResolver
from flight_profiler.common.system_logger import logger


class WatchResult:

    def __init__(
        self,
        method_identifier: str = None,
        cost_ms: float = None,
        is_exp: bool = False,
        exception: str = None,
        start_ms: int = None,
        expr: str = None,
        filter_expr: str = None,
        watch_fail_info: Optional[str] = None,
        filter_fail_info: Optional[str] = None,
        type: str = None,
        value: Any = None,
    ):
        self.method_identifier = method_identifier
        self.cost_ms = cost_ms
        self.exception = exception
        self.filter_expr = filter_expr
        self.is_exp = is_exp
        self.watch_fail_info = watch_fail_info
        self.filter_fail_info = filter_fail_info
        self.value = value
        self.start_time = start_ms
        self.type = type
        self.expr = expr


class WatchDisplayer(object):
    def __init__(self, expr: str, expand_level: int, method_identifier: str, raw_output: bool,
                 verbose: bool):
        self.expr = expr
        self.verbose = verbose
        self.expr_resolver: MethodInvocationExprResolver = MethodInvocationExprResolver(
            self.expr
        )
        self.expand_level: int = expand_level
        self.raw_output = raw_output
        self.method_identifier: str = method_identifier

    def dump(self, start_time, target_obj, time_cost, return_obj, *args, **kwargs):
        value = None
        failed_info = None
        try:
            value = self.expr_resolver.eval(target_obj, return_obj, *args, **kwargs)
        except Exception as e:
            failed_info = traceback.format_exc()
            logger.exception("[WatchDisplayer] parse expression failed.")
        watch_result = WatchResult(
            method_identifier=self.method_identifier,
            cost_ms=time_cost,
            is_exp=False,
            start_ms=start_time,
            expr=self.expr,
            watch_fail_info=failed_info,
            type=str(type(value)),
            value=encode_obj_to_transfer(value, self.expand_level, self.raw_output,
                                         verbose=self.verbose),
        )
        return pickle.dumps(watch_result)

    def dump_error(self, start_time, target_obj, time_cost, err_text, *args, **kwargs):
        value = None
        failed_info = None
        try:
            value = self.expr_resolver.eval(target_obj, None, *args, **kwargs)
        except Exception as e:
            failed_info = traceback.format_exc()
            logger.exception("[WatchDisplayer] parse expression failed.")
        watch_result = WatchResult(
            method_identifier=self.method_identifier,
            cost_ms=time_cost,
            is_exp=True,
            exception=err_text,
            start_ms=start_time,
            expr=self.expr,
            watch_fail_info=failed_info,
            type=str(type(value)),
            value=encode_obj_to_transfer(value, self.expand_level, self.raw_output,
                                         verbose=self.verbose),
        )
        return pickle.dumps(watch_result)
