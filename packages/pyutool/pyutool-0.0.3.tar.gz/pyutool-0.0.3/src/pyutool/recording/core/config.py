# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : config
@Author  : YL_top01
@Date    : 2025/4/5 10:33
"""

"""配置模块"""
# Built-in modules
import os
import re
import configparser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)

@dataclass
class LogConfig:
    """
    日志配置类，控制日志的存储、格式和行为。

    字段说明：
    - name: 日志名称（用于区分不同日志器实例）
    - log_dir: 日志存储目录（支持相对路径，结合base_dir使用）
    - base_dir: 基础路径，log_dir为相对路径时的参考目录（默认当前工作目录）
    - use_caller_path: 若为True，自动将日志目录基于调用者路径计算（适合多模块场景）
    - max_size: 单个日志文件最大大小（字节），超过触发轮转（默认10MB）
    - backups: 日志轮转时保留的备份文件数（默认5个）
    - enable_daily: 是否按日期拆分日志（每日一个子目录，格式由date_dir_format控制）
    - date_dir_format: 日期目录格式（strftime格式，默认"%Y/%m/%d"）
    - language: 错误消息语言（"zh"中文 / "en"英文，默认"zh"）
    - encoding: 日志文件编码（推荐"utf-8-sig"以支持中文，默认"utf-8-sig"）
    - enable_console: 是否在控制台输出日志（默认True）
    """
    # 基础配置
    name: str = "app"  # 日志名称
    log_dir: str = "logs"  # 默认相对路径
    language: str = "zh"  # 显示语言

    # 新增日志字段配置
    log_fields: Dict[str, bool] = field(default_factory=lambda: {
        "timestamp": True,
        "level": True,
        "error_type": True,
        "location": True,
        "message": True
    })

    # 轮转配置
    max_size: int = 10 * 1024 * 1024  # 10MB
    backups: int = 5  # 保留备份数

    # 功能开关
    enable_console: bool = True  # 控制台输出
    enable_daily: bool = True  # 按日分割
    auto_create_dir: bool = True  # 自动创建目录

    # 格式配置
    date_dir_format: str = "%Y/%m/%d"  # ✅ 新增日期目录格式字段
    log_format: str = (
        "{log_timestamp} | {log_level} | {log_message} | "  
        "{log_file}:{log_line}"
    )
    encoding: str = "utf-8-sig"
    # 新增字段
    base_dir: Optional[str] = None  # 新增基础路径配置
    use_abs_path: bool = False  # 是否强制使用绝对路径
    use_caller_path: bool = True  # ✅ 新增：是否自动检测调用者路径
    skip_frames: list[str] = field(default_factory=lambda: [
        "pytest",
        "unittest",
        "recording"  # 跳过自身模块的调用栈
    ])
    time_format: Optional[str] = "%Y-%m-%d %H:%M:%S"  # 默认ISO风格时间格式
    @classmethod
    def from_ini(cls, path: str) -> "LogConfig":
        """从INI文件加载配置"""
        cfg = configparser.ConfigParser()
        cfg.read(path, encoding='utf-8')

        return cls(
            name=cfg.get('DEFAULT', 'Name', fallback='app'),
            log_dir=cfg.get('DEFAULT', 'LogDir', fallback='logs'),
            max_size=cfg.getint('DEFAULT', 'MaxSize', fallback=10_485_760),
            backups=cfg.getint('DEFAULT', 'Backups', fallback=5),
            language=cfg.get('DEFAULT', 'Language', fallback='zh'),
            enable_console=cfg.getboolean('DEFAULT', 'Console', fallback=True),
            enable_daily=cfg.getboolean('DEFAULT', 'Daily', fallback=True),
            time_format=cfg.get('DEFAULT', 'TimeFormat', fallback="%Y-%m-%d %H:%M:%S")
        )

    def _generate_log_format(self) -> str:
        """确保每个字段对应extra中的键"""
        field_map = {
            "timestamp": "%(log_timestamp)s",
            "level": "%(log_level)-8s",  # 左对齐8字符
            "message": "%(log_message)s",
            "file": "%(log_file)s",
            "line": "%(log_line)d",
            "function": "%(log_function)s",
            "context": "%(log_context)s"
        }
        ordered_fields = [
            "timestamp",
            "level",
            "message",
            "file",
            "line",
            "function",
            "context"
        ]

        enabled = []
        for field in ordered_fields:
            if self.log_fields.get(field, False):
                fmt = field_map[field]
                enabled.append(fmt)

        return " | ".join(enabled)

    def __post_init__(self):
        ConfigValidator.validate_log_dir(self.log_dir)

class ConfigValidator:
    @staticmethod
    def validate_log_dir(path: str):
        normalized = os.path.normpath(path).replace("\\", "/")
        if not re.match(r'^[\w/:.\-_\s]+$', normalized):
            raise ValueError(f"非法日志路径: {path}")

# LogConfig 中调用

def get_default_path() -> Path:
    """获取模块级默认日志路径"""
    module_path = Path(__file__).parent
    return module_path / "logs"
