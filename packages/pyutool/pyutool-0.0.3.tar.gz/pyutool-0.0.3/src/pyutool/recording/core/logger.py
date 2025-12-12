# logger.py
"""核心日志记录模块"""
# Built-in modules
import logging
import inspect
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from collections import defaultdict
import threading
import traceback
import json
import warnings
import types
from typing import ClassVar


# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording.core.config import LogConfig
from pyutool.recording.errors.base import BaseCustomError
from pyutool.recording.errors.errors import eTypeError
from pyutool.recording.errors.functions import check_type
from pyutool.recording.utils.object import locate, identify_type


class JSONContextFormatter(logging.Formatter):
    def __init__(self, fmt, style='{', *args, **kwargs):
        super().__init__(fmt, style=style, *args, **kwargs)

    def formatTime(self, record, datefmt=None):
        if datefmt:
            return datetime.fromtimestamp(record.created).strftime(datefmt)
        return super().formatTime(record, datefmt)

    def format(self, record):
        try:
            # 确保所有字段都有默认值
            fields = [
                'log_timestamp', 'log_level', 'log_message',
                'log_file', 'log_line', 'log_function', 'log_context'
            ]

            for field in fields:
                if not hasattr(record, field):
                    setattr(record, field, "")

            # 添加时间格式化
            record.log_asctime = self.formatTime(record, self.datefmt)

            return super().format(record)
        except Exception as e:
            # 返回简化错误消息
            return f"FORMAT ERROR: {str(e)}"

    def _get_caller_frame(self, record):
        """获取调用者栈帧（跳过日志系统内部调用）"""
        frame = inspect.currentframe()
        # 向上追踪直到跳出日志模块
        while frame:
            frame = frame.f_back
            path = frame.f_code.co_filename if frame else ""
            # 跳过日志系统内部调用栈
            if "pyutoolpyutool/recording" not in path and "logging/__init__.py" not in path:
                break
        return frame


