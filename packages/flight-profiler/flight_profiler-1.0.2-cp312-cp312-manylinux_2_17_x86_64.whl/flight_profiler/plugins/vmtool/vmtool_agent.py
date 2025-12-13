import gc
import importlib
import inspect
import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict

from flight_profiler.common.dumps import encode_obj_to_transfer
from flight_profiler.common.expression_result import ExpressionResult
from flight_profiler.plugins.vmtool.vmtool_parser import VmtoolParams
from flight_profiler.utils.render_util import (
    COLOR_END,
    COLOR_GREEN,
    COLOR_ORANGE,
    COLOR_RED,
)


class VmtoolActionExecutor(ABC):

    @abstractmethod
    def do_action(self, params: VmtoolParams) -> Any:
        pass

class ForceGcExecutor(VmtoolActionExecutor):

    def do_action(self, params: VmtoolParams) -> Any:
        try:
            count = gc.collect()
        except:
            return f"ForceGc {COLOR_RED}failed{COLOR_END}, error is: {traceback.format_exc()}"

        return f"{COLOR_GREEN}Gc execute successfully, totally {count} unreachable objects are freed.{COLOR_END}"


class GetInstanceExecutor(VmtoolActionExecutor):

    def do_action(self, params: VmtoolParams):
        module_name = params.module_name
        class_name = params.class_name
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            return (
                f"{COLOR_RED}Error in locating module named "
                f"{COLOR_ORANGE}{module_name}{COLOR_END}{COLOR_RED}. Type: {type(e)}, details: {str(e)}!{COLOR_END}"
            )

        cls = getattr(module, class_name, None)
        if cls is None or not inspect.isclass(cls):
            return (
                f"{COLOR_RED}No class named {COLOR_ORANGE}{class_name}{COLOR_END}{COLOR_RED}"
                f" is found in module {module_name}!{COLOR_END}"
            )

        class_referrers = gc.get_referrers(cls)
        class_instances = []

        cancel_on_limit: bool = False
        upper_bound: int = params.limit
        if params.expr == "instances" and params.limit != -1:
            cancel_on_limit = True

        count: int = 0
        if not cancel_on_limit or upper_bound != 0:
            for obj in class_referrers:
                if isinstance(obj, cls):
                    class_instances.append(obj)
                    count += 1
                    if cancel_on_limit and count >= upper_bound:
                        break

        result: ExpressionResult = ExpressionResult(expr=params.expr)
        try:
            eval_result = params.expression_resolver.eval_target(class_instances)
            result.value = encode_obj_to_transfer(eval_result,
                                                  max_depth=params.expand,
                                                  raw_output=params.raw_output,
                                                  verbose=params.verbose)
            result.type = str(type(eval_result))
        except:
            result.failed = True
            result.failed_reason = traceback.format_exc()

        return result


ACTION_EXECUTOR_INITIATOR: Dict[str, callable] = {
    "getInstances": GetInstanceExecutor,
    "forceGc": ForceGcExecutor,
}


class VmtoolAgent:

    def do_action(self, param: VmtoolParams):
        if param.action not in ACTION_EXECUTOR_INITIATOR:
            return (
                f"{COLOR_RED}Unsupported action {param.action}, current only support "
                f"{COLOR_GREEN}{'|'.join(ACTION_EXECUTOR_INITIATOR.keys())}{COLOR_END}{COLOR_RED}!{COLOR_END}"
            )

        return ACTION_EXECUTOR_INITIATOR[param.action]().do_action(param)


GLOBAL_VMTOOL_AGENT = VmtoolAgent()
