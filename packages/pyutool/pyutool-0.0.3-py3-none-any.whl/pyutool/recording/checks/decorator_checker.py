# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : decorator_checker.py
@Author  : YL_top01
@Date    : 2025/8/25 14:44
"""

# Built-in modules
import inspect
import functools
import warnings
from typing import Optional, Callable, Any, get_origin, get_args, Tuple, Type, List, Union
from datetime import datetime

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.checks.checkexecutor_base import CheckExecutor, CheckLevel
from pyutool.recording.core.logger import LoggerManager
from pyutool.recording.errors.base import BaseCustomError
from pyutool.recording.errors.errors import eTypeError
from pyutool.recording.errors.functions import check_type, check_logger_initialized, check_function
from pyutool.recording.errors.parameter import ParameterMissingError, TooManyParametersError, ParameterTypeError
from pyutool.recording.errors.validation import ValidationError
from pyutool.recording.utils.object import locate


class DecoratorCheckExecutor(CheckExecutor):
    """装饰器检查执行器"""

    def check_function(self, func: callable, context: dict = None) -> bool:
        """检查对象是否为函数"""
        condition = inspect.isfunction(func)
        error = eTypeError(func, "function")
        return self.execute(condition, error, context)

    def check_decorator(self, decorator: callable, context: dict = None) -> bool:
        """检查对象是否为有效的装饰器"""
        condition = inspect.isfunction(decorator) and len(inspect.signature(decorator).parameters) == 1
        error = ValidationError("无效的装饰器格式")
        return self.execute(condition, error, context)



# region 验证装饰器 - 改进错误处理
# 辅助函数：解析类型注解，返回（原始类型，泛型参数）
def resolve_type_annotation(annotation: Any) -> Tuple[Type, List[Type]]:
    """
    解析类型注解，提取原始类型和泛型参数
    示例：
    - List[str] → (list, [str])
    - Dict[str, int] → (dict, [str, int])
    - str → (str, [])
    - Union[int, str] → (Union[int, str], [])
    """
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is None:
        # 不是泛型类型（如 str、int、Union）
        return annotation, []
    else:
        # 是泛型类型（如 List[str] → origin=list，args=[str]）
        return origin, list(args)


# 辅助函数：校验单个值是否符合类型注解（支持泛型）
def check_value_type(value: Any, expected_type: Any) -> bool:
    """
    检查值是否符合期望类型（支持泛型、Union、Optional）
    示例：
    - check_value_type([1,2], List[int]) → True
    - check_value_type("abc", str) → True
    - check_value_type(None, Optional[str]) → True
    - check_value_type(123, Union[int, str]) → True
    """
    # 处理 Union 类型（包括 Optional）
    if get_origin(expected_type) is Union:
        union_args = get_args(expected_type)
        # 只要值符合 Union 中的任意一个类型，就返回 True
        return any(check_value_type(value, arg_type) for arg_type in union_args)

    # 处理 None 类型（单独判断，避免和泛型冲突）
    if expected_type is None or expected_type is type(None):
        return value is None

    # 解析泛型类型（原始类型 + 泛型参数）
    origin_type, generic_args = resolve_type_annotation(expected_type)

    # 1. 先校验原始类型（如 List[str] → 先检查是否是 list）
    if not isinstance(value, origin_type):
        return False

    # 2. 若有泛型参数，进一步校验元素类型
    if generic_args:
        if origin_type is list:
            # 列表：所有元素必须符合泛型参数（如 List[str] → 所有元素是 str）
            elem_type = generic_args[0]
            return all(check_value_type(elem, elem_type) for elem in value)
        elif origin_type is dict:
            # 字典：key 符合第一个泛型参数，value 符合第二个（如 Dict[str, int]）
            if len(generic_args) < 2:
                return True
            key_type, val_type = generic_args
            return (all(check_value_type(k, key_type) for k in value.keys()) and
                    all(check_value_type(v, val_type) for v in value.values()))
        # 其他泛型（如 Tuple、Set）可按需扩展
    return True


def validate_parameters(enable_type_check=True):
    """参数校验装饰器，支持类型检查（含泛型）、忽略self/cls、处理*args/**kwargs"""

    def decorator(func):
        sig = inspect.signature(func)
        param_types = {}
        var_positional_type = None  # 存储 *args 的类型注解
        var_keyword_type = None  # 存储 **kwargs 的类型注解

        # 收集参数类型，忽略 self 和 cls，单独处理 *args 和 **kwargs
        for name, param in sig.parameters.items():
            if name in ('self', 'cls'):
                continue
            if param.annotation == inspect.Parameter.empty:
                continue

            if param.kind == param.VAR_POSITIONAL:  # 处理 *args
                var_positional_type = param.annotation
            elif param.kind == param.VAR_KEYWORD:  # 处理 **kwargs
                var_keyword_type = param.annotation
            else:  # 普通参数
                param_types[name] = param.annotation

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 参数绑定校验
                try:
                    bound = sig.bind(*args, **kwargs)
                except TypeError as e:
                    err_msg = str(e)
                    if "missing" in err_msg:
                        raise ParameterMissingError(func) from e
                    elif "too many" in err_msg:
                        raise TooManyParametersError(func) from e

                # 类型校验
                if enable_type_check:
                    # 1. 检查普通参数（支持泛型）
                    for name, value in bound.arguments.items():
                        if name in param_types:
                            expected_type = param_types[name]
                            if not check_value_type(value, expected_type):
                                # 格式化错误信息（显示泛型类型）
                                expect_str = str(expected_type).replace("typing.", "")
                                actual_str = f"{type(value).__name__}({value})"
                                raise ParameterTypeError(
                                    func,
                                    expect=expect_str,
                                    actual=actual_str,
                                    param_name=name
                                )

                    # 2. 检查 *args (可变位置参数，支持泛型)
                    if var_positional_type is not None:
                        args_value = bound.arguments.get(sig.var_positional)
                        if args_value is not None:
                            for idx, arg in enumerate(args_value):
                                if not check_value_type(arg, var_positional_type):
                                    expect_str = str(var_positional_type).replace("typing.", "")
                                    actual_str = f"{type(arg).__name__}({arg})"
                                    raise ParameterTypeError(
                                        func,
                                        expect=expect_str,
                                        actual=actual_str,
                                        param_name=f"*args[{idx}]"
                                    )

                    # 3. 检查 **kwargs (可变关键字参数，支持泛型)
                    if var_keyword_type is not None:
                        kwargs_value = bound.arguments.get(sig.var_keyword)
                        if kwargs_value is not None:
                            for key, value in kwargs_value.items():
                                if not check_value_type(value, var_keyword_type):
                                    expect_str = str(var_keyword_type).replace("typing.", "")
                                    actual_str = f"{type(value).__name__}({value})"
                                    raise ParameterTypeError(
                                        func,
                                        expect=expect_str,
                                        actual=actual_str,
                                        param_name=f"**kwargs['{key}']"
                                    )

                return func(*args, **kwargs)
            except Exception as e:
                # 保留你原有日志记录逻辑（record_error(e)）
                # record_error(e)  # 若已定义，取消注释
                raise

        return wrapper

    return decorator


# 高效版
def validate_class_parameters(enable_type_check=True, exclude_methods=None):
    """
    类装饰器：为类中的所有方法自动添加参数校验。

    :param enable_type_check: 是否启用类型检查
    :param exclude_methods: 需要排除的方法名列表（例如 ['__init__', 'internal_method']）
    """
    if exclude_methods is None:
        exclude_methods = []

    def decorator(cls):
        # 遍历类的所有属性
        for attr_name, attr_value in cls.__dict__.items():
            # 检查是否是函数，并且不在排除列表中
            if callable(attr_value) and attr_name not in exclude_methods:
                # 为这个方法应用 validate_parameters 装饰器
                decorated_method = validate_parameters(enable_type_check)(attr_value)
                # 将装饰后的方法重新赋值给类
                setattr(cls, attr_name, decorated_method)
        return cls

    return decorator
# endregion



def log_function_errors(
        logger_name: Optional[str] = None,
        log_level: str = "ERROR",
        continue_on_error: bool = True,
        capture_args: bool = True
) -> Callable:
    """函数错误日志装饰器，适配游戏开发场景（复用现有检查执行器）"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 1. 复用 LoggerCheckExecutor 检查日志系统是否初始化（符合现有架构）
            logger_initialized = check_logger_initialized(level=CheckLevel.BOOL)
            if not logger_initialized:
                warnings.warn("日志系统未初始化，无法记录函数错误", RuntimeWarning)
                if not continue_on_error:
                    raise RuntimeError("日志系统未初始化，终止执行")
                return None  # 日志未初始化时的安全返回

            # 2. 复用现有检查执行器验证函数类型（确保装饰的是有效函数）
            if not check_function(func, level=CheckLevel.BOOL):
                warnings.warn(f"@{log_function_errors.__name__} 只能装饰函数对象", RuntimeWarning)
                return func(*args, **kwargs)  # 非函数对象直接执行，不处理

            # 3. 获取日志器（复用现有 LoggerManager）
            logger = LoggerManager.get_logger(logger_name) if logger_name else LoggerManager.get_logger()

            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 4. 构建错误上下文（复用 utils.locate 工具）
                context = {
                    "function": f"{func.__module__}.{func.__name__}",
                    "location": locate(func),
                    "timestamp": datetime.now().isoformat()
                }

                # 5. 捕获函数参数（控制长度避免日志膨胀）
                if capture_args:
                    context["args"] = str(args)[:500]
                    context["kwargs"] = str(kwargs)[:500]

                # 6. 记录异常（区分自定义与系统异常）
                if isinstance(e, BaseCustomError):
                    # 自定义异常直接记录（复用 record_error 逻辑）
                    logger.record_error(e, extra_context=context)
                else:
                    # 系统异常转换为自定义异常（复用 eTypeError）
                    custom_err = eTypeError(
                        obj=func,
                        expected_type="valid execution",
                        message=f"Function error: {str(e)}", **context
                    )
                    logger.record(log_level, str(custom_err), context)

                # 7. 控制是否中断执行（游戏场景默认不中断）
                if not continue_on_error:
                    raise

                # 8. 返回默认值（基于函数返回注解，兼容现有类型检查逻辑）
                return_type = func.__annotations__.get("return")
                if return_type is None:
                    return None
                # 对基础类型返回默认值（复用 TypeCheckExecutor 的基础类型判断）
                if check_type(return_type, "basic", level=CheckLevel.BOOL):
                    return return_type() if return_type != type(None) else None
                return None

        return wrapper

    return decorator


def require_logger(func):
    """确保日志系统已初始化的装饰器"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not check_logger_initialized(level=CheckLevel.BOOL):
            warnings.warn("请先初始化日志系统", RuntimeWarning)
            return None
        return func(*args, **kwargs)

    return wrapper