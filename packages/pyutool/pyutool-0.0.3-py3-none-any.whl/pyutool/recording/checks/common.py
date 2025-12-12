# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : common
@Author  : YL_top01
@Date    : 2025/8/30 13:40
"""

# Built-in modules
from enum import Enum

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)


class CheckLevel(Enum):
    """检查执行等级"""
    ASSERT = 1  # 断言式：失败时抛出异常
    BOOL = 2  # 布尔式：返回检查结果布尔值
    LOG = 3  # 日志式：记录错误并返回布尔值