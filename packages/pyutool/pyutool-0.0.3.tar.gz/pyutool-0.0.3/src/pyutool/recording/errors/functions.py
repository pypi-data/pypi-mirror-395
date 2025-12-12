# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : functions
@Author  : YL_top01
@Date    : 2025/8/30 11:55
"""




# Built-in modules
from typing import Union, Any

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.checks.common import CheckLevel
from pyutool.recording.checks.factory import CheckFactory
from pyutool.recording.errors.errors import LoadingError, ExampleError, ERRORS

# region 简化调用函数
def check_type(obj: Any, expected_type: Union[type, str],
               level: CheckLevel = CheckLevel.LOG,
               context: dict = None) -> bool:
    """
    类型检查简化接口

    支持的类型标识符:
      'function' - 普通函数
      'class'    - 类
      'method'   - 方法
      'module'   - 模块
      'example'  - 类实例
      'basic'    - 基本数据类型
      'any'      - 任何类型
    """
    return CheckFactory.get_executor("type", level).check(obj, expected_type, context)


def check_path(path: str, check_exists: bool = False,
               level: CheckLevel = CheckLevel.LOG,
               context: dict = None) -> bool:
    """路径检查简化接口（增强版）"""
    executor = CheckFactory.get_executor("path", level)
    if not executor.check_format(path, context):
        return False
    if check_exists:
        return executor.check_exists(path, context)

    return True


def check_key(container: dict, key: str,
              level: CheckLevel = CheckLevel.LOG,
              context: dict = None) -> bool:
    """键检查简化接口"""
    return CheckFactory.get_executor("key", level).check(container, key, context)


def check_range(value: float, min_val: float, max_val: float,
                level: CheckLevel = CheckLevel.LOG,
                context: dict = None) -> bool:
    """范围检查简化接口"""
    return CheckFactory.get_executor("range", level).check(value, min_val, max_val, context)


def check_encoding(encoding: str,
                   level: CheckLevel = CheckLevel.LOG,
                   context: dict = None) -> bool:
    """编码检查简化接口"""
    return CheckFactory.get_executor("encoding", level).check(encoding, context)


def check_function(func: callable,
                   level: CheckLevel = CheckLevel.LOG,
                   context: dict = None) -> bool:
    """函数检查简化接口"""
    return CheckFactory.get_executor("decorator", level).check_function(func, context)


def check_decorator(decorator: callable,
                    level: CheckLevel = CheckLevel.LOG,
                    context: dict = None) -> bool:
    """装饰器检查简化接口"""
    return CheckFactory.get_executor("decorator", level).check_decorator(decorator, context)


def check_logger_initialized(level: CheckLevel = CheckLevel.LOG,
                             context: dict = None) -> bool:
    """日志系统初始化检查"""
    return CheckFactory.get_executor("logger", level).check_initialized(context)


def check_resource_path(relative_path: str,
                        level: CheckLevel = CheckLevel.LOG,
                        context: dict = None) -> Union[str, bool]:
    """
    资源路径检查简化接口

    返回:
        验证成功时返回绝对路径，失败时根据level返回：
          - ASSERT: 抛出异常
          - BOOL: 返回False
          - LOG: 返回None并记录错误
    """
    executor = CheckFactory.get_executor("path", level)
    return executor.check_resource_path(relative_path, context)


# endregion

def record_loading_error(logger: 'Logger', e, msg: str, *arg, **kwargs) -> None:  # 用字符串注解避免提前导入
    # 在函数内部延迟导入 Logger
    from pyutool.recording.core.logger import Logger
    if check_type(logger, Logger, CheckLevel.BOOL):
        if e in ERRORS:
            error = e(*arg, **kwargs)
        else:
            error = LoadingError(e)
        logger.record_error(error, msg)
    else:
        raise ExampleError(logger, Logger)


def safe_type_check(obj: Any, expected_type: Union[type, str],
                   context: dict = None) -> bool:
    """
    安全的类型检查（不抛出异常，仅返回检查结果）
    功能与check_type类似，但强制使用CheckLevel.BOOL避免抛出异常
    """
    return CheckFactory.get_executor("type", CheckLevel.BOOL).check(obj, expected_type, context)