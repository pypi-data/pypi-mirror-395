# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : path
@Author  : YL_top01
@Date    : 2025/8/25 15:59
"""
import sys
# Built-in modules
from pathlib import Path
import os
import warnings
import datetime

from pyutool.recording.checks.factory import CheckLevel
from pyutool.recording.core.logger import record_error
from pyutool.recording.errors.functions import check_path
from pyutool.recording.errors.path import InvalidPathError


# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)



class PathManager:
    @staticmethod
    def resolve_log_path(config) -> Path:
        """解析最终日志路径（迁移自Logger._resolve_paths）"""
        base_dir = Path(config.base_dir) if config.base_dir else Path.cwd()
        log_dir = Path(config.log_dir)
        if not log_dir.is_absolute():
            log_dir = base_dir / log_dir

        # 处理按日期分割的目录
        if config.enable_daily:
            date_dir = datetime.now().strftime(config.date_dir_format)
            log_dir = log_dir / date_dir
        return log_dir.resolve()

    @staticmethod
    def validate_log_path(path: Path, expected_parent: Path):
        """验证路径安全性（迁移自Logger._validate_paths）"""
        if any(kw in str(path) for kw in ["pytest-of", "Temp", "tmp"]):
            return
        if not str(path).startswith(str(expected_parent)):
            warnings.warn(f"Log path outside expected directory: {path}", RuntimeWarning)

    @staticmethod
    def ensure_dir_exists(path: Path):
        """确保目录存在（迁移自Logger初始化逻辑）"""
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

class PathValidator:
    """增强型路径验证器（支持资源路径验证）"""

    def __init__(self, level=CheckLevel.ASSERT, debug:bool=True):
        from src.pyutool.recording.checks.path_checker import PathCheckExecutor
        self.executor = PathCheckExecutor(level, debug)

    def validate_resource_path(self, relative_path: str) -> str:
        """验证并返回资源路径（自动处理打包环境）"""
        try:
            path = get_resource_path(relative_path)
            self.executor.full_check(path)
            return path
        except InvalidPathError as e:
            record_error(e)
            if self.executor.level == CheckLevel.ASSERT:
                raise
            return None

    def is_valid_resource_path(self, relative_path: str) -> bool:
        """检查资源路径是否有效（不抛出异常）"""
        try:
            path = get_resource_path(relative_path)
            return self.executor.full_check(path)
        except Exception:
            return False


# region 路径辅助函数
def get_resource_path(relative_path: str, validate: bool = True) -> str:
    """
    获取资源的绝对路径（支持开发环境和PyInstaller打包环境）

    参数:
        relative_path: 资源的相对路径
        validate: 是否验证路径存在性（默认为True）

    返回:
        资源的绝对路径

    异常:
        当validate=True且路径不存在时抛出PathNotExistsError
    """
    # 确定基础路径（PyInstaller打包环境使用_MEIPASS）
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS  # PyInstaller临时解压目录
    else:
        # 获取当前脚本所在目录（开发环境）
        base_dir = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(base_dir, relative_path)
    normalized_path = os.path.normpath(full_path)

    if validate:
        check_path(normalized_path, check_exists=True, level=CheckLevel.ASSERT)

    return normalized_path


# endregion