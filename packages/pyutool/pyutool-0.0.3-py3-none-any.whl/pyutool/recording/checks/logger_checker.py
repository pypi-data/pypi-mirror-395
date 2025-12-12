# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : logger_checker.py
@Author  : YL_top01
@Date    : 2025/8/30 11:43
"""



# Built-in modules
# (无内置模块)

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.checks.checkexecutor_base import CheckExecutor
from pyutool.recording.core.logger import LoggerManager


class LoggerCheckExecutor(CheckExecutor):
    """日志系统检查执行器"""

    def check_initialized(self, context: dict = None) -> bool:
        """检查日志系统是否初始化"""
        try:
            LoggerManager.get_default_logger()
            return True
        except Exception:
            condition = False
        error = RuntimeError("日志系统未初始化")
        return self.execute(condition, error, context)