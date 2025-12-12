"""
异常体系继承关系：
- BaseCustomError: 所有自定义异常的基类（支持错误定位和上下文）
  ├─ ParameterError: 参数相关异常基类
  │  ├─ ParameterMissingError: 必需参数缺失
  │  ├─ TooManyParametersError: 参数数量过多
  │  └─ ParameterTypeError: 参数类型不匹配
  ├─ InvalidPathError: 路径相关异常基类
  │  ├─ PathFormatError: 路径格式非法
  │  └─ PathNotExistsError: 路径不存在
  ├─ eTypeError: 类型不匹配（通用）
  ├─ eKeyError: 键不存在异常
  └─ LoadingError: 资源加载失败

- AppBaseError: 业务异常基类（包含错误分类和代码）
  ├─ ValidationError: 校验异常基类
  │  ├─ RangeValidationError: 范围验证失败
  │  └─ FormatValidationError: 格式验证失败
  └─ DatabaseError: 数据库异常
"""
# Built-in modules
from typing import Any, Optional, Union
from typing import TYPE_CHECKING

# Local modules
from pyutool.recording.utils.object import identify_type, get_all_subclasses
from pyutool.recording.errors.base import BaseCustomError, AppBaseError

if TYPE_CHECKING:
    from pyutool.recording.errors.functions import check_type  # 仅类型检查时导入

# region 双语言消息工厂
class ErrorMessage:
    @staticmethod
    def get_language() -> str:
        try:
            # 延迟导入：在函数内部而非模块顶部导入
            from pyutool.recording.core.logger import LoggerManager
            logger = LoggerManager.get_logger()
            return logger.config.language
        except Exception:
            return 'en'  # 默认语言

    @classmethod
    def type_error(cls, expected, actual) -> str:
        templates = {
            'en': "Expected {expected}, got {actual}",
            'zh': "期望类型 {expected}，实际类型 {actual}"
        }
        return templates[cls.get_language()].format(expected=expected, actual=actual)

    @classmethod
    def parameter_missing_error(cls) -> str:
        templates = {
            'en': "The function [{obj_info}] parameters are missing",
            'zh': "函数 [{obj_info}] 参数丢失"
        }
        return templates[cls.get_language()]

    @classmethod
    def too_parameters_error(cls) -> str:
        templates = {
            'en': "The function [{obj_info}] has too many parameters",
            'zh': "函数 [{obj_info}] 参数过多"
        }
        return templates[cls.get_language()]

    @classmethod
    def parameter_type_error(cls, expect, actual) -> str:
        templates = {
            'en': "Parameter type mismatch, expected {expect}, got {actual}",
            'zh': "参数类型不匹配，期望 {expect}，实际 {actual}"
        }
        return templates[cls.get_language()].format(expect=expect, actual=actual)

    @classmethod
    def example_error(cls, expected_target, actual) -> str:
        templates = {
            'en': "Example type error, expected {expected_target}, got {actual}",
            'zh': "示例类型错误，期望 {expected_target}，实际 {actual}"
        }
        return templates[cls.get_language()].format(
            expected_target=expected_target,
            actual=actual
        )

    @classmethod
    def path_error(cls) -> str:
        templates = {
            'en': "Path error: [{obj_info}]",
            'zh': "路径错误: [{obj_info}]"
        }
        return templates[cls.get_language()]

    @classmethod
    def path_format_error(cls, path) -> str:
        templates = {
            'en': "Invalid path format: {path}",
            'zh': "路径格式非法: {path}"
        }
        return templates[cls.get_language()].format(path=path)

    @classmethod
    def path_not_exists_error(cls, path) -> str:
        templates = {
            'en': "Path does not exist: {path}",
            'zh': "路径不存在: {path}"
        }
        return templates[cls.get_language()].format(path=path)

    @classmethod
    def encode_error(cls) -> str:
        templates = {
            'en': "Encoding error occurred with: {obj}",
            'zh': "编码错误: {obj}"
        }
        return templates[cls.get_language()]

    @classmethod
    def key_error(cls) -> str:
        templates = {
            'en': "Key '{key}' does not exist in [{obj_info}]",
            'zh': "键 '{key}' 在 [{obj_info}] 中不存在"
        }
        return templates[cls.get_language()]

    @classmethod
    def loading_error(cls) -> str:
        templates = {
            'en': "Resource loading failed: [{obj_info}]",
            'zh': "资源加载失败: [{obj_info}]"
        }
        return templates[cls.get_language()]


# endregion

# region 类型检查异常
class ExampleError(BaseCustomError, Exception):
    def __init__(self, obj, expected_target, detail=True, location=True):
        from .functions import check_type  # 避免循环导入
        check_type(expected_target, 'class')
        check_type(obj, 'example')
        message_template = ErrorMessage.example_error(expected_target, identify_type(obj))
        msg = self._generate_message(
            obj,
            message_template.format(expected=expected_target),
            detail,
            location
        )
        super().__init__(msg.format(expect_target=expected_target.__name__))


class eTypeError(BaseCustomError, TypeError):
    """类型错误"""

    def __init__(self, obj: Any, expected_type: Union[type, str], **context):
        actual_type = identify_type(obj, detail=True)
        message = ErrorMessage.type_error(expected_type, actual_type)
        super().__init__(obj, message, expected_type=expected_type, **context)


# endregion

# region 编码异常
class EncodeError(BaseCustomError, Exception):
    def __init__(self, obj, switch=False, detail=True, location=True):
        from .functions import check_type  # 避免循环导入
        check_type(obj, str)
        msg = self._generate_message(
            obj,
            ErrorMessage.encode_error(),
            detail,
            location
        )
        super().__init__(msg.format(obj=obj))
# endregion

# region 其他业务异常
class eKeyError(BaseCustomError, KeyError):
    def __init__(self, obj: Any, key: str, detail: bool = True,
                 location: bool = False, message: Optional[str] = None):
        if message is None:
            message = self._generate_message(
                obj,
                ErrorMessage.key_error(),
                detail,
                location
            )
        super().__init__(message.format(key=key))

class LoadingError(BaseCustomError):
    """资源加载错误"""

    def __init__(self, obj, detail=True, location=True):
        msg = self._generate_message(
            obj,
            ErrorMessage.loading_error(),
            detail,
            location
        )
        super().__init__(obj, msg)

class eAttributeError(BaseCustomError, AttributeError):
    '''
    \n obj
    \n attr_name
    '''

    def __init__(
            self,
            obj: Any,
            attr_name: str,
            detail: bool = True,
            location: bool = True
    ):
        message = self._generate_message(
            obj,
            ErrorMessage.attribute_error(),
            detail,
            location
        )
        super().__init__(message.format(attr_name=attr_name))

class OperationNotAllowed(BaseCustomError, PermissionError):
    """操作不允许异常"""

    def __init__(self, operation: str, obj: Any):
        super().__init__(f"不允许对 {identify_type(obj)} 执行 {operation} 操作")

class BusinessError(AppBaseError):
    """业务异常基类"""
    category = "BUSINESS"
    code = 2000
# endregion



ERRORS = get_all_subclasses(BaseCustomError)
ERRORS.append(get_all_subclasses(AppBaseError))


if __name__ == '__main__':
    for e in [e for e in ERRORS if hasattr(e, "__name__")]:
        print(e.__name__)