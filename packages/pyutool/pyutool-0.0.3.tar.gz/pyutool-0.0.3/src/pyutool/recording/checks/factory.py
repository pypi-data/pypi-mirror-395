# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : factory
@Author  : YL_top01
@Date    : 2025/8/25 16:05
"""


# Built-in modules
from enum import Enum


# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.checks.common import CheckLevel





class CheckFactory:
    _executor_registry = {
        "type": (
            "pyutool.recording.checks.type_checker",
            "TypeCheckExecutor"
        ),
        "path": (
            "pyutool.recording.checks.path_checker",
            "PathCheckExecutor"
        ),
        "key": (
            "pyutool.recording.checks.key_checker",
            "KeyCheckExecutor"
        ),
        "range": (
            "pyutool.recording.checks.range_checker",
            "RangeCheckExecutor"
        ),
        "logger": (
            "pyutool.recording.checks.logger_checker",
            "LoggerCheckExecutor"
        ),
        "encoding": (
            "pyutool.recording.checks.encoding_checker",
            "EncodingCheckExecutor"
        ),
        "decorator": (
            "pyutool.recording.checks.decorator_checker",
            "DecoratorCheckExecutor"
        ),
    }

    @staticmethod
    def get_executor(name: str, level: CheckLevel = CheckLevel.LOG):
        """动态导入检查器，打破循环依赖"""
        # 错误：原代码使用了 _executor_map，实际定义的是 _executor_registry
        if name not in CheckFactory._executor_registry:  # 修正此处
            raise ValueError(f"未知的检查器: {name}")

        # 延迟导入：仅在调用时才加载目标模块和类
        module_path, class_name = CheckFactory._executor_registry[name]  # 修正此处
        module = __import__(module_path, fromlist=[class_name])
        executor_class = getattr(module, class_name)

        return executor_class(level)