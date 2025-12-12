# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : type_checker
@Author  : YL_top01
@Date    : 2025/8/25 16:06
"""


# Built-in modules
import inspect
from typing import Union, Any

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.checks.checkexecutor_base import CheckExecutor
from pyutool.recording.errors.errors import eTypeError
from pyutool.recording.utils.object import identify_type


class TypeCheckExecutor(CheckExecutor):
    """类型检查执行器（支持类型标识符）"""

    # 类型标识符映射
    TYPE_IDENTIFIERS = {
        'function': inspect.isfunction,
        'class': inspect.isclass,
        'method': inspect.ismethod,
        'module': inspect.ismodule,
        'example': lambda obj: not any([
            inspect.ismodule(obj),
            inspect.isclass(obj),
            inspect.isfunction(obj),
            inspect.ismethod(obj)
        ]) and hasattr(obj, '__class__'),
        'basic': lambda obj: isinstance(obj, (int, float, bool, str, list, dict, tuple, set, bytes)),
        'any': lambda obj: True
    }

    def check(self, obj: Any, expected_type: Union[type, str], context: dict = None) -> bool:
        """执行类型检查，支持类型标识符"""
        # 处理类型标识符
        if isinstance(expected_type, str):
            check_func = self.TYPE_IDENTIFIERS.get(expected_type.lower())
            if check_func is None:
                raise ValueError(f"无效的类型标识符: {expected_type}")

            condition = check_func(obj)
            actual_type = identify_type(obj, detail=True)
        # 处理标准类型检查
        else:
            condition = isinstance(obj, expected_type)
            actual_type = type(obj).__name__

        error = eTypeError(obj, expected_type, actual_type=actual_type)
        return self.execute(condition, error, context)
