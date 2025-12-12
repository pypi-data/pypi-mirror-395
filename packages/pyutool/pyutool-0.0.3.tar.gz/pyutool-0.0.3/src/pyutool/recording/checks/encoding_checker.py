# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : encoding_checker.py
@Author  : YL_top01
@Date    : 2025/8/30 11:43
"""





# Built-in modules
import codecs

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.checks.checkexecutor_base import CheckExecutor
from pyutool.recording.errors.errors import EncodeError


class EncodingCheckExecutor(CheckExecutor):
    """编码检查执行器"""

    def check(self, encoding: str, context: dict = None) -> bool:
        """检查编码是否有效"""
        try:
            codecs.lookup(encoding)
            return True
        except LookupError:
            condition = False
        error = EncodeError(encoding)
        return self.execute(condition, error, context)