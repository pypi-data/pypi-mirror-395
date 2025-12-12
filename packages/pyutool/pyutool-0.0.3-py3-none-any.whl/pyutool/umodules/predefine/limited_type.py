# -*- coding: utf-8 -*-
"""
增强版路径处理和有限类型模块
包含路径风格枚举、自定义异常、字符串校验工具及增强版路径封装类
以及时间、日期、编码和语言相关类型封装
"""

import re
import os
import string
import random
import time
import datetime
import locale
from enum import Enum
from typing import Optional, List, Union, Tuple
from pathlib import Path, PurePosixPath, PureWindowsPath
from zoneinfo import ZoneInfo

try:
    from pyutool.recording import validate_parameters
except ImportError:
    def validate_parameters(*args, **kwargs):
        def wrapper(func):
            return func

        return wrapper

try:
    import chardet
except ImportError:
    chardet = None


class PathStyle(Enum):
    """路径风格枚举"""
    AUTO = "auto"  # 自动适配系统
    POSIX = "posix"  # POSIX风格（Linux/macOS）
    WINDOWS = "windows"  # Windows风格


class TimeSeparator(Enum):
    """时间分隔符枚举"""
    COLON = ':'  # 冒号分隔（例：14:30:25）
    DOT = '.'  # 点号分隔（例：14.30.25）
    HYPHEN = '-'  # 连字符分隔（例：14-30-25）
    SPACE = ' '  # 空格分隔（例：14 30 25）


class DateSeparator(Enum):
    """日期分隔符枚举"""
    DOT = '.'  # 点号分隔（例：2025.10.05）
    SLASH = '/'  # 斜杠分隔（例：2025/10/05）
    HYPHEN = '-'  # 连字符分隔（例：2025-10-05）
    COLON = ':'  # 冒号分隔（例：2025:10:05）
    SPACE = ' '  # 空格分隔（例：2025 10 05）


class DatetimeSeparator(Enum):
    """日期时间组合分隔符枚举"""
    SPACE = ' '  # 空格分隔（例：2025-10-05 14:30:25）
    T = 'T'  # T分隔（例：2025-10-05T14:30:25，符合ISO 8601）
    AT = '@'  # @分隔（例：2025-10-05@14:30:25）


class EncodingStyle(Enum):
    """编码风格枚举"""
    UTF8 = 'utf-8'
    GBK = 'gbk'
    GB2312 = 'gb2312'
    UTF16 = 'utf-16'
    UTF32 = 'utf-32'
    ISO88591 = 'iso-8859-1'
    ASCII = 'ascii'


class LanguageStyle(Enum):
    """语言风格枚举（基于ISO 639-1语言代码）"""
    CHINESE = 'zh'
    ENGLISH = 'en'
    JAPANESE = 'ja'
    KOREAN = 'ko'
    FRENCH = 'fr'
    GERMAN = 'de'
    SPANISH = 'es'
    RUSSIAN = 'ru'


class PathInvalidError(ValueError):
    """路径格式非法异常"""

    def __init__(self, path: str, style: PathStyle):
        super().__init__(f"路径格式非法（{style.value}风格）：{path}")


class PathNotExistsError(FileNotFoundError):
    """路径不存在异常"""

    def __init__(self, path: str):
        super().__init__(f"路径不存在：{path}")


class InvalidTimeError(ValueError):
    """时间格式非法异常"""

    def __init__(self, time_str: str, msg: str = ""):
        super().__init__(f"无效的时间格式: {time_str}" + (f" ({msg})" if msg else ""))


class InvalidDateError(ValueError):
    """日期格式非法异常"""

    def __init__(self, date_str: str, msg: str = ""):
        super().__init__(f"无效的日期格式: {date_str}" + (f" ({msg})" if msg else ""))


class InvalidDatetimeError(ValueError):
    """日期时间格式非法异常"""

    def __init__(self, datetime_str: str, msg: str = ""):
        super().__init__(f"无效的日期时间格式: {datetime_str}" + (f" ({msg})" if msg else ""))


class InvalidEncodingError(ValueError):
    """无效编码异常"""

    def __init__(self, encoding: str):
        super().__init__(f"无效的编码格式: {encoding}")


class InvalidLanguageError(ValueError):
    """无效语言异常"""

    def __init__(self, language: str):
        super().__init__(f"无效的语言代码: {language}")


