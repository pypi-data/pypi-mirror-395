# -*- coding: utf-8 -*-
"""
字符串工具类模块（String Utilities）
提供常用的字符串校验、格式转换、随机路径生成等功能，支持多系统路径兼容、多格式日期时间验证等场景。

核心功能：
1. 基础校验：手机号、邮箱、路径格式、日期、时间合法性校验
2. 字符类型判断：纯数字、纯字母、字母数字混合、纯符号、纯空格判断
3. 格式处理：字符串大小写统一转换
4. 随机生成：符合系统规则的随机路径生成（支持 Windows/POSIX 风格）

枚举说明：
- PathStyle：路径风格枚举，控制路径验证/生成的系统规则
- TimeSeparator：日期/时间分隔符枚举，限定合法的分隔符类型
"""

import re
import os
from enum import Enum
import string
import random
from typing import Optional, List, Union

# 导入参数验证装饰器（假设用于输入合法性校验）
from pyutool.recording import validate_parameters


class PathStyle(Enum):
    """
    路径风格枚举（用于指定路径验证/生成的系统规则）
    适配不同操作系统的路径格式规范，确保跨平台兼容性
    """
    AUTO = "auto"      # 自动根据当前系统判断（默认行为）
    POSIX = "posix"    # 强制使用 POSIX 规则（适用于 Linux/macOS/Unix）
    WINDOWS = "windows"# 强制使用 Windows 规则（适用于 Windows 系统）


class TimeSeparator(Enum):
    """
    日期/时间分隔符枚举
    限定日期和时间字符串中允许使用的分隔符类型，避免混合分隔符导致的格式错误
    """
    DOT = '.'       # 点号分隔（例：2025.10.05 / 14.30.25）
    SLASH = '/'     # 斜杠分隔（例：2025/10/05）
    HYPHEN = '-'    # 连字符分隔（例：2025-10-05 / 14-30-25）
    SPACE = ' '     # 空格分隔（例：2025 10 05）
    COLON = ':'     # 冒号分隔（例：14:30:25）