class Logger:
    """
    日志记录器核心类，负责日志的格式化、写入和轮转管理。

    特性：
    - 支持多线程安全写入（基于RLock）
    - 按大小/日期自动轮转日志
    - 多语言错误消息支持
    - 上下文信息自动捕获（调用文件/行号/函数）

    用法示例：
    >>> config = LogConfig(name="my_app", log_dir="logs")
    >>> logger = LoggerManager.create_logger("my_app", config)
    >>> logger.record("INFO", "应用启动成功")
    """

    def __init__(self, config: LogConfig):
        self.config = config
        self.__name__ = "Logger"
        self._validate_config()  # 先校验配置
        self._resolve_paths()  # 再解析路径
        self.stats = defaultdict(int)  # 确保统计字典存在
        self._lock = threading.RLock()  # 改用可重入锁
        self._write_lock = threading.RLock()
        self._setup_handlers()  # 最后初始化处理器
        self.safe_rollover = self._safe_rollover  # 添加公共方法

    def record(self, level: str, message: str, context: dict = None):
        """
        记录一条日志

        参数：
            level: 日志级别（INFO/DEBUG/ERROR等）
            message: 日志文本内容
            context: 额外上下文信息（字典格式，将被JSON序列化）

        异常：
            记录失败时会尝试写入 logging_errors.txt 并打印错误
        """
        try:
            metadata = self._get_caller_metadata()
            logger = logging.getLogger(self.config.name)

            # 根据配置格式化时间
            if self.config.time_format:
                timestamp = datetime.now().strftime(self.config.time_format)
            else:
                timestamp = datetime.now().isoformat()

            # 修复：给所有字段添加"log_"前缀避免冲突
            log_data = {
                "log_timestamp": timestamp,
                "log_level": level.upper(),
                "log_message": message.strip(),
                "log_file": metadata.get("file", "unknown"),
                "log_line": metadata.get("line", 0),
                "log_function": metadata.get("function", "unknown"),
                "log_context": json.dumps(context) if context else ""
            }

            with self._write_lock:
                logger.log(
                    level=getattr(logging, level.upper()),
                    msg=message.strip(),
                    extra=log_data
                )

                self.file_handler.flush()
                if os.name == 'nt':
                    os.fsync(self.file_handler.stream.fileno())

                self._update_stats(level)

        except Exception as e:
            error_msg = f"记录失败: {str(e)}"
            print(error_msg)
            try:
                with open(self._current_log_path.parent / "logging_errors.txt", "pypi", encoding='utf-8-sig') as f:
                    f.write(f"{datetime.now().isoformat()}|{error_msg}\n")
            except:
                pass

    def _safe_rollover(self):
        """Windows安全的日志轮转"""
        try:
            # 关闭当前处理器
            self.close()

            # 执行轮转
            base_path = self._current_log_path
            base_name = base_path.stem

            # 创建备份文件
            for i in range(self.config.backups - 1, 0, -1):
                src = base_path.parent / f"{base_name}.{i}"
                if src.exists():
                    dst = base_path.parent / f"{base_name}.{i + 1}"
                    try:
                        if dst.exists():
                            dst.unlink()
                        src.rename(dst)
                    except Exception as e:
                        warnings.warn(f"重命名备份失败: {str(e)}")

            # 重命名当前日志
            if base_path.exists():
                first_backup = base_path.parent / f"{base_name}.1"
                try:
                    if first_backup.exists():
                        first_backup.unlink()
                    base_path.rename(first_backup)
                except Exception as e:
                    warnings.warn(f"重命名当前日志失败: {str(e)}")

            # 重新初始化处理器
            self._setup_handlers()

        except Exception as e:
            print(f"安全轮转失败: {str(e)}")
            traceback.print_exc()

    def _validate_paths(self):
        """允许临时目录路径"""
        # 识别pytest临时目录和Windows临时目录
        if any(kw in str(self.full_log_dir) for kw in ["pytest-of", "Temp", "tmp"]):
            return
        expected_parent = Path(self.config.base_dir or Path.cwd())
        full_path = self.full_log_dir.resolve()
        if not str(full_path).startswith(str(expected_parent)):
            warnings.warn(f"Log path outside expected directory: {full_path}", RuntimeWarning)

    def _get_caller_frame(self) -> Optional[types.FrameType]:
        skip_paths = [
            "pytest", "_pytest", "unittest", "pluggy",
            "site-packages", "dist-packages",
            "recording/logger.py", "logging/__init__.py", "logger.py"  # 添加logger.py
        ]

        stack = inspect.stack()
        for frame_info in stack:
            frame = frame_info.frame
            filename = frame_info.filename

            # 优先识别测试文件
            if "test_" in filename or "_tests" in filename:
                return frame

            # 跳过不需要的路径
            if any(sp in filename for sp in skip_paths):
                continue

            return frame
        return None

    def _validate_config(self):
        """校验关键配置项"""
        if not isinstance(self.config.max_size, int) or self.config.max_size <= 0:
            raise ValueError("max_size必须为正整数")
        if not isinstance(self.config.backups, int) or self.config.backups < 0:
            raise ValueError("backups必须为自然数")

    @property
    def _current_log_path(self) -> Path:
        """获取当前日志文件路径"""
        if self.config.enable_daily:
            date_dir = datetime.now().strftime(self.config.date_dir_format)
            path = self.full_log_dir / date_dir
            if not path.exists() and self.config.auto_create_dir:
                path.mkdir(parents=True, exist_ok=True)
            return path / f"{datetime.now():%Y%m%d}.log"
        return self.full_log_dir / "app.log"

    def close(self):
        """安全关闭所有资源"""
        with self._lock:
            if self.file_handler:
                try:
                    # 确保文件处理器完全关闭
                    self.file_handler.flush()
                    self.file_handler.close()

                    # 从logging系统中移除
                    logging.getLogger(self.config.name).removeHandler(self.file_handler)

                    # Windows特有关闭处理
                    if os.name == 'nt' and hasattr(self.file_handler.stream, 'fileno'):
                        try:
                            os.close(self.file_handler.stream.fileno())
                        except:
                            pass

                except Exception as e:
                    print(f"关闭日志处理器失败: {str(e)}")
                finally:
                    self.file_handler = None

    def _resolve_paths(self):
        """动态解析日志路径（增强Windows兼容性）"""
        if self.config.base_dir:
            base_path = Path(self.config.base_dir).resolve()
        elif self.config.use_caller_path:
            try:
                frame = inspect.stack()[2]  # 调整栈帧层级
                caller_path = Path(frame.filename).parent.resolve()
                base_path = caller_path
            except:
                base_path = Path.cwd().resolve()
        else:
            base_path = Path(__file__).parent.parent.resolve()  # 项目根目录

        # 处理Windows路径格式
        log_dir = Path(self.config.log_dir)
        if not log_dir.is_absolute():
            log_dir = base_path / log_dir

        # Windows路径格式化
        if os.name == 'nt':
            log_dir = Path(str(log_dir).replace('/', '\\'))

        # 确保路径存在
        self.full_log_dir = log_dir
        if not self.full_log_dir.exists() and self.config.auto_create_dir:
            self.full_log_dir.mkdir(parents=True, exist_ok=True)

    # def _get_caller_metadata(self) -> dict:
    #     """获取调用者元数据（增强栈帧分析）"""
    #     frame = self._get_caller_frame()
    #     if not frame:
    #         return {"file": "unknown", "line": 0, "function": "unknown"}
    #
    #     try:
    #         # 获取栈帧信息
    #         frame_info = inspect.getframeinfo(frame)
    #
    #         # 提取文件名（不含路径）
    #         filename = Path(frame_info.filename).name
    #
    #         # 特殊处理测试文件
    #         if "test_" in filename or "_tests" in filename:
    #             return {
    #                 "file": filename,
    #                 "line": frame_info.lineno,
    #                 "function": frame_info.function
    #             }
    #
    #         return {
    #             "file": filename,
    #             "line": frame_info.lineno,
    #             "function": frame_info.function
    #         }
    #     except Exception:
    #         return {"file": "unknown", "line": 0, "function": "unknown"}

    def _setup_handlers(self):
        """确保日志目录存在并设置处理器"""
        if not self.full_log_dir.exists():
            self.full_log_dir.mkdir(parents=True, exist_ok=True)

        self.file_handler = RotatingFileHandler(
            filename=str(self._current_log_path),
            encoding=self.config.encoding,
            maxBytes=self.config.max_size,
            backupCount=self.config.backups
        )

        # 修复：只传入fmt参数
        formatter = JSONContextFormatter(
            fmt=self.config.log_format,
            style='{',
            datefmt=self.config.time_format  # 传递时间格式
        )

        self.file_handler.setFormatter(formatter)
        logger = logging.getLogger(self.config.name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.file_handler)

    def _update_stats(self, level: str):
        """更新统计信息"""
        self.stats['total'] += 1
        self.stats[level.lower()] += 1

    def _write_record(self, record: Dict):
        """确保字段正确传递"""
        logger = logging.getLogger(self.config.name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            logger.addHandler(self.file_handler)

        # 获取调用者信息（精确到测试代码位置）
        try:
            frame = self._get_caller_frame()
            pathname = frame.f_code.co_filename if frame else 'unknown'
            lineno = frame.f_lineno if frame else 0
        except AttributeError as e:
            pathname = 'unknown'
            lineno = 0
            warnings.warn(f"获取调用栈失败: {str(e)}")

        logger.log(
            level=logging.getLevelName(record['level']),
            msg=record['message'],
            extra={
                '_context': record.get('context', {}),
                '_caller_path': pathname,
                '_caller_line': lineno
            },
            stacklevel=4  # 调整跳过层级
        )

    def _get_log_format(self) -> str:
        """生成多语言日志格式字符串"""
        translations = {
            'time': {'zh': '时间', 'en': 'Time'},
            'level': {'zh': '级别', 'en': 'Level'},
            'error': {'zh': '错误', 'en': 'Error'},
            'location': {'zh': '位置', 'en': 'Location'},
            'message': {'zh': '信息', 'en': 'Message'}
        }
        return self.config.log_format.format(
            **{k: v[self.config.language] for k, v in translations.items()}
        )

    def _get_localized_format(self) -> str:
        """多语言格式处理"""
        translations = {
            "timestamp": {"zh": "时间", "en": "Time"},
            "level": {"zh": "级别", "en": "Level"},
            "error_type": {"zh": "错误类型", "en": "ErrorType"},
            "location": {"zh": "位置", "en": "Location"},
            "message": {"zh": "信息", "en": "Message"}
        }

        localized_format = self.config.log_format
        for field, trans in translations.items():
            localized_format = localized_format.replace(
                f"{{{field}}}",
                trans[self.config.language]
            )
        return localized_format

    def _get_stack_trace(self, error) -> str:
        """获取完整的堆栈跟踪"""
        try:
            return "".join(traceback.format_exception(
                type(error), error, error.__traceback__
            ))
        except:
            return traceback.format_exc()

    def _get_caller_metadata(self) -> dict:
        """获取调用者元数据（增强栈帧分析）"""
        frame = self._get_caller_frame()
        if not frame:
            return {"file": "unknown", "line": 0, "function": "unknown"}

        try:
            frame_info = inspect.getframeinfo(frame)
            return {
                "file": Path(frame_info.filename).name,
                "line": frame_info.lineno,
                "function": frame_info.function,
                "full_path": frame_info.filename
            }
        except:
            return {"file": "unknown", "line": 0, "function": "unknown"}

    def record_error(self, error: BaseCustomError, extra_context: Optional[Dict] = None):
        """
        记录自定义错误

        :param error: 自定义错误对象
        :param extra_context: 额外的上下文信息
        """
        try:
            # 合并上下文
            full_context = {**error.context}
            if extra_context:
                full_context.update(extra_context)

            # 获取调用者元数据
            caller_meta = self._get_caller_metadata()

            # 构建错误记录
            error_record = error.to_dict()
            error_record.update({
                "caller": caller_meta,
                "full_context": full_context
            })

            # 记录错误
            self.record(
                level='ERROR',
                message=f"{error.error_type}: {str(error)}",
                context=error_record
            )

        except Exception as e:
            # 错误记录失败时的后备处理
            fallback_msg = (
                f"记录错误失败: {str(e)} | "
                f"原始错误: {error.error_type} - {str(error)}"
            )
            print(fallback_msg)
            try:
                with open(self._current_log_path.parent / "logging_errors.txt", "pypi") as f:
                    f.write(f"{datetime.now().isoformat()}|{fallback_msg}\n")
            except:
                pass

    def _get_code_location(self, frame) -> str:
        """确保始终返回有效位置信息"""
        try:
            if not frame:
                return "unknown;0"
            return f"{frame.f_code.co_filename};{frame.f_lineno}"
        except Exception:
            return "unknown;0"

    def get_statistics(self) -> Dict:
        """获取统计摘要"""
        return {
            'total': self.stats['total'],
            'levels': dict(self.stats),
            'daily': self._get_daily_stats()
        }

    def _get_daily_stats(self) -> Dict:
        """按日统计日志数量"""
        daily_stats = defaultdict(int)
        with open(self._current_log_path, 'r') as f:
            for line in f:
                date = line.split('[')[1].split(']')[0][:10]
                daily_stats[date] += 1
        return dict(daily_stats)

    def _build_error_record(
            self,
            error: BaseCustomError,
            frame: Optional[types.FrameType] = None,
            context: Optional[Dict] = None
    ) -> dict:
        """构建错误记录结构"""
        base_record = self._build_log_record('ERROR', str(error))
        location_info = self._get_location_info(frame) if frame else {}

        return {
            **base_record,
            'error_type': error.__class__.__name__,
            'stack_trace': self._get_stack_trace(error),
            'object_info': {
                'type': identify_type(error),
                'location': locate(error)
            },
            'context': context or {},
            'caller_location': location_info
        }

    def _get_location_info(self, frame: types.FrameType) -> dict:
        """从栈帧获取位置信息"""
        try:
            return {
                'file': Path(frame.f_code.co_filename).name,
                'line': frame.f_lineno,
                'function': frame.f_code.co_name
            }
        except Exception:
            return {'file': 'unknown', 'line': 0, 'function': 'unknown'}

    def _build_log_record(self, level: str, message: str, context: dict = None) -> dict:
        """构建日志记录结构"""
        return {
            'timestamp': datetime.now().isoformat(),
            'level': level.upper(),
            'message': message,
            'context': context or {}
        }


class LoggerManager:
    _instances: ClassVar[dict] = {}
    _default_name: ClassVar[Optional[str]] = None
    _lock: ClassVar[threading.RLock] = threading.RLock()
    _loggers: ClassVar[Dict[str, Logger]] = {}

    @classmethod
    def _create_logger(cls, name: str, config: LogConfig) -> Logger:
        """实际创建 Logger 实例的内部方法"""
        with cls._lock:
            if name in cls._instances:
                raise ValueError(f"Logger '{name}' 已存在")

            # 创建前验证路径
            if config.auto_create_dir:
                Path(config.log_dir).mkdir(parents=True, exist_ok=True)

            logger = Logger(config)
            cls._instances[name] = logger

            # 设置第一个实例为默认
            if not cls._default_name:
                cls._default_name = name

            return logger

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> "Logger":
        """修正后的获取方法"""
        with cls._lock:  # ✅ 添加线程锁
            if name is None:
                if cls._default_name is None:
                    raise ValueError("无默认日志实例")
                return cls._instances[cls._default_name]

            if name not in cls._instances:
                raise KeyError(f"日志实例 '{name}' 不存在")
            return cls._instances[name]

    @classmethod
    def remove_logger(cls, name: str):
        with cls._lock:
            if name in cls._instances:
                logger = cls._instances[name]
                try:
                    # 确保文件处理器完全关闭
                    if logger.file_handler:
                        logger.file_handler.close()
                        # 从logging系统中移除
                        log = logging.getLogger(name)
                        log.removeHandler(logger.file_handler)
                except Exception as e:
                    print(f"关闭日志处理器失败: {str(e)}")
                finally:
                    del cls._instances[name]

    @classmethod
    def clear_all_loggers(cls):
        with cls._lock:
            for name in list(cls._instances.keys()):
                cls.remove_logger(name)
            cls._default_name = None

    @classmethod
    def create_logger(cls, name: str, config: LogConfig) -> "Logger":
        try:
            if config.use_caller_path and not config.base_dir:
                stack = inspect.stack()
                skip_keywords = [
                    *config.skip_frames,
                    "site-packages",
                    "dist-packages",
                    "venv",
                    "pytest",
                    "_pytest",
                    "test_",
                    "test\\",
                    "test/",
                    "_tests",  # 新增：跳过测试目录
                    "unittest",
                    "__init__.py",
                    "<frozen"  # 跳过Python内部模块
                ]

                # 调整调用栈起始层级为更深的调用
                for frame_info in inspect.stack()[3:]:  # 从更早的栈帧开始分析
                    frame = frame_info.frame
                    filename = str(frame.f_code.co_filename).lower()

                    # 跳过Python内部模块和无效路径
                    if filename.startswith('<') or not filename:
                        continue

                    # 增强路径过滤条件
                    if any(keyword in filename for keyword in skip_keywords):
                        continue

                    # 获取有效调用者路径
                    try:
                        caller_path = Path(frame.f_code.co_filename).resolve().parent
                        config.base_dir = str(caller_path)
                        break
                    except Exception as e:
                        # 特殊处理无效路径
                        if "WinError 123" in str(e) or "syntax is incorrect" in str(e):
                            # 跳过无效路径，继续下一个栈帧
                            continue
                        warnings.warn(f"路径解析失败: {str(e)}", RuntimeWarning)

            # 路径优先级: base_dir > 默认模块路径
            base_path = Path(config.base_dir) if config.base_dir else Path(__file__).parent.parent.parent  # ✅ 调整到项目根目录

            # Windows路径格式化
            if os.name == 'nt':
                config.log_dir = os.path.normpath(config.log_dir).replace("/", "\\")
            else:
                config.log_dir = os.path.normpath(config.log_dir)

            # 构建完整日志路径
            full_log_dir = base_path / config.log_dir
            if not full_log_dir.exists() and config.auto_create_dir:
                full_log_dir.mkdir(parents=True, exist_ok=True)
            config.log_dir = str(full_log_dir)

            if not Path(config.log_dir).is_absolute():
                warnings.warn(f"日志路径应为绝对路径: {config.log_dir}", RuntimeWarning)

            # ================== 实例创建 ==================
            with cls._lock:
                if name in cls._instances:
                    raise ValueError(f"Logger '{name}' 已存在")

                logger = Logger(config)
                cls._instances[name] = logger

                # 设置第一个实例为默认
                if not cls._default_name:
                    cls._default_name = name

                return logger

        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"创建日志实例失败: {str(e)}") from e

    @classmethod
    def get_default_logger(cls) -> "Logger":
        if cls._default_name is None:
            raise ValueError("无默认日志实例")
        return cls._instances[cls._default_name]

    @classmethod
    def set_default(cls, name: str):
        with cls._lock:
            if name not in cls._instances:
                raise KeyError(f"无法设置默认实例: '{name}' 不存在")
            cls._default_name = name


def record_error(error: Exception, context: Optional[dict] = None):
    """安全记录错误到日志系统"""
    try:
        logger = LoggerManager.get_logger()
        if isinstance(error, BaseCustomError):
            # 对于自定义错误，使用专用记录方法
            logger.record_error(error, context)
        else:
            # 对于普通异常，记录为ERROR级别
            logger.record('ERROR', str(error), context)
    except Exception as log_err:
        warnings.warn(f"错误记录失败: {str(log_err)}", RuntimeWarning)

def safe_type_check(obj, expected_type, **kwargs) -> bool:
    """安全类型检查，返回布尔值"""
    try:
        check_type(obj, expected_type, **kwargs)
        return True
    except eTypeError as e:
        record_error(e)
        return False
    except Exception as e:
        record_error(e)
        return False
