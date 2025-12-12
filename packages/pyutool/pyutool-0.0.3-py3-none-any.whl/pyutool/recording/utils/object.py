# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : object
@Author  : YL_top01
@Date    : 2025/8/25 16:00
"""

# Built-in modules
import inspect
import os
from typing import Any
import logging

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)

def locate(obj: Any) -> str:
    """
    定位对象来源

    返回格式: [来源].[类型]: [名称]
    示例: "main.variable: my_var (int)"

    参数:
        obj: 要定位的对象

    返回:
        定位描述字符串
    """
    try:
        # 处理 None 和基本类型
        if obj is None:
            return "main.variable: None (NoneType)"

        # 基本类型处理
        if isinstance(obj, (int, float, str, bool, list, dict, tuple, set)):
            return _locate_basic_type(obj)

        # 模块处理
        if inspect.ismodule(obj):
            return _locate_module(obj)

        # 类处理
        if inspect.isclass(obj):
            return _locate_class(obj)

        # 函数处理
        if inspect.isfunction(obj):
            return _locate_function(obj)

        # 方法处理
        if inspect.ismethod(obj):
            return _locate_method(obj)

        # 实例处理
        if hasattr(obj, '__class__'):
            return _locate_instance(obj)

        return f"Unknown: {type(obj).__name__}"

    except Exception as e:
        logging.warning(f"对象定位失败: {str(e)}")
        return f"Locate Error: {str(e)}"


def _locate_basic_type(obj: Any) -> str:
    """定位基本数据类型"""
    # 尝试通过调用栈查找变量名
    frame = inspect.currentframe()
    while frame:
        local_vars = frame.f_locals
        global_vars = frame.f_globals

        for name, value in {**local_vars, **global_vars}.items():
            if value is obj:
                return f"main.variable: {name} ({type(obj).__name__})"

        frame = frame.f_back

    # 如果调用栈中未找到，返回类型
    return f"main.variable: {type(obj).__name__}"


def _locate_module(obj: Any) -> str:
    """定位模块"""
    try:
        file_path = inspect.getfile(obj)
        file_name = os.path.basename(file_path)
        return f"main.module: {file_name}"
    except TypeError:
        return f"main.module: {obj.__name__}"


def _locate_class(obj: Any) -> str:
    """定位类"""
    module = inspect.getmodule(obj)
    module_name = module.__name__
    is_main = module_name == '__main__'
    prefix = 'main' if is_main else _get_file_name(obj)
    return f"{prefix}.class: {obj.__name__}"


def _locate_function(obj: Any) -> str:
    """定位函数"""
    module = inspect.getmodule(obj)
    module_name = module.__name__
    is_main = module_name == '__main__'
    prefix = 'main' if is_main else _get_file_name(obj)

    if hasattr(obj, '__qualname__'):
        context = obj.__qualname__.split('.')[:-1]
        context_str = '.'.join(context) if context else ''
        return f"{prefix}.{context_str + '.' if context_str else ''}function: {obj.__name__}"
    return f"{prefix}.function: {obj.__name__}"


def _locate_method(obj: Any) -> str:
    """定位方法"""
    return f"method: {obj.__name__}"


def _locate_instance(obj: Any) -> str:
    """定位实例"""
    module = inspect.getmodule(obj)
    module_name = module.__name__
    is_main = module_name == '__main__'
    prefix = 'main' if is_main else _get_file_name(obj)
    return f"{prefix}.example: {type(obj).__name__}"


def _get_file_name(obj: Any) -> str:
    """获取对象所在文件名"""
    try:
        file_path = inspect.getfile(obj)
        return os.path.basename(file_path)
    except (TypeError, AttributeError):
        return "Unknown"


def identify_type(target: Any, detail: bool = False) -> str:
    """
    识别对象类型

    参数:
        target: 要识别的对象
        detail: 是否返回详细信息

    返回:
        类型描述字符串
    """
    try:
        # 处理 None
        if target is None:
            return 'NoneType' if detail else 'None'

        # 基本类型
        if isinstance(target, (int, float, bool, str, list, dict, tuple, set, bytes)):
            return _identify_basic_type(target, detail)

        # 模块
        if inspect.ismodule(target):
            return _identify_module(target, detail)

        # 类
        if inspect.isclass(target):
            return _identify_class(target, detail)

        # 函数
        if inspect.isfunction(target):
            return _identify_function(target, detail)

        # 方法
        if inspect.ismethod(target):
            return _identify_method(target, detail)

        # 实例
        if hasattr(target, '__class__'):
            return _identify_instance(target, detail)

        # 其他情况
        return f'Unknown : {type(target).__name__}' if detail else 'Unknown'

    except Exception as e:
        logging.warning(f"类型识别失败: {str(e)}")
        return f'Identification Error : {str(e)}' if detail else 'Unknown'


def _identify_basic_type(target: Any, detail: bool) -> str:
    """识别基本类型"""
    return f'Basic data : {type(target).__name__}' if detail else 'Basic data'


def _identify_module(target: Any, detail: bool) -> str:
    """识别模块"""
    if detail:
        try:
            return f'module : {os.path.basename(target.__file__)}'
        except AttributeError:
            return f'module : {target.__name__}'
    return 'module'


def _identify_class(target: Any, detail: bool) -> str:
    """识别类"""
    return f'class : {target.__name__}' if detail else 'class'


def _identify_function(target: Any, detail: bool) -> str:
    """识别函数"""
    return f'function : {target.__name__}' if detail else 'function'


def _identify_method(target: Any, detail: bool) -> str:
    """识别方法"""
    return f'method : {target.__name__}' if detail else 'method'


def _identify_instance(target: Any, detail: bool) -> str:
    """识别实例"""
    return f'example : {target.__class__.__name__}' if detail else 'example'

def get_all_subclasses(cls, claude_self:bool=False) -> list:
    """
    获取类的所有子类（递归）

    参数:
        cls: 基类

    返回:
        所有子类的列表
    """
    subclasses = []
    if claude_self:
        subclasses.append(cls)
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        # 递归获取子类的子类
        subclasses.extend(get_all_subclasses(subclass))
    return subclasses
