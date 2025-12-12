# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : path
@Author  : YL_top01
@Date    : 2025/8/25 16:04
"""



# Built-in modules
# (无内置模块)

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.errors.base import BaseCustomError
from pyutool.recording.errors.errors import ErrorMessage


class InvalidPathError(BaseCustomError, Exception):
    """基础路径错误（改为接受外部消息，不再内部生成）"""
    def __init__(self, obj, message, detail=True, location=True):  # 新增message参数
        # 移除内部生成msg的逻辑，直接使用传入的message
        super().__init__(obj, message)


class PathFormatError(InvalidPathError):
    """路径格式非法"""
    def __init__(self, path: str):
        # 使用path_format_error模板，包含具体路径
        message = ErrorMessage.path_format_error(path)
        # 正确传递参数给父类：obj=路径, message=格式化后的消息
        super().__init__(obj=path, message=message)


class PathNotExistsError(InvalidPathError):
    """路径不存在"""

    def __init__(self, path: str):
        message = ErrorMessage.path_not_exists_error(path)
        super().__init__(path, message)