class StringChecker:
    """
    字符串校验与处理工具类
    所有方法均为静态方法，无需实例化即可调用，支持链式组合使用
    核心特性：
    - 输入类型容错：对非字符串输入返回明确结果（不抛出异常，除非特殊说明）
    - 逻辑有效性校验：不仅检查格式，还验证数值合理性（如日期的2月天数、时间的小时范围）
    - 多系统兼容：路径相关方法支持 Windows/POSIX 双风格
    """

    # ------------------------------
    # 手机号验证
    # ------------------------------
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        验证国内手机号格式合法性

        校验规则：
        - 必须是 11 位纯数字字符串
        - 以数字 1 开头
        - 第二位为 3-9（覆盖当前国内所有运营商号段）

        Args:
            phone: 待验证的手机号字符串

        Returns:
            bool: 格式合法返回 True，否则返回 False（非字符串输入直接返回 False）

        Examples:
            >>> StringChecker.is_valid_phone("13800138000")
            True
            >>> StringChecker.is_valid_phone("1234567890")
            False
            >>> StringChecker.is_valid_phone(13800138000)  # 非字符串输入
            False
        """
        if not isinstance(phone, str):
            return False
        pattern = r"^1[3-9]\d{9}$"
        return re.fullmatch(pattern, phone) is not None

    # ------------------------------
    # 邮箱验证
    # ------------------------------
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        验证邮箱格式合法性（宽松匹配，兼容大多数常见邮箱格式）

        校验规则：
        - 本地部分（@前）：允许字母、数字、下划线、百分号、加号、减号、点号
        - 域名部分（@后）：允许字母、数字、点号、减号，支持多级域名
        - 顶级域名（最后一段）：至少 1 个字母（兼容 .co、.io 等短顶级域名）

        Args:
            email: 待验证的邮箱字符串

        Returns:
            bool: 格式合法返回 True，否则返回 False（非字符串输入直接返回 False）

        Examples:
            >>> StringChecker.is_valid_email("test@example.com")
            True
            >>> StringChecker.is_valid_email("user.name+tag@sub.domain.co")
            True
            >>> StringChecker.is_valid_email("invalid-email")
            False
        """
        if not isinstance(email, str):
            return False
        # 宽松匹配正则：允许顶级域名1个或多个字母
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$"
        return re.fullmatch(pattern, email) is not None

    # ------------------------------
    # 路径格式验证（纯格式，不检查存在性）
    # ------------------------------
    @staticmethod
    def is_valid_path(path: str, style: PathStyle = PathStyle.AUTO) -> bool:
        """
        验证路径格式合法性（仅检查语法格式，不涉及文件系统存在性校验）

        核心特性：
        - 自动适配当前系统（默认行为），也可强制指定路径风格
        - 拒绝空字符串、空字节（\0）、控制字符等非法输入
        - 严格遵循对应系统的路径命名规则（如 Windows 保留名、POSIX 连字符限制）

        Args:
            path: 待验证的路径字符串（不能为空或纯空格）
            style: 路径验证风格，默认 AUTO（自动判断系统），可选 POSIX/WINDOWS

        Returns:
            bool: 格式合法返回 True，否则返回 False

        Raises:
            None: 输入非字符串或空字符串时直接返回 False，不抛出异常

        Examples:
            # Windows 风格有效路径（使用原始字符串或双反斜杠）
            >>> StringChecker.is_valid_path(r"C:\\Users\\user\\file.txt", PathStyle.WINDOWS)
            True
            # POSIX 风格有效路径
            >>> StringChecker.is_valid_path("/home/user/docs", PathStyle.POSIX)
            True
            # 含非法字符（?）的 Windows 路径
            >>> StringChecker.is_valid_path(r"C:\\invalid?file.txt", PathStyle.WINDOWS)
            False
        """
        if not isinstance(path, str) or not path.strip():
            return False  # 空字符串或纯空格无效

        # 空字节在所有系统均非法（会导致路径截断）
        if '\0' in path:
            return False

        # 确定验证风格（自动判断时基于当前系统）
        if style == PathStyle.AUTO:
            target_style = PathStyle.WINDOWS if os.name == 'nt' else PathStyle.POSIX
        else:
            target_style = style

        # 执行对应风格的验证
        if target_style == PathStyle.WINDOWS:
            return StringChecker._is_valid_windows_path(path)
        else:
            return StringChecker._is_valid_posix_path(path)

    @staticmethod
    def _is_valid_windows_path(path: str) -> bool:
        """
        Windows 路径格式验证（内部辅助方法，不对外暴露）

        校验规则（基于 Windows 系统路径规范）：
        1. 支持绝对路径（带盘符，如 C:）和相对路径
        2. 允许 / 和 \ 作为路径分隔符，支持连续分隔符（如 // 或 \\）
        3. 禁止使用 < > : " | ? * 等非法字符
        4. 路径组件（目录/文件名）不能：
           - 长度超过 255 字符
           - 以空格开头或结尾（Windows 会自动截断）
           - 为保留名（CON/PRN/AUX/NUL，含扩展名如 CON.txt）
           - 为设备名（COM1-9/LPT1-9，含扩展名如 COM2.txt）
        5. 禁止包含 ASCII 控制字符（ord < 32，如换行、制表符）

        Args:
            path: 已通过外层基础校验的路径字符串

        Returns:
            bool: Windows 路径格式合法返回 True，否则返回 False
        """
        # 拆分驱动器号（如 C:）和路径主体
        drive_part = ''
        if len(path) >= 2 and path[1] == ':' and path[0].isalpha():
            drive_part = path[:2]
            path_body = path[2:]
        else:
            path_body = path  # 相对路径（无驱动器号）

        # Windows 非法字符集（移除 /，因 Windows 支持 / 作为分隔符）
        illegal_chars = {'<', '>', ':', '"', '|', '?', '*'}
        if any(char in illegal_chars for char in path_body):
            return False

        # 控制字符检查（ASCII < 32 的不可见字符）
        if any(ord(char) < 32 for char in path_body):
            return False

        # 拆分路径组件（兼容 / 和 \ 分隔符，过滤连续分隔符产生的空字符串）
        parts = [p for p in re.split(r'[\\/]', path_body) if p]

        # 检查每个路径组件的有效性
        for part in parts:
            # 允许 .（当前目录）和 ..（父目录）
            if part in ('.', '..'):
                continue

            # 组件长度不能超过 255 字符（Windows 单个路径组件最大长度限制）
            if len(part) > 255:
                return False

            # 组件不能以空格开头或结尾（Windows 会自动截断，视为非法格式）
            if part.startswith(' ') or part.endswith(' '):
                return False

            # 检查 Windows 保留名称（不区分大小写，支持带扩展名的情况）
            if re.match(r'(?i)^(CON|PRN|AUX|NUL)(\..*)?$', part):
                return False

            # 检查 Windows 设备名称（COM1-9、LPT1-9，不区分大小写，支持带扩展名）
            if re.match(r'(?i)^(COM|LPT)([1-9])(\..*)?$', part):
                return False

        return True

    @staticmethod
    def _is_valid_posix_path(path: str) -> bool:
        """
        POSIX 路径格式验证（内部辅助方法，不对外暴露），适用于 Linux/macOS/Unix 系统

        校验规则（基于 POSIX 路径规范）：
        1. 支持绝对路径（以 / 开头）和相对路径
        2. 仅允许 / 作为路径分隔符，支持连续分隔符（如 //）
        3. 禁止包含 ASCII 控制字符（ord < 32，如换行、制表符）
        4. 路径组件（目录/文件名）不能：
           - 长度超过 255 字符
           - 以空格开头或结尾（避免意外空格导致的路径错误）
           - 以连字符（-）开头（避免被误认为命令行参数）

        Args:
            path: 已通过外层基础校验的路径字符串

        Returns:
            bool: POSIX 路径格式合法返回 True，否则返回 False
        """
        # 控制字符检查（ASCII < 32 的不可见字符）
        if any(ord(char) < 32 for char in path):
            return False

        # 拆分路径组件（按 / 分隔，过滤连续分隔符产生的空字符串）
        parts = [p for p in path.split('/') if p]

        # 检查每个路径组件的有效性
        for part in parts:
            # 允许 .（当前目录）和 ..（父目录）
            if part in ('.', '..'):
                continue

            # 组件长度不能超过 255 字符（POSIX 单个路径组件最大长度限制）
            if len(part) > 255:
                return False

            # 组件不能以空格开头或结尾（避免路径解析歧义）
            if part.startswith(' ') or part.endswith(' '):
                return False

            # 组件不能以连字符开头（防止被误认为命令参数，如 rm -rf）
            if part.startswith('-'):
                return False

        return True

    # ------------------------------
    # 日期格式验证（支持多分隔符和中文格式）
    # ------------------------------
    @staticmethod
    def is_valid_date(date_str: str, separators: List[TimeSeparator] = None) -> bool:
        """
        验证日期格式合法性（包含逻辑有效性校验，如2月天数、月份范围）

        支持格式：
        - 分隔符格式：年-月-日、年.月.日、年/月/日、年 月 日（支持指定允许的分隔符）
        - 中文格式：年日月（如 2025年10月05日，支持单数月份/日期，如 2025年3月5日）

        核心特性：
        - 自动检测分隔符，拒绝混合分隔符（如 2025-10/05）
        - 校验逻辑有效性：月份 1-12、日期匹配当月天数（考虑闰年）
        - 支持自定义允许的分隔符列表

        Args:
            date_str: 待验证的日期字符串（不能为空或纯空格）
            separators: 允许的分隔符列表（元素为 TimeSeparator 枚举），默认允许 DOT/SLASH/HYPHEN/SPACE

        Returns:
            bool: 格式合法且逻辑有效返回 True，否则返回 False（非字符串输入直接返回 False）

        Examples:
            >>> StringChecker.is_valid_date("2025-10-05")
            True
            >>> StringChecker.is_valid_date("2025年10月05日")
            True
            >>> StringChecker.is_valid_date("2025/02/29")  # 2025非闰年，2月无29日
            False
            >>> StringChecker.is_valid_date("2025.13.01")  # 月份13无效
            False
        """
        if not isinstance(date_str, str) or not date_str.strip():
            return False

        # 优先处理中文日期格式（含 年/月/日 字符）
        if any(c in date_str for c in ['年', '月', '日']):
            return StringChecker._validate_chinese_date(date_str)

        # 定义默认允许的分隔符（DOT/SLASH/HYPHEN/SPACE）
        default_seps = {sep.value for sep in [
            TimeSeparator.DOT, TimeSeparator.SLASH,
            TimeSeparator.HYPHEN, TimeSeparator.SPACE
        ]}
        # 处理用户指定的分隔符（转换为字符集合）
        allowed_seps = {sep.value for sep in separators} if separators else default_seps

        # 提取并验证分隔符（整个日期必须使用同一分隔符）
        sep = None
        for c in date_str:
            if c in allowed_seps:
                if sep is None:
                    sep = c
                elif c != sep:
                    return False  # 混合分隔符无效
        if sep is None:
            return False  # 无有效分隔符

        # 拆分年月日（必须为3个部分）
        parts = date_str.split(sep)
        if len(parts) != 3:
            return False

        # 转换为数字并校验范围
        try:
            year, month, day = map(int, parts)
        except ValueError:
            return False  # 非数字部分无效

        # 校验月份和日期的逻辑有效性
        if not (1 <= month <= 12):
            return False
        return 1 <= day <= StringChecker._get_days_in_month(year, month)

    @staticmethod
    @validate_parameters(True)
    def _validate_chinese_date(chinese_date: str) -> bool:
        """
        验证中文日期格式合法性（内部辅助方法，不对外暴露）

        支持格式：
        - 完整格式：yyyy年mm月dd日（如 2025年10月05日）
        - 简化格式：yyyy年m月d日（如 2025年3月5日）
        包含逻辑有效性校验（日期匹配当月天数）

        Args:
            chinese_date: 待验证的中文日期字符串（已通过外层基础校验）

        Returns:
            bool: 中文日期格式合法且逻辑有效返回 True，否则返回 False
        """
        # 中文日期正则：支持单数/双数月份和日期
        pattern = r'^\d{4}年(0?[1-9]|1[0-2])月(0?[1-9]|[12]\d|3[01])日$'
        if not re.fullmatch(pattern, chinese_date):
            return False

        # 提取年月日并验证逻辑有效性
        year = int(chinese_date[:4])
        month = int(re.search(r'年(\d+)月', chinese_date).group(1))
        day = int(re.search(r'月(\d+)日', chinese_date).group(1))

        return 1 <= day <= StringChecker._get_days_in_month(year, month)

    @staticmethod
    @validate_parameters()
    def _get_days_in_month(year: int, month: int) -> int:
        """
        获取指定年月的天数（内部辅助方法，不对外暴露），支持闰年判断

        规则：
        - 大月（1/3/5/7/8/10/12）：31天
        - 小月（4/6/9/11）：30天
        - 2月：闰年29天，平年28天（闰年规则：能被4整除但不能被100整除，或能被400整除）

        Args:
            year: 年份（整数）
            month: 月份（整数，1-12）

        Returns:
            int: 指定年月的天数

        Raises:
            依赖 @validate_parameters 装饰器处理输入合法性（如非整数、月份超出范围）
        """
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:  # 2月
            return 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28

    # ------------------------------
    # 时间格式验证（支持时分秒）
    # ------------------------------
    @staticmethod
    def is_valid_time(time_str: str, separators: List[TimeSeparator] = None) -> bool:
        """
        验证时间格式合法性（包含逻辑有效性校验，如小时/分钟/秒范围）

        支持格式：
        - 时分格式：hh:mm、hh.mm、hh-mm（2个部分）
        - 时分秒格式：hh:mm:ss、hh.mm.ss、hh-mm-ss（3个部分）
        支持自定义允许的分隔符列表

        核心特性：
        - 自动检测分隔符，拒绝混合分隔符（如 14:30-25）
        - 校验逻辑有效性：小时 0-23、分钟 0-59、秒 0-59

        Args:
            time_str: 待验证的时间字符串（不能为空或纯空格）
            separators: 允许的分隔符列表（元素为 TimeSeparator 枚举），默认允许 COLON/DOT/HYPHEN

        Returns:
            bool: 格式合法且逻辑有效返回 True，否则返回 False（非字符串输入直接返回 False）

        Examples:
            >>> StringChecker.is_valid_time("14:30:25")
            True
            >>> StringChecker.is_valid_time("23.59")
            True
            >>> StringChecker.is_valid_time("25:30")  # 小时25无效
            False
            >>> StringChecker.is_valid_time("12:60:00")  # 分钟60无效
            False
        """
        if not isinstance(time_str, str) or not time_str.strip():
            return False

        # 定义默认允许的分隔符（COLON/DOT/HYPHEN）
        default_seps = {sep.value for sep in [
            TimeSeparator.COLON, TimeSeparator.DOT, TimeSeparator.HYPHEN
        ]}
        # 处理用户指定的分隔符（转换为字符集合）
        allowed_seps = {sep.value for sep in separators} if separators else default_seps

        # 提取并验证分隔符（整个时间必须使用同一分隔符）
        sep = None
        for c in time_str:
            if c in allowed_seps:
                if sep is None:
                    sep = c
                elif c != sep:
                    return False  # 混合分隔符无效
        if sep is None:
            return False  # 无有效分隔符

        # 拆分时分秒（支持 2 部分：时分 / 3 部分：时分秒）
        parts = time_str.split(sep)
        if len(parts) not in (2, 3):
            return False

        # 转换为数字并校验范围
        try:
            hour = int(parts[0])
            minute = int(parts[1])
            second = int(parts[2]) if len(parts) == 3 else 0  # 无秒时默认 0
        except ValueError:
            return False  # 非数字部分无效

        # 校验时分秒的逻辑有效性
        return (0 <= hour <= 23) and (0 <= minute <= 59) and (0 <= second <= 59)

    # ------------------------------
    # 字符类型判断
    # ------------------------------
    @staticmethod
    def is_digit(text: str) -> bool:
        """
        判断字符串是否仅包含数字字符（0-9）

        说明：
        - 空字符串返回 False
        - 仅包含数字字符（0-9）返回 True，否则返回 False
        - 不支持 Unicode 数字（如 ①、Ⅻ），仅支持 ASCII 数字

        Args:
            text: 待判断的字符串

        Returns:
            bool: 仅含数字返回 True，否则返回 False

        Examples:
            >>> StringChecker.is_digit("123456")
            True
            >>> StringChecker.is_digit("123abc")
            False
            >>> StringChecker.is_digit("")
            False
        """
        return text.isdigit()

    @staticmethod
    def is_alpha(text: str) -> bool:
        """
        判断字符串是否仅包含字母字符（大小写 pypi-z/A-Z）

        说明：
        - 空字符串返回 False
        - 仅包含字母字符返回 True，否则返回 False
        - 不支持 Unicode 字母（如 中文、日文），仅支持 ASCII 字母

        Args:
            text: 待判断的字符串

        Returns:
            bool: 仅含字母返回 True，否则返回 False

        Examples:
            >>> StringChecker.is_alpha("HelloWorld")
            True
            >>> StringChecker.is_alpha("Hello123")
            False
            >>> StringChecker.is_alpha("")
            False
        """
        return text.isalpha()

    @staticmethod
    def is_alnum(text: str) -> bool:
        """
        判断字符串是否仅包含字母和数字字符（pypi-z/A-Z/0-9）

        说明：
        - 空字符串返回 False
        - 仅包含字母和/或数字返回 True，否则返回 False
        - 不支持 Unicode 字符，仅支持 ASCII 字母和数字

        Args:
            text: 待判断的字符串

        Returns:
            bool: 仅含字母和数字返回 True，否则返回 False

        Examples:
            >>> StringChecker.is_alnum("Hello123")
            True
            >>> StringChecker.is_alnum("Hello!123")
            False
            >>> StringChecker.is_alnum("")
            False
        """
        return text.isalnum()

    @staticmethod
    def is_symbol(text: str) -> bool:
        """
        判断字符串是否仅包含符号字符（非字母、非数字、非空格）

        说明：
        - 空字符串返回 False
        - 符号定义：排除 ASCII 字母（pypi-z/A-Z）、ASCII 数字（0-9）、所有空格字符（空格、制表符等）
        - 支持的符号：!@#$%^&*()_+-=[]{}|;:,.<>? 等

        Args:
            text: 待判断的字符串

        Returns:
            bool: 仅含符号返回 True，否则返回 False

        Examples:
            >>> StringChecker.is_symbol("!@#$%")
            True
            >>> StringChecker.is_symbol("!@#123")
            False
            >>> StringChecker.is_symbol("")
            False
        """
        if not text:  # 空字符串直接返回 False
            return False
        for char in text:
            if char in string.ascii_letters or char in string.digits or char.isspace():
                return False
        return True

    @staticmethod
    def is_space(text: str) -> bool:
        """
        判断字符串是否仅包含空白字符（空格、制表符、换行符等）

        说明：
        - 空字符串返回 False
        - 仅包含空白字符（isspace() 为 True 的字符）返回 True，否则返回 False
        - 支持所有 Unicode 空白字符（如 空格、\t、\n、\r 等）

        Args:
            text: 待判断的字符串

        Returns:
            bool: 仅含空白字符返回 True，否则返回 False

        Examples:
            >>> StringChecker.is_space("  abc  ")
            False
            >>> StringChecker.is_space("")
            False
        """
        return text.isspace()

    # ------------------------------
    # 随机路径生成
    # ------------------------------
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
        """
        生成格式合法的随机路径字符串（兼容 Windows/POSIX，严格符合 is_valid_path 校验）

        核心特性：
        - 自动适配当前系统路径风格（默认），也可强制指定
        - 生成的路径 100% 符合对应系统的命名规则（无非法字符、保留名等）
        - 支持自定义路径深度、目录数量、文件名、后缀等参数
        - 极端情况自动重试，确保返回合法路径

        Args:
            style: 路径风格，默认 AUTO（自动适配当前系统），可选 POSIX/WINDOWS
            is_absolute: 是否生成绝对路径，True=绝对路径（默认），False=相对路径
            depth: 路径深度（包含的目录级数），默认 2 级（如 pypi/b/xxx.txt）
            dir_count: 每级目录下的子目录数量，默认 1 个（如 depth=2 时为 dir1/dir2）
            file_name: 自定义文件名（不含后缀），None 则随机生成（默认 None）
            extensions: 允许的文件后缀列表（如 [".yml", ".ini"]），None 则使用默认常见后缀
            min_component_len: 目录名/文件名（不含后缀）的最小长度，默认 3
            max_component_len: 目录名/文件名（不含后缀）的最大长度，默认 8

        Returns:
            str: 格式合法的随机路径字符串

        Examples:
            # 生成当前系统风格的绝对路径（默认配置）
            >>> StringChecker.get_random_path()
            # Windows 输出示例：C:\\xY7z_9\\kL3mN\\data87.csv
            # POSIX 输出示例：/ab3_cd/efg789/log123.txt

            # 生成 POSIX 风格相对路径（深度3级，自定义后缀）
            >>> StringChecker.get_random_path(
            ...     style=PathStyle.POSIX,
            ...     is_absolute=False,
            ...     depth=3,
            ...     extensions=[".yml", ".ini"],
            ...     min_component_len=2,
            ...     max_component_len=6
            ... )
            # 输出示例：xy_12/ab34/cd56/config.yml
        """
        # 1. 确定目标路径风格（与 is_valid_path 逻辑一致）
        if style == PathStyle.AUTO:
            target_style = PathStyle.WINDOWS if os.name == 'nt' else PathStyle.POSIX
        else:
            target_style = style

        # 2. 定义路径常量（分隔符、合法字符、根路径）
        if target_style == PathStyle.WINDOWS:
            sep = "\\"  # Windows 标准分隔符（兼容 /，但生成时用 \ 更符合习惯）
            # Windows 路径组件合法字符：字母、数字、下划线、连字符（排除非法字符）
            valid_chars = string.ascii_letters + string.digits + "_-"
            # Windows 绝对路径根：随机选择 C:/ 到 H:/ 盘符
            roots = [f"{chr(ord('C') + i)}:" for i in range(6)]  # C:/ D:/ ... H:/
        else:  # POSIX 风格
            sep = "/"  # POSIX 标准分隔符
            # POSIX 路径组件合法字符：字母、数字、下划线、连字符（后续会过滤 - 开头）
            valid_chars = string.ascii_letters + string.digits + "_-"
            roots = ["/"]  # POSIX 绝对路径根（仅 /）

        # 3. 生成单个合法的路径组件（目录名/文件名，不含后缀）
        def _random_component() -> str:
            """内部辅助函数：生成符合对应系统规则的路径组件"""
            length = random.randint(min_component_len, max_component_len)
            # 循环生成，直到满足所有规则（确保合法性）
            while True:
                component = ''.join(random.choice(valid_chars) for _ in range(length))
                # 按目标风格校验组件合法性
                if target_style == PathStyle.WINDOWS:
                    # Windows 组件规则：非保留名、非设备名、首尾无空格
                    if (not re.match(r'(?i)^(CON|PRN|AUX|NUL)(\..*)?$', component) and
                            not re.match(r'(?i)^(COM|LPT)([1-9])(\..*)?$', component) and
                            not component.startswith(' ') and not component.endswith(' ')):
                        break
                else:
                    # POSIX 组件规则：首尾无空格、不以 - 开头
                    if (not component.startswith(' ') and 
                        not component.endswith(' ') and 
                        not component.startswith('-')):
                        break
            return component

        # 4. 生成随机目录结构
        dir_components = []
        for _ in range(depth):
            # 每级目录下生成 dir_count 个子目录
            level_dirs = [_random_component() for _ in range(dir_count)]
            dir_components.extend(level_dirs)
        # 拼接目录部分（如 ["dir1", "dir2"] -> "dir1\\dir2" 或 "dir1/dir2"）
        dir_part = sep.join(dir_components)

        # 5. 生成文件名和后缀
        if file_name is None:
            file_base = _random_component()  # 随机生成文件名（不含后缀）
        else:
            # 自定义文件名：过滤非法字符，确保符合路径规则
            file_base = ''.join(c for c in file_name if c in valid_chars)
            # 若过滤后为空，使用随机生成的文件名兜底
            if not file_base:
                file_base = _random_component()

        # 处理文件后缀（默认使用常见后缀列表）
        default_extensions = [".txt", ".csv", ".json", ".log", ".bin", ".dat"]
        selected_ext = random.choice(extensions) if extensions else random.choice(default_extensions)
        file_part = f"{file_base}{selected_ext}"  # 完整文件名（含后缀）

        # 6. 拼接完整路径（区分绝对/相对路径）
        if is_absolute:
            root = random.choice(roots)  # 随机选择根路径
            if target_style == PathStyle.WINDOWS:
                # Windows 绝对路径：根路径 + 目录 + 文件（如 C:\\dir1\\dir2\\data.txt）
                full_path = f"{root}{sep}{dir_part}{sep}{file_part}"
            else:
                # POSIX 绝对路径：根路径 + 目录 + 文件（如 /dir1/dir2/data.txt）
                full_path = f"{root}{dir_part}{sep}{file_part}"
        else:
            # 相对路径：目录 + 文件（如 dir1/dir2/data.txt）
            full_path = f"{dir_part}{sep}{file_part}"

        # 7. 双重校验：确保生成的路径符合 is_valid_path 规则（极端情况重试）
        if StringChecker.is_valid_path(full_path, style=target_style):
            return full_path
        # 理论上不会触发，若触发则递归重试（确保返回合法路径）
        return StringChecker.get_random_path(
            style=target_style,
            is_absolute=is_absolute,
            depth=depth,
            dir_count=dir_count,
            file_name=file_name,
            extensions=extensions,
            min_component_len=min_component_len,
            max_component_len=max_component_len
        )

    @staticmethod
    def uniform_case(text: str, case_mode: str = 'lower') -> str:
        """
        将字符串转换为统一大小写格式

        Args:
            text: 待转换的字符串
            case_mode: 转换模式，可选 'lower'（小写，默认）或 'upper'（大写）

        Returns:
            str: 转换后的字符串

        Raises:
            TypeError: 输入非字符串时抛出
            ValueError: case_mode 不是 'lower' 或 'upper' 时抛出

        Examples:
            >>> StringChecker.uniform_case("Hello World")
            'hello world'
            >>> StringChecker.uniform_case("Hello World", case_mode='upper')
            'HELLO WORLD'
        """
        if not isinstance(text, str):
            raise TypeError("Input must be pypi string")

        if case_mode == 'lower':
            return text.lower()
        elif case_mode == 'upper':
            return text.upper()
        else:
            raise ValueError("case_mode must be 'lower' or 'upper'")

if __name__ == "__main__":
    pass