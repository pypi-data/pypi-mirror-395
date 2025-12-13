import uuid
from typing import Any


class ExpressionResolver:

    def eval(self, target_obj: Any, return_obj: Any, *args, **kwargs) -> Any:
        """
        :param target_obj: invocation current obj is a class method
        :param return_obj: if this is a method invocation
        :param args: method invocation args
        :param kwargs: method invocation kwargs
        """
        pass

    def eval_target(self, target_obj: Any) -> Any:
        """
        :param target_obj: varies depend on command types
        """
        pass

    def eval_filter(
        self, target_obj: Any, return_obj: Any, cost: int, *args, **kwargs
    ) -> Any:
        """
        :param target_obj: varies depend on command types
        """
        pass


class MethodInvocationExprResolver(ExpressionResolver):

    def __init__(self, expr: str):
        """
        expr format: python right value statement, target/return_obj/throwExp/args/kwargs
        """

        self.__expr = expr
        uid = str(uuid.uuid4())
        self.__func_name = f"expr_func_{uid.replace('-', '_')}"
        self.__code = f"def {self.__func_name}(target, return_obj, *args, **kwargs): return {self.__expr}"

    def eval(self, target_obj: Any, return_obj: Any, *args, **kwargs) -> Any:
        namespace = {}
        exec(self.__code, globals(), namespace)
        return namespace[self.__func_name](target_obj, return_obj, *args, **kwargs)


class InstanceExprResolver(ExpressionResolver):

    def __init__(self, expr: str):
        """
        expr format: python right value statement, target
        """

        self.__expr = expr
        uid = str(uuid.uuid4())
        self.__func_name = f"expr_func_{uid.replace('-', '_')}"
        self.__code = f"def {self.__func_name}(target): return {self.__expr}"

    def eval_target(self, target_obj: Any) -> Any:
        namespace = {}
        exec(self.__code, globals(), namespace)
        return namespace[self.__func_name](target_obj)


class InstanceListExprResolver(ExpressionResolver):

    def __init__(self, expr: str):
        """
        expr format: python right value statement, instances
        """

        self.__expr = expr
        uid = str(uuid.uuid4())
        self.__func_name = f"expr_func_{uid.replace('-', '_')}"
        self.__code = f"def {self.__func_name}(instances): return {self.__expr}"

    def eval_target(self, target_obj: Any) -> Any:
        namespace = {}
        exec(self.__code, globals(), namespace)
        return namespace[self.__func_name](target_obj)


class FilterExprResolver(ExpressionResolver):

    def __init__(self, expr: str):
        """
        expr format: python right value statement, target/return_obj/cost/args/kwargs
        """

        self.__expr = expr
        uid = str(uuid.uuid4())
        self.__func_name = f"expr_func_{uid.replace('-', '_')}"
        self.__code = f"def {self.__func_name}(target, return_obj, cost, *args, **kwargs): return {self.__expr}"

    def eval_filter(
        self, target_obj: Any, return_obj: Any, cost: float, *args, **kwargs
    ) -> False:

        if self.__expr is not None:
            namespace = {}
            exec(self.__code, globals(), namespace)
            ok = namespace[self.__func_name](
                target_obj, return_obj, cost, *args, **kwargs
            )
            if not ok:
                return False
        return True
