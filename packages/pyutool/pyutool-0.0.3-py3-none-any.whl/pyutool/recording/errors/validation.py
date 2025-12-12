# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : validation.py
@Author  : YL_top01
@Date    : 2025/8/25 16:10
"""





# Built-in modules
from typing import Any

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.errors.base import AppBaseError, BaseCustomError
from pyutool.recording.errors.errors import ErrorMessage

class ValidationError(AppBaseError):
    """校验异常基类"""
    category = "VALIDATION"
    code = 1000

    def __init__(self, message: str, context: dict = None):
        # 添加错误代码到消息
        full_msg = f"[{self.category}-{self.code:04d}] {message}"
        super().__init__(full_msg, context)


class RangeValidationError(ValidationError, ValueError):
    """范围验证失败"""

    def __init__(self, value, min_val, max_val):
        super().__init__(
            f"值 {value} 超出允许范围 ({min_val}-{max_val})"
        )


class FormatValidationError(ValidationError, ValueError):
    """格式验证失败"""

    def __init__(self, value, pattern):
        super().__init__(
            f"值 {value} 不符合格式要求: {pattern}"
        )


class ScopeError(BaseCustomError, Exception):
    '''
        \n obj
        \n iter
        '''

    def __init__(
            self,
            obj: Any,
            iter: Any,
            detail: bool = True,
            location: bool = True
    ):
        message = self._generate_message(
            obj,
            ErrorMessage.scope_error(),
            detail,
            location
        )
        super().__init__(message.format(iter=iter))


class TypeValidationError(ValidationError):
    code = 1001

    def __init__(self, expected, actual):
        super().__init__(f"Type mismatch. Expected {expected}, got {actual.__name__}")


class DatabaseError(AppBaseError):
    """数据库异常"""
    category = "DATABASE"
    code = 3000