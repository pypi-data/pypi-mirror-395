# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : reporter.py
@Author  : YL_top01
@Date    : 2025/8/25 15:59
提供功能:
- 日志频率统计
- 错误类型分析
- 模块使用统计
"""

# Built-in modules
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, Iterator, Any
import json
import logging

# Third-party modules
# (无第三方依赖)


# Local modules
# (无本地依赖)

class LogAnalyzer:
    """日志分析器"""

    def __init__(self, logger):
        """
        初始化日志分析器

        参数:
            logger: 日志记录器实例
        """
        self.logger = logger
        self._cache = {}

    def frequency_report(self) -> Dict[str, Dict]:
        """
        生成频率报告

        返回:
            包含以下统计的字典:
            - daily: 每日日志数量
            - hourly: 每小时日志数量
            - errors: 错误类型统计
            - modules: 模块使用统计
        """
        report = {
            'daily': defaultdict(int),
            'hourly': defaultdict(int),
            'errors': defaultdict(int),
            'modules': defaultdict(int)
        }

        # 遍历所有日志条目
        for entry in self._parse_logs():
            self._process_timestamp(entry, report)
            self._process_error_type(entry, report)
            self._process_module(entry, report)

        # 转换为普通字典
        return {k: dict(v) for k, v in report.items()}

    def _process_timestamp(self, entry: dict, report: dict):
        """处理时间戳信息"""
        timestamp = entry.get("timestamp")
        if not timestamp:
            return

        try:
            dt = datetime.fromisoformat(timestamp)
            report['daily'][dt.date().isoformat()] += 1
            report['hourly'][dt.hour] += 1
        except (ValueError, TypeError):
            pass

    def _process_error_type(self, entry: dict, report: dict):
        """处理错误类型"""
        error_type = entry.get("error_type")
        if error_type:
            report['errors'][error_type] += 1

    def _process_module(self, entry: dict, report: dict):
        """处理模块信息"""
        module = entry.get("context", {}).get("module")
        if module:
            report['modules'][module] += 1

    def _parse_logs(self) -> Iterator[dict]:
        """遍历日志目录解析所有日志文件"""
        log_dir = Path(self.logger.full_log_dir)

        # 递归查找所有日志文件
        for log_file in log_dir.glob("**/*.log"):
            if not log_file.is_file():
                continue

            try:
                with open(log_file, 'r', encoding=self.logger.config.encoding) as f:
                    for line in f:
                        yield self._parse_line(line)
            except Exception as e:
                logging.error(f"日志文件解析失败: {log_file} - {str(e)}")

    def _parse_line(self, line: str) -> dict:
        """解析单行日志内容"""
        try:
            entry = json.loads(line)
            return {
                "error_type": entry.get("error_type"),
                "module": entry.get("module"),
                "timestamp": entry.get("timestamp")
            }
        except json.JSONDecodeError:
            # 尝试提取部分信息
            return self._parse_invalid_line(line)
        except Exception as e:
            logging.error(f"日志行解析异常: {str(e)}")
            return {}

    def _parse_invalid_line(self, line: str) -> dict:
        """解析无效JSON的日志行"""
        # 尝试提取时间戳
        timestamp = None
        if '"timestamp":' in line:
            try:
                ts_start = line.index('"timestamp":') + len('"timestamp":')
                ts_end = line.index(',', ts_start)
                timestamp = line[ts_start:ts_end].strip(' "')
            except (ValueError, IndexError):
                pass

        return {
            "error_type": "InvalidLogFormat",
            "module": "LogAnalyzer",
            "timestamp": timestamp
        }