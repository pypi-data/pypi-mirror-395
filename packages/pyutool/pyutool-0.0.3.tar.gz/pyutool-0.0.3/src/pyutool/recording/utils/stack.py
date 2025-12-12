# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : stack
@Author  : YL_top01
@Date    : 2025/8/25 15:59
"""


# Built-in modules
import inspect
from pathlib import Path
from typing import Optional, Tuple

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)

def get_caller_location(skip_keywords: Optional[list] = None) -> Tuple[str, int]:
    """
    获取调用者代码位置

    参数:
        skip_keywords: 需要跳过的路径关键词列表

    返回:
        (filename, lineno): 文件名（不含路径）和行号
    """
    skip_keywords = skip_keywords or [
        "pyutool/recording",
        "logging/__init__",
        "site-packages"
    ]

    stack = inspect.stack()
    for frame_info in stack[1:]:  # 跳过当前函数本身
        frame = frame_info.frame
        filename = inspect.getframeinfo(frame).filename

        # 检查是否需要跳过
        if any(key in filename for key in skip_keywords):
            continue

        return (
            Path(filename).name,  # 仅保留文件名
            frame_info.lineno
        )

    return ("unknown", 0)