# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : path_checker
@Author  : YL_top01
@Date    : 2025/8/25 16:06
"""

# Built-in modules
import os
import re
from pathlib import Path

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.checks.common import CheckLevel
from pyutool.recording.checks.checkexecutor_base import CheckExecutor
from pyutool.recording.core.logger import record_error
from pyutool.recording.errors.path import PathFormatError, PathNotExistsError
from pyutool.umodules.new_re import StringChecker, PathStyle

class PathCheckExecutor(CheckExecutor):
    def __init__(self, level: CheckLevel = CheckLevel.LOG, debug: bool = False):
        super().__init__(level)
        self.debug = debug

    def check_format(self, path: str, context: dict = None) -> bool:
        """检查路径格式（使用 StringChecker 统一逻辑）"""
        self._log(f"开始验证路径: {path}")
        condition = StringChecker.is_valid_path(path, style=PathStyle.AUTO)
        error = PathFormatError(path)
        return self.execute(condition, error, context)

    def check_exists(self, path: str, context: dict = None) -> bool:
        """检查路径存在"""
        self._log(f"检查路径存在: {path}")
        condition = Path(path).exists()
        error = PathNotExistsError(path)
        return self.execute(condition, error, context)

    def full_check(self, path: str, context: dict = None) -> bool:
        """完整路径检查（格式+存在）"""
        if not self.check_format(path, context):
            return False
        return self.check_exists(path, context)

    def _log(self, message: str):
        """记录调试信息"""
        if self.debug:
            print(f"[PathCheckExecutor] {message}")

    def check_resource_path(self, relative_path: str, context: dict = None) -> str:
        """检查资源路径（自动处理打包环境）"""
        try:
            # 延迟导入：打破循环依赖
            from pyutool.recording.utils.path import get_resource_path
            path = get_resource_path(relative_path, validate=False)

            # 执行完整路径检查
            if self.full_check(path, context):
                return path

            return None
        except Exception as e:
            record_error(e)
            if self.level == CheckLevel.ASSERT:
                raise
            return None