class StringChecker:
    """字符串校验工具类"""

    @staticmethod
    def is_valid_path(path: str, style: PathStyle = PathStyle.AUTO) -> bool:
        """验证路径格式合法性"""
        if not isinstance(path, str) or not path.strip() or '\0' in path:
            return False

        # 确定验证风格
        target_style = (PathStyle.WINDOWS if os.name == 'nt' else PathStyle.POSIX
                        ) if style == PathStyle.AUTO else style

        return (StringChecker._is_valid_windows_path(path)
                if target_style == PathStyle.WINDOWS
                else StringChecker._is_valid_posix_path(path))

    @staticmethod
    def _is_valid_windows_path(path: str) -> bool:
        """Windows路径验证"""
        # 分离驱动器号
        drive_part = path[:2] if len(path) >= 2 and path[1] == ':' and path[0].isalpha() else ''
        path_body = path[2:] if drive_part else path

        # 非法字符检查
        illegal_chars = {'<', '>', ':', '"', '|', '?', '*'}
        if any(c in illegal_chars for c in path_body):
            return False

        # 控制字符检查
        if any(ord(c) < 32 for c in path_body):
            return False

        # 路径组件检查
        parts = [p for p in re.split(r'[\\/]', path_body) if p]
        for part in parts:
            if part in ('.', '..'):
                continue
            if len(part) > 255 or part.startswith(' ') or part.endswith(' '):
                return False
            # 保留设备名检查
            if re.match(r'(?i)^(CON|PRN|AUX|NUL)(\..*)?$', part):
                return False
            if re.match(r'(?i)^(COM|LPT)([1-9])(\..*)?$', part):
                return False

        return True

    @staticmethod
    def _is_valid_posix_path(path: str) -> bool:
        """POSIX路径验证"""
        if any(ord(c) < 32 for c in path):
            return False

        parts = [p for p in path.split('/') if p]
        for part in parts:
            if part in ('.', '..'):
                continue
            if (len(part) > 255 or part.startswith(' ') or
                    part.endswith(' ') or part.startswith('-')):
                return False

        return True

    @staticmethod
    def get_random_path(
            style: PathStyle = PathStyle.AUTO,
            is_absolute: bool = True,
            depth: int = 2,
            dir_count: int = 1,
            file_name: Optional[str] = None,
            extensions: Optional[List[str]] = None,
            min_component_len: int = 3,
            max_component_len: int = 8
    ) -> str:
        """生成随机合法路径"""
        target_style = (PathStyle.WINDOWS if os.name == 'nt' else PathStyle.POSIX
                        ) if style == PathStyle.AUTO else style
        sep = "\\" if target_style == PathStyle.WINDOWS else "/"
        valid_chars = string.ascii_letters + string.digits + "_-"
        roots = [f"{chr(ord('C') + i)}:" for i in range(6)] if target_style == PathStyle.WINDOWS else ["/"]

        def _random_component() -> str:
            while True:
                length = random.randint(min_component_len, max_component_len)
                component = ''.join(random.choice(valid_chars) for _ in range(length))
                if target_style == PathStyle.WINDOWS:
                    if (not re.match(r'(?i)^(CON|PRN|AUX|NUL)(\..*)?$', component) and
                            not re.match(r'(?i)^(COM|LPT)([1-9])(\..*)?$', component) and
                            not component.startswith(' ') and not component.endswith(' ')):
                        break
                else:
                    if not (component.startswith((' ', '-')) or component.endswith(' ')):
                        break
            return component

        # 生成目录部分
        dir_components = []
        for _ in range(depth):
            dir_components.extend([_random_component() for _ in range(dir_count)])
        dir_part = sep.join(dir_components)

        # 生成文件名部分
        if file_name:
            file_base = ''.join(c for c in file_name if c in valid_chars) or _random_component()
        else:
            file_base = _random_component()

        extensions = extensions or [".txt", ".csv", ".json", ".log", ".bin", ".dat"]
        file_part = f"{file_base}{random.choice(extensions)}"

        # 组合完整路径
        if is_absolute:
            root = random.choice(roots)
            full_path = f"{root}{sep}{dir_part}{sep}{file_part}" if target_style == PathStyle.WINDOWS else f"{root}{dir_part}{sep}{file_part}"
        else:
            full_path = f"{dir_part}{sep}{file_part}"

        return full_path if StringChecker.is_valid_path(full_path, target_style) else StringChecker.get_random_path(
            style=target_style, is_absolute=is_absolute, depth=depth, dir_count=dir_count,
            file_name=file_name, extensions=extensions, min_component_len=min_component_len,
            max_component_len=max_component_len
        )

    # 其他字符串校验方法
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return isinstance(phone, str) and re.fullmatch(r"^1[3-9]\d{9}$", phone) is not None

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return isinstance(email, str) and re.fullmatch(r"^[pypi-zA-Z0-9._%+-]+@[pypi-zA-Z0-9.-]+\.[pypi-zA-Z]{1,}$",
                                                       email) is not None

    @staticmethod
    def is_valid_date(date_str: str, separators: List[DateSeparator] = None) -> bool:
        if not isinstance(date_str, str) or not date_str.strip():
            return False
        if any(c in date_str for c in ['年', '月', '日']):
            return StringChecker._validate_chinese_date(date_str)

        default_seps = {sep.value for sep in
                        [DateSeparator.DOT, DateSeparator.SLASH, DateSeparator.HYPHEN, DateSeparator.SPACE]}
        allowed_seps = {sep.value for sep in separators} if separators else default_seps
        sep = None
        for c in date_str:
            if c in allowed_seps:
                if sep is None:
                    sep = c
                elif c != sep:
                    return False
        if sep is None:
            return False

        parts = date_str.split(sep)
        if len(parts) != 3:
            return False
        try:
            year, month, day = map(int, parts)
        except ValueError:
            return False
        return 1 <= month <= 12 and 1 <= day <= StringChecker._get_days_in_month(year, month)

    @staticmethod
    @validate_parameters(True)
    def _validate_chinese_date(chinese_date: str) -> bool:
        pattern = r'^\d{4}年(0?[1-9]|1[0-2])月(0?[1-9]|[12]\d|3[01])日$'
        if not re.fullmatch(pattern, chinese_date):
            return False
        year = int(chinese_date[:4])
        month = int(re.search(r'年(\d+)月', chinese_date).group(1))
        day = int(re.search(r'月(\d+)日', chinese_date).group(1))
        return 1 <= day <= StringChecker._get_days_in_month(year, month)

    @staticmethod
    @validate_parameters()
    def _get_days_in_month(year: int, month: int) -> int:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28

    @staticmethod
    def is_valid_time(time_str: str, separators: List[TimeSeparator] = None) -> bool:
        if not isinstance(time_str, str) or not time_str.strip():
            return False

        default_seps = {sep.value for sep in [TimeSeparator.COLON, TimeSeparator.DOT, TimeSeparator.HYPHEN]}
        allowed_seps = {sep.value for sep in separators} if separators else default_seps
        sep = None
        for c in time_str:
            if c in allowed_seps:
                if sep is None:
                    sep = c
                elif c != sep:
                    return False
        if sep is None:
            return False

        parts = time_str.split(sep)
        if len(parts) not in (2, 3):
            return False
        try:
            hour, minute = int(parts[0]), int(parts[1])
            second = int(parts[2]) if len(parts) == 3 else 0
        except ValueError:
            return False
        return 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59

    @staticmethod
    def is_digit(text: str) -> bool:
        return text.isdigit()

    @staticmethod
    def is_alpha(text: str) -> bool:
        return text.isalpha()

    @staticmethod
    def is_alnum(text: str) -> bool:
        return text.isalnum()

    @staticmethod
    def is_symbol(text: str) -> bool:
        if not text:
            return False
        for char in text:
            if char in string.ascii_letters or char in string.digits or char.isspace():
                return False
        return True

    @staticmethod
    def is_space(text: str) -> bool:
        return text.isspace()

    @staticmethod
    def uniform_case(text: str, case_mode: str = 'lower') -> str:
        if not isinstance(text, str):
            raise TypeError("输入必须是字符串")
        return text.lower() if case_mode == 'lower' else text.upper() if case_mode == 'upper' else ValueError(
            "case_mode必须是'lower'或'upper'")


