import importlib
import pickle
import traceback
from typing import Any

from flight_profiler.common.dumps import encode_obj_to_transfer
from flight_profiler.common.expression_result import ExpressionResult
from flight_profiler.plugins.getglobal.getglobal_parser import GetGlobalParams
from flight_profiler.utils.render_util import COLOR_END, COLOR_ORANGE, COLOR_RED


class GetGlobalAgent:

    def search_global_var(self, params: GetGlobalParams) -> bytes:
        module_name: str = params.module_name
        class_name: str = params.class_name
        var_name: str = params.variable

        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            return pickle.dumps(
                f"{COLOR_RED}Error in locating module named "
                f"{COLOR_ORANGE}{module_name}{COLOR_END}{COLOR_RED}. Type: {type(e)}, details: {str(e)}!{COLOR_END}"
            )

        if class_name is None:
            if var_name in module.__dict__:
                instance = module.__dict__[var_name]
                result_map = self.__build_result(instance, params)
                return pickle.dumps(result_map)
            else:
                return pickle.dumps(
                    f"{COLOR_RED}No global variable named {COLOR_ORANGE}{var_name}{COLOR_END}{COLOR_RED}"
                    f" is found in module {module_name}!{COLOR_END}"
                )
        else:
            cls = getattr(module, class_name, None)
            if cls is None:
                return pickle.dumps(
                    f"{COLOR_RED}No class named {COLOR_ORANGE}{class_name}{COLOR_END}{COLOR_RED}"
                    f" is found in module {module_name}!"
                )

            try:
                var = getattr(cls, var_name)
            except AttributeError:
                return pickle.dumps(
                    f"{COLOR_RED}No static variable named {COLOR_ORANGE}{class_name}{COLOR_END}{COLOR_RED}"
                    f" is found in module {module_name}!{COLOR_END}"
                )
            return pickle.dumps(
                self.__build_result(var, params)
            )

    def __build_result(self, instance: Any, params: GetGlobalParams) -> ExpressionResult:
        result: ExpressionResult = ExpressionResult(expr=params.expr)
        try:
            eval_result = params.expr_resolver.eval_target(instance)
            result.value = encode_obj_to_transfer(eval_result,
                                                  max_depth=params.expand_level,
                                                  raw_output=params.raw_output,
                                                  verbose=params.verbose)
            result.type = str(type(eval_result))
        except:
            result.failed = True
            result.failed_reason = traceback.format_exc()
        return result


GlobalGetGlobalAgent = GetGlobalAgent()
