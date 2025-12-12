# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : parameter
@Author  : YL_top01
@Date    : 2025/8/25 16:05
"""

# Built-in modules
from typing import TYPE_CHECKING

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.errors.base import BaseCustomError
from pyutool.recording.errors.errors import ErrorMessage
from pyutool.recording.errors.functions import check_type


class ParameterError(BaseCustomError):
    """参数相关异常基类"""
    _category = "PARAMETER"


class TooManyParametersError(ParameterError):
    def __init__(self, obj, detail=True, location=True):
        from .functions import safe_type_check  # 避免循环导入
        safe_type_check(obj, 'function')
        msg = self._generate_message(
            obj,
            ErrorMessage.too_parameters_error(),
            detail,
            location
        )
        super().__init__(obj, msg)


class ParameterMissingError(ParameterError):
    """必需参数缺失"""

    def __init__(self, obj, detail=True, location=True):
        if TYPE_CHECKING:
            check_type(obj, 'function')  # 类型检查逻辑
        check_type(obj, 'function')
        msg = self._generate_message(
            obj,
            ErrorMessage.parameter_missing_error(),
            detail,
            location
        )
        super().__init__(obj, msg)


class ParameterTypeError(ParameterError):
    """参数类型不匹配"""

    def __init__(self, obj, expect, actual, switch=False, detail=True, location=True):
        from .functions import check_type
        check_type(obj, 'function')
        msg = self._generate_message(
            obj,
            ErrorMessage.parameter_type_error(expect, actual),
            detail,
            location
        )
        super().__init__(obj, msg)