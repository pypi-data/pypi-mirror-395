# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : checkexecutor_base
@Author  : YL_top01
@Date    : 2025/8/30 13:24
"""

# Built-in modules


# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.core.logger import record_error
from pyutool.recording.checks.common import CheckLevel




class CheckExecutor:
    """
    检查执行器基类，统一管理检查逻辑的执行策略。

    提供三种检查模式：
    - ASSERT：检查失败时立即抛出异常
    - BOOL：返回布尔值表示检查结果，不抛异常
    - LOG：记录错误日志并返回布尔值

    用法示例：
    >>> executor = CheckExecutor(CheckLevel.ASSERT)
    >>> executor.execute(1 > 2, ValueError("1不大于2"))  # 抛出异常
    """

    def __init__(self, level: CheckLevel = CheckLevel.LOG):
        self.level = level

    def execute(self, condition: bool, error: Exception, context: dict = None) -> bool:
        """
        执行检查的统一入口

        参数:
            condition: 检查条件（True表示通过，False表示失败）
            error: 检查失败时的异常对象
            context: 错误上下文（用于日志记录）

        返回:
            bool: 检查是否通过
        """
        if condition:
            return True

        if self.level == CheckLevel.ASSERT:
            raise error
        elif self.level == CheckLevel.BOOL:
            return False
        elif self.level == CheckLevel.LOG:
            record_error(error, context)
            return False