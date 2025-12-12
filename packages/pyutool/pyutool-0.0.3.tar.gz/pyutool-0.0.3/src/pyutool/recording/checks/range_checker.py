# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : range_checker
@Author  : YL_top01
@Date    : 2025/8/25 16:06
"""

# Built-in modules
# (无内置模块)

# Third-party modules
# (无第三方依赖)

# Local modules

from pyutool.recording.errors.validation import RangeValidationError
from pyutool.recording.checks.checkexecutor_base import CheckExecutor

class RangeCheckExecutor(CheckExecutor):
    """范围检查执行器"""

    def check(self, value: float, min_val: float, max_val: float, context: dict = None) -> bool:
        """检查值是否在范围内"""
        condition = min_val <= value <= max_val
        error = RangeValidationError(value, min_val, max_val)
        return self.execute(condition, error, context)