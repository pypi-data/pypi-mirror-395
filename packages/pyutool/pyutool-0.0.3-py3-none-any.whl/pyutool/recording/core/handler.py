# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : handler
@Author  : YL_top01
@Date    : 2025/8/25 16:06
"""

# Built-in modules
from pathlib import Path
import warnings

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)

class LogRotator:
    @staticmethod
    def safe_rollover(current_log_path: Path, backups: int):
        """安全轮转日志（迁移自Logger._safe_rollover）"""
        base_name = current_log_path.stem
        # 备份文件轮转
        for i in range(backups - 1, 0, -1):
            src = current_log_path.parent / f"{base_name}.{i}"
            if src.exists():
                dst = current_log_path.parent / f"{base_name}.{i + 1}"
                try:
                    if dst.exists():
                        dst.unlink()
                    src.rename(dst)
                except Exception as e:
                    warnings.warn(f"备份重命名失败: {str(e)}")
        # 重命名当前日志
        if current_log_path.exists():
            first_backup = current_log_path.parent / f"{base_name}.1"
            try:
                if first_backup.exists():
                    first_backup.unlink()
                current_log_path.rename(first_backup)
            except Exception as e:
                warnings.warn(f"当前日志重命名失败: {str(e)}")
