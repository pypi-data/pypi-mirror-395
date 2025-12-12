# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : key_checker.py
@Author  : YL_top01
@Date    : 2025/8/30 11:40
"""

# Built-in modules
# (无内置模块)

# Third-party modules
# (无第三方依赖)

# Local modules

from pyutool.recording.errors.errors import eKeyError
from pyutool.recording.checks.checkexecutor_base import CheckExecutor

class KeyCheckExecutor(CheckExecutor):
    """键检查执行器"""

    def check(self, container: dict, key: str, context: dict = None) -> bool:
        """检查键是否存在"""
        condition = key in container
        error = eKeyError(container, key)
        return self.execute(condition, error, context)