# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : log_parsing
@Author  : YL_top01
@Date    : 2025/8/25 15:59
"""



# Built-in modules
import json
import logging
import os
from pathlib import Path

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)

def read_last_log(logger) -> dict:
    """
    读取最新日志条目

    参数:
        logger: 日志记录器实例

    返回:
        解析后的日志字典
    """
    latest_log = {}
    log_dir = Path(logger.config.log_dir)

    # 查找所有日志文件
    log_files = sorted(
        log_dir.glob("**/*.log"),
        key=os.path.getmtime,
        reverse=True
    )

    # 从最新文件开始读取
    for log_file in log_files:
        if not log_file.is_file():
            continue

        try:
            with open(log_file, "r", encoding=logger.config.encoding) as f:
                # 读取最后一行非空内容
                for line in reversed(f.readlines()):
                    if line.strip():
                        latest_log = _parse_log_line(line.strip())
                        if latest_log:  # 找到有效日志则返回
                            return latest_log
        except Exception as e:
            logging.error(f"日志文件读取失败: {log_file} - {str(e)}")

    return latest_log


def _parse_log_line(line: str) -> dict:
    """解析单行日志内容"""
    line = line.strip().lstrip('\ufeff')
    try:
        # 尝试解析为JSON
        return json.loads(line)
    except json.JSONDecodeError:
        # 回退到旧格式解析
        return _parse_legacy_log_line(line)


def _parse_legacy_log_line(line: str) -> dict:
    """解析旧格式日志行"""
    parts = line.split("|", 6)  # 只分割6次
    context = {}

    # 尝试解析上下文
    if len(parts) > 6:
        try:
            context = json.loads(parts[6])
        except:
            context = {"raw": parts[6]}

    return {
        "timestamp": parts[0].strip() if len(parts) > 0 else "",
        "level": parts[1].strip()[:8] if len(parts) > 1 else "",
        "message": parts[2].strip() if len(parts) > 2 else "",
        "file": parts[3].strip() if len(parts) > 3 else "",
        "line": int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0,
        "function": parts[5].strip() if len(parts) > 5 else "",
        "context": context
    }
