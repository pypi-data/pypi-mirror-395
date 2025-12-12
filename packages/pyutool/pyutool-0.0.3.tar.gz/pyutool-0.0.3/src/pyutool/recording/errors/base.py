# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : base
@Author  : YL_top01
@Date    : 2025/8/25 16:05
"""





# Built-in modules
from datetime import datetime
import traceback
from typing import Any

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.utils.object import identify_type, locate

# region 基础异常类
class AppBaseError(Exception):
    """应用基础异常"""
    category = "GENERAL"
    code = 0000

    def __init__(self, message: str, context: dict = None):
        super().__init__(message)
        self.context = context or {}

class BaseCustomError(Exception):
    """基础自定义错误类（重构）"""

    def __init__(self, obj: Any, message: str, **context):
        """
        :param obj: 导致错误的对象
        :param message: 错误消息
        :param context: 错误相关上下文
        """
        super().__init__(message)
        self.obj = obj
        self.context = context or {}
        self.timestamp = datetime.now().isoformat()
        # 自动捕获错误发生时的堆栈
        self.stack_trace = self._capture_stack_trace()
        self.message = message  # 存储原始消息

    def _capture_stack_trace(self) -> str:
        """捕获当前堆栈跟踪"""
        try:
            return "".join(traceback.format_stack(limit=10)[:-2])
        except:
            return "无法获取堆栈跟踪"

    def _generate_message(self, obj: Any, template: str, detail: bool, location: bool) -> str:
        """生成错误消息的默认实现"""
        obj_info = identify_type(obj, detail)
        if location:
            loc = locate(obj)
            return f"{template} | 位置: {loc}"
        return template.format(obj_info=obj_info)

    @property
    def error_type(self) -> str:
        """获取错误类型名称"""
        return type(self).__name__

    def to_dict(self) -> dict:
        """将错误转换为字典格式"""
        return {
            "error_type": self.error_type,
            "message": str(self),
            "object": identify_type(self.obj),
            "timestamp": self.timestamp,
            "stack_trace": self.stack_trace,
            "context": self.context
        }
# endregion