@validate_parameters()
class LimitedPath:
    """增强版路径封装类"""

    def __init__(self, path_str: str, style: PathStyle = PathStyle.AUTO,
                 check_exists: bool = False, create_if_missing: bool = False):
        self._style = style
        self._check_exists = check_exists
        self._path_str = path_str.strip()

        # 路径格式验证
        self._validate_path_format()

        # 初始化路径对象
        if style == PathStyle.POSIX:
            self._path_obj = PurePosixPath(self._path_str)
        elif style == PathStyle.WINDOWS:
            self._path_obj = PureWindowsPath(self._path_str)
        else:
            self._path_obj = Path(self._path_str)

        # 存在性验证
        self._validate_path_exists()

        # 自动创建目录
        if create_if_missing and not self.exists() and self._is_likely_directory():
            self._path_obj.mkdir(parents=True, exist_ok=True)

    def _validate_path_format(self) -> None:
        """验证路径格式"""
        if not StringChecker.is_valid_path(self._path_str, self._style):
            raise PathInvalidError(self._path_str, self._style)

    def _validate_path_exists(self) -> None:
        """验证路径存在性"""
        if self._check_exists and not self.exists():
            raise PathNotExistsError(str(self._path_obj))

    def _is_likely_directory(self) -> bool:
        """判断是否为目录路径"""
        path_str = str(self._path_obj)
        return path_str.endswith(('/', '\\')) or '.' not in self._path_obj.name

    def exists(self) -> bool:
        """检查路径是否存在"""
        return isinstance(self._path_obj, Path) and self._path_obj.exists()

    def __str__(self) -> str:
        return str(self._path_obj)

    @property
    def depth(self) -> int:
        """路径深度"""
        return len(self._path_obj.parts)

    @property
    def extension(self) -> str:
        """文件扩展名"""
        return self._path_obj.suffix

    @property
    def stem(self) -> str:
        """文件名（不含扩展名）"""
        return self._path_obj.stem

    def join(self, *parts: str) -> 'LimitedPath':
        """拼接路径"""
        new_path = self._path_obj.joinpath(*parts)
        return LimitedPath(
            str(new_path),
            style=self._style,
            check_exists=self._check_exists
        )

    def relative_to(self, other: 'LimitedPath') -> str:
        """计算相对路径"""
        return str(self._path_obj.relative_to(other._path_obj))

    @property
    def type(self) -> str:
        return "Path"

    @property
    def absolute_path(self) -> str:
        """绝对路径"""
        return str(self._path_obj.absolute()) if isinstance(self._path_obj, Path) else str(self._path_obj)

    @property
    def parent(self) -> 'LimitedPath':
        """父目录路径对象"""
        return LimitedPath(
            str(self._path_obj.parent),
            style=self._style,
            check_exists=self._check_exists
        )


@validate_parameters()
class LimitedTime:
    """时间封装类（时分秒）"""

    def __init__(self, time_str: Optional[str] = None,
                 separator: Union[TimeSeparator, str] = TimeSeparator.COLON,
                 hours: int = 0, minutes: int = 0, seconds: int = 0):
        """
        初始化时间对象

        :param time_str: 时间字符串，如 "12:44:00"
        :param separator: 时间分隔符，可以是枚举或自定义字符（会验证有效性）
        :param hours: 小时（如果不提供time_str则使用）
        :param minutes: 分钟（如果不提供time_str则使用）
        :param seconds: 秒（如果不提供time_str则使用）
        """
        self._separator = self._validate_separator(separator)

        if time_str:
            self._parse_time_str(time_str)
        else:
            self._validate_time_components(hours, minutes, seconds)
            self._hours = hours
            self._minutes = minutes
            self._seconds = seconds

    def _validate_separator(self, separator: Union[TimeSeparator, str]) -> str:
        """验证分隔符有效性"""
        if isinstance(separator, TimeSeparator):
            return separator.value
        if isinstance(separator, str) and len(separator) == 1 and re.match(r'^[\:\.\-\s]$', separator):
            return separator
        raise ValueError(f"不支持的时间分隔符: {separator}")

    def _parse_time_str(self, time_str: str) -> None:
        """解析时间字符串"""
        parts = time_str.split(self._separator)

        if len(parts) not in (2, 3):
            raise InvalidTimeError(time_str, f"应包含{2}或{3}个部分，实际包含{len(parts)}个")

        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2]) if len(parts) == 3 else 0
        except ValueError:
            raise InvalidTimeError(time_str, "时间部分必须为整数")

        self._validate_time_components(hours, minutes, seconds)
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

    def _validate_time_components(self, hours: int, minutes: int, seconds: int) -> None:
        """验证时间组件有效性"""
        if not (0 <= hours < 24):
            raise InvalidTimeError(f"{hours}:{minutes}:{seconds}", "小时必须在0-23之间")
        if not (0 <= minutes < 60):
            raise InvalidTimeError(f"{hours}:{minutes}:{seconds}", "分钟必须在0-59之间")
        if not (0 <= seconds < 60):
            raise InvalidTimeError(f"{hours}:{minutes}:{seconds}", "秒必须在0-59之间")

    @property
    def hours(self) -> int:
        """小时"""
        return self._hours

    @property
    def minutes(self) -> int:
        """分钟"""
        return self._minutes

    @property
    def seconds(self) -> int:
        """秒"""
        return self._seconds

    @property
    def total_seconds(self) -> int:
        """转换为总秒数"""
        return self._hours * 3600 + self._minutes * 60 + self._seconds

    def to_string(self, separator: Optional[Union[TimeSeparator, str]] = None) -> str:
        """转换为字符串表示"""
        sep = self._validate_separator(separator) if separator else self._separator
        return f"{self._hours:02d}{sep}{self._minutes:02d}{sep}{self._seconds:02d}"

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f"LimitedTime(hours={self._hours}, minutes={self._minutes}, seconds={self._seconds})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, LimitedTime):
            return False
        return (self._hours == other._hours and
                self._minutes == other._minutes and
                self._seconds == other._seconds)


@validate_parameters()
class LimitedDate:
    """日期封装类（年月日）"""

    def __init__(self, date_str: Optional[str] = None,
                 separator: Union[DateSeparator, str] = DateSeparator.HYPHEN,
                 year: int = 2000, month: int = 1, day: int = 1):
        """
        初始化日期对象

        :param date_str: 日期字符串，如 "2025-1-1"
        :param separator: 日期分隔符，可以是枚举或自定义字符（会验证有效性）
        :param year: 年（如果不提供date_str则使用）
        :param month: 月（如果不提供date_str则使用）
        :param day: 日（如果不提供date_str则使用）
        """
        self._separator = self._validate_separator(separator)

        if date_str:
            self._parse_date_str(date_str)
        else:
            self._validate_date_components(year, month, day)
            self._year = year
            self._month = month
            self._day = day

    def _validate_separator(self, separator: Union[DateSeparator, str]) -> str:
        """验证分隔符有效性"""
        if isinstance(separator, DateSeparator):
            return separator.value
        if isinstance(separator, str) and len(separator) == 1 and re.match(r'^[\.\/\-\:\s]$', separator):
            return separator
        raise ValueError(f"不支持的日期分隔符: {separator}")

    def _parse_date_str(self, date_str: str) -> None:
        """解析日期字符串"""
        parts = date_str.split(self._separator)

        if len(parts) != 3:
            raise InvalidDateError(date_str, f"应包含3个部分，实际包含{len(parts)}个")

        try:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
        except ValueError:
            raise InvalidDateError(date_str, "日期部分必须为整数")

        self._validate_date_components(year, month, day)
        self._year = year
        self._month = month
        self._day = day

    def _validate_date_components(self, year: int, month: int, day: int) -> None:
        """验证日期组件有效性"""
        if year < 1 or year > 9999:
            raise InvalidDateError(f"{year}-{month}-{day}", "年份必须在1-9999之间")
        if month < 1 or month > 12:
            raise InvalidDateError(f"{year}-{month}-{day}", "月份必须在1-12之间")

        # 检查每月的天数
        days_in_month = self._get_days_in_month(year, month)
        if day < 1 or day > days_in_month:
            raise InvalidDateError(f"{year}-{month}-{day}",
                                   f"{month}月在{year}年只有{days_in_month}天")

    @staticmethod
    def _get_days_in_month(year: int, month: int) -> int:
        """获取指定月份的天数"""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:  # 2月
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28

    @property
    def year(self) -> int:
        """年"""
        return self._year

    @property
    def month(self) -> int:
        """月"""
        return self._month

    @property
    def day(self) -> int:
        """日"""
        return self._day

    @property
    def weekday(self) -> int:
        """星期几（0=星期一，6=星期日）"""
        return datetime.date(self._year, self._month, self._day).weekday()

    @property
    def is_leap_year(self) -> bool:
        """是否为闰年"""
        return (self._year % 4 == 0 and self._year % 100 != 0) or (self._year % 400 == 0)

    def to_string(self, separator: Optional[Union[DateSeparator, str]] = None) -> str:
        """转换为字符串表示"""
        sep = self._validate_separator(separator) if separator else self._separator
        return f"{self._year}{sep}{self._month:02d}{sep}{self._day:02d}"

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f"LimitedDate(year={self._year}, month={self._month}, day={self._day})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, LimitedDate):
            return False
        return (self._year == other._year and
                self._month == other._month and
                self._day == other._day)


@validate_parameters()
class LimitedDatetime:
    """日期时间组合类（年月日时分秒）"""

    def __init__(self,
                 datetime_str: Optional[str] = None,
                 date_sep: Union[DateSeparator, str] = DateSeparator.HYPHEN,
                 time_sep: Union[TimeSeparator, str] = TimeSeparator.COLON,
                 datetime_sep: Union[DatetimeSeparator, str] = DatetimeSeparator.SPACE,
                 date: Optional[LimitedDate] = None,
                 time: Optional[LimitedTime] = None,
                 timestamp: Optional[float] = None,
                 timezone: str = "UTC"):
        """
        初始化日期时间对象

        :param datetime_str: 日期时间字符串，如 "2025-1-1 12:44:00"
        :param date_sep: 日期分隔符
        :param time_sep: 时间分隔符
        :param datetime_sep: 日期和时间之间的分隔符
        :param date: LimitedDate对象（如果不提供datetime_str则使用）
        :param time: LimitedTime对象（如果不提供datetime_str则使用）
        :param timestamp: 时间戳（如果提供则优先使用）
        :param timezone: 时区，默认为UTC
        """
        self._timezone = ZoneInfo(timezone)
        self._date_sep = self._validate_date_separator(date_sep)
        self._time_sep = self._validate_time_separator(time_sep)
        self._datetime_sep = self._validate_datetime_separator(datetime_sep)

        if timestamp is not None:
            self._from_timestamp(timestamp)
        elif datetime_str:
            self._parse_datetime_str(datetime_str)
        elif date and time:
            self._date = date
            self._time = time
        else:
            raise ValueError("必须提供datetime_str、(date和time)或timestamp中的一种")

    def _validate_date_separator(self, separator: Union[DateSeparator, str]) -> str:
        """验证日期分隔符"""
        if isinstance(separator, DateSeparator):
            return separator.value
        if isinstance(separator, str) and len(separator) == 1 and re.match(r'^[\.\/\-\:\s]$', separator):
            return separator
        raise ValueError(f"不支持的日期分隔符: {separator}")

    def _validate_time_separator(self, separator: Union[TimeSeparator, str]) -> str:
        """验证时间分隔符"""
        if isinstance(separator, TimeSeparator):
            return separator.value
        if isinstance(separator, str) and len(separator) == 1 and re.match(r'^[\:\.\-\s]$', separator):
            return separator
        raise ValueError(f"不支持的时间分隔符: {separator}")

    def _validate_datetime_separator(self, separator: Union[DatetimeSeparator, str]) -> str:
        """验证日期时间分隔符"""
        if isinstance(separator, DatetimeSeparator):
            return separator.value
        if isinstance(separator, str) and len(separator) >= 1 and re.match(r'^[\sT@]$', separator):
            return separator
        raise ValueError(f"不支持的日期时间分隔符: {separator}")

    def _parse_datetime_str(self, datetime_str: str) -> None:
        """解析日期时间字符串"""
        # 分割日期和时间部分
        parts = datetime_str.split(self._datetime_sep)
        if len(parts) != 2:
            raise InvalidDatetimeError(datetime_str, f"应包含日期和时间两部分，实际包含{len(parts)}个部分")

        date_str, time_str = parts
        self._date = LimitedDate(date_str, separator=self._date_sep)
        self._time = LimitedTime(time_str, separator=self._time_sep)

    def _from_timestamp(self, timestamp: float) -> None:
        """从时间戳初始化"""
        dt = datetime.datetime.fromtimestamp(timestamp, tz=self._timezone)
        self._date = LimitedDate(year=dt.year, month=dt.month, day=dt.day)
        self._time = LimitedTime(hours=dt.hour, minutes=dt.minute, seconds=dt.second)

    @property
    def date(self) -> LimitedDate:
        """日期部分"""
        return self._date

    @property
    def time(self) -> LimitedTime:
        """时间部分"""
        return self._time

    @property
    def year(self) -> int:
        """年"""
        return self._date.year

    @property
    def month(self) -> int:
        """月"""
        return self._date.month

    @property
    def day(self) -> int:
        """日"""
        return self._date.day

    @property
    def hours(self) -> int:
        """小时"""
        return self._time.hours

    @property
    def minutes(self) -> int:
        """分钟"""
        return self._time.minutes

    @property
    def seconds(self) -> int:
        """秒"""
        return self._time.seconds

    @property
    def timestamp(self) -> float:
        """转换为时间戳"""
        dt = datetime.datetime(
            self.year, self.month, self.day,
            self.hours, self.minutes, self.seconds,
            tzinfo=self._timezone
        )
        return dt.timestamp()

    @property
    def timezone(self) -> str:
        """时区"""
        return str(self._timezone)

    def to_string(self,
                  date_sep: Optional[Union[DateSeparator, str]] = None,
                  time_sep: Optional[Union[TimeSeparator, str]] = None,
                  datetime_sep: Optional[Union[DatetimeSeparator, str]] = None) -> str:
        """转换为字符串表示"""
        d_sep = self._validate_date_separator(date_sep) if date_sep else self._date_sep
        t_sep = self._validate_time_separator(time_sep) if time_sep else self._time_sep
        dt_sep = self._validate_datetime_separator(datetime_sep) if datetime_sep else self._datetime_sep

        return f"{self._date.to_string(d_sep)}{dt_sep}{self._time.to_string(t_sep)}"

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return (f"LimitedDatetime(year={self.year}, month={self.month}, day={self.day}, "
                f"hours={self.hours}, minutes={self.minutes}, seconds={self.seconds}, "
                f"timezone={self.timezone})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, LimitedDatetime):
            return False
        return (self._date == other._date and
                self._time == other._time and
                self._timezone == other._timezone)


@validate_parameters()
class LimitedEncoding:
    """编码封装类"""

    def __init__(self, encoding: Union[str, EncodingStyle]):
        """
        初始化编码对象

        :param encoding: 编码名称或EncodingStyle枚举
        """
        if isinstance(encoding, EncodingStyle):
            self._encoding = encoding.value
        else:
            self._encoding = encoding.lower()

        self._validate_encoding()

    def _validate_encoding(self) -> None:
        """验证编码有效性"""
        # 检查是否为支持的编码
        supported_encodings = {e.value for e in EncodingStyle}
        if self._encoding not in supported_encodings:
            raise InvalidEncodingError(self._encoding)

    @property
    def encoding(self) -> str:
        """编码名称"""
        return self._encoding

    @staticmethod
    def detect(data: bytes) -> 'LimitedEncoding':
        """
        检测字节数据的编码

        :param data: 字节数据
        :return: 检测到的编码对应的LimitedEncoding对象
        """
        if chardet is None:
            raise ImportError("chardet库未安装，无法使用编码检测功能")

        result = chardet.detect(data)
        encoding = result['encoding']
        if not encoding:
            raise InvalidEncodingError("无法检测编码")
        return LimitedEncoding(encoding)

    def is_valid_for_data(self, data: bytes) -> bool:
        """
        检查数据是否可以用当前编码解码

        :param data: 字节数据
        :return: 是否可以解码
        """
        try:
            data.decode(self._encoding)
            return True
        except UnicodeDecodeError:
            return False

    def __str__(self) -> str:
        return self._encoding

    def __repr__(self) -> str:
        return f"LimitedEncoding(encoding='{self._encoding}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, LimitedEncoding):
            return False
        return self._encoding == other._encoding


@validate_parameters()
class LimitedLanguage:
    """语言封装类"""

    def __init__(self, language: Union[str, LanguageStyle]):
        """
        初始化语言对象

        :param language: 语言代码或LanguageStyle枚举
        """
        if isinstance(language, LanguageStyle):
            self._language_code = language.value
        else:
            self._language_code = language.lower()

        self._validate_language()

    def _validate_language(self) -> None:
        """验证语言代码有效性"""
        supported_languages = {l.value for l in LanguageStyle}
        if self._language_code not in supported_languages:
            # 检查是否为有效的locale
            try:
                locale.setlocale(locale.LC_ALL, f"{self._language_code}.UTF-8")
            except locale.Error:
                raise InvalidLanguageError(self._language_code)

    @property
    def language_code(self) -> str:
        """语言代码（ISO 639-1）"""
        return self._language_code

    @property
    def language_name(self) -> str:
        """语言名称（本地化）"""
        # 获取语言名称的映射
        lang_names = {
            'zh': '中文',
            'en': 'English',
            'ja': '日本語',
            'ko': '한국어',
            'fr': 'français',
            'de': 'Deutsch',
            'es': 'español',
            'ru': 'русский'
        }
        return lang_names.get(self._language_code, self._language_code)

    def format_date(self, date: LimitedDate) -> str:
        """
        按当前语言格式化日期

        :param date: 日期对象
        :return: 格式化后的日期字符串
        """
        try:
            locale.setlocale(locale.LC_TIME, f"{self._language_code}.UTF-8")
            dt = datetime.date(date.year, date.month, date.day)
            return dt.strftime("%x")
        except (locale.Error, ValueError):
            return str(date)
        finally:
            # 恢复默认locale
            locale.resetlocale()

    def __str__(self) -> str:
        return f"{self.language_name} ({self._language_code})"

    def __repr__(self) -> str:
        return f"LimitedLanguage(language_code='{self._language_code}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, LimitedLanguage):
            return False
        return self._language_code == other._language_code


class LimitedTypeFactory:
    """有限类型工厂类，用于创建各种有限类型对象"""

    @staticmethod
    def create_time(time_str: Optional[str] = None,
                    separator: Union[TimeSeparator, str] = TimeSeparator.COLON,
                    hours: int = 0, minutes: int = 0, seconds: int = 0) -> LimitedTime:
        """创建时间对象"""
        return LimitedTime(
            time_str=time_str,
            separator=separator,
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )

    @staticmethod
    def create_date(date_str: Optional[str] = None,
                    separator: Union[DateSeparator, str] = DateSeparator.HYPHEN,
                    year: int = 2000, month: int = 1, day: int = 1) -> LimitedDate:
        """创建日期对象"""
        return LimitedDate(
            date_str=date_str,
            separator=separator,
            year=year,
            month=month,
            day=day
        )

    @staticmethod
    def create_datetime(datetime_str: Optional[str] = None,
                        date_sep: Union[DateSeparator, str] = DateSeparator.HYPHEN,
                        time_sep: Union[TimeSeparator, str] = TimeSeparator.COLON,
                        datetime_sep: Union[DatetimeSeparator, str] = DatetimeSeparator.SPACE,
                        date: Optional[LimitedDate] = None,
                        time: Optional[LimitedTime] = None,
                        timestamp: Optional[float] = None,
                        timezone: str = "UTC") -> LimitedDatetime:
        """创建日期时间对象"""
        return LimitedDatetime(
            datetime_str=datetime_str,
            date_sep=date_sep,
            time_sep=time_sep,
            datetime_sep=datetime_sep,
            date=date,
            time=time,
            timestamp=timestamp,
            timezone=timezone
        )

    @staticmethod
    def create_encoding(encoding: Union[str, EncodingStyle]) -> LimitedEncoding:
        """创建编码对象"""
        return LimitedEncoding(encoding)

    @staticmethod
    def create_language(language: Union[str, LanguageStyle]) -> LimitedLanguage:
        """创建语言对象"""
        return LimitedLanguage(language)

    @staticmethod
    def create_path(path_str: str,
                    style: PathStyle = PathStyle.AUTO,
                    check_exists: bool = False,
                    create_if_missing: bool = False) -> LimitedPath:
        """创建路径对象"""
        return LimitedPath(
            path_str=path_str,
            style=style,
            check_exists=check_exists,
            create_if_missing=create_if_missing
        )