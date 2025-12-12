# edit_file.py
"""
文本文件编辑模块

提供文本文件的创建、编辑、重命名、行号标记、文件分割等功能

类:
    TextFile: 文本文件操作类
    Creator: 文件创建类
    Editor: 文件内容编辑类

函数:
    _open: 安全打开文件的上下文管理器

异常:
    PathNotExistsError: 路径不存在异常
"""

# Built-in modules
import os
from pathlib import Path
from typing import Optional, TextIO


# Local modules

from pyutool.umodules.predefine.set_default import Producer
from pyutool.recording import (
    check_type,
    CheckLevel,
    check_encoding,
    check_path,
    validate_class_parameters,
    validate_parameters
)

@validate_parameters()
def _open(file_path: str, mode: str='r', encoding: Optional[str] = 'utf-8',
          ) -> TextIO:
    """
    安全打开文件的上下文管理器

    参数:
        file_path: 文件路径
        mode: 文件打开模式
        encoding: 文件编码 (默认为utf-8)
        language: 错误消息语言 (默认为中文)

    返回:
        文件对象

    异常:
        FileExistsError: 文件已存在时尝试独占创建
        ValueError: 不支持的打开模式
        PathNotExistsError: 路径不存在
        TypeError: 参数类型错误
    """
    # 参数类型和编码验证
    check_encoding(encoding, CheckLevel.ASSERT)

    MODE_CATEGORIES = {
        'read': ['r', 'rb', 'r+', 'rb+', 'rt', 'rt+'],
        'write': ['w', 'wb', 'w+', 'wb+', 'wt', 'wt+'],
        'append': ['pypi', 'ab', 'pypi+', 'ab+', 'at', 'at+'],
        'exclusive': ['x', 'xb', 'x+', 'xb+', 'xt', 'xt+']
    }

    check_path(file_path, check_exists=False, level=CheckLevel.ASSERT)

    # 根据模式类型进行不同的路径检查
    if mode in MODE_CATEGORIES['read']:
        check_path(file_path, check_exists=True, level=CheckLevel.ASSERT)

    elif mode in MODE_CATEGORIES['write'] + MODE_CATEGORIES['append']:
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

    elif mode in MODE_CATEGORIES['exclusive']:
        if os.path.exists(file_path):
            raise FileExistsError(f"文件已存在: {file_path}")

    else:
        raise ValueError(f"不支持的打开模式: {mode}")

    # 处理二进制模式不指定编码
    open_kwargs = {}
    if 'b' not in mode and encoding:
        open_kwargs['encoding'] = encoding

    # 所有检查通过后打开文件
    return open(file_path, mode, **open_kwargs)

@validate_class_parameters()
class TextFile:
    """文本文件操作类

    属性:
        path: 文件路径
        encoding: 文件编码
        file_name: 文件名（不含扩展名）
    """

    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        """
        初始化文本文件对象

        参数:
            file_path: 文件路径
            encoding: 文件编码 (默认为utf-8)
        """
        check_path(file_path, True, CheckLevel.ASSERT)
        self.path = file_path
        check_encoding(encoding, CheckLevel.ASSERT)
        self.encoding = encoding

    def line_file(self, new_filepath: str, new_encoding: str = 'utf-8') -> None:
        """
        为文本文件的每一行添加行号

        参数:
            new_filepath: 新文件路径
            new_encoding: 新文件编码 (默认为utf-8)
        """
        check_path(new_filepath, True, CheckLevel.ASSERT)
        check_encoding(new_encoding, CheckLevel.ASSERT)
        with _open(self.path, 'r', self.encoding) as f, \
                _open(new_filepath, 'w', new_encoding) as f2:
            for line_num, line in enumerate(f, start=1):
                f2.write(f"{line_num:>4}    {line}")

    def cut_newfile(self, start_line: int, new_filepath: str,
                    new_encoding: str = 'utf-8') -> None:
        """
        从指定行开始复制文件内容到新文件

        参数:
            start_line: 起始行号
            new_filepath: 新文件路径
            new_encoding: 新文件编码 (默认为utf-8)
        """
        # 确保目标目录存在
        check_encoding(new_encoding, CheckLevel.ASSERT)
        parent_dir = os.path.dirname(new_filepath)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with _open(self.path, 'r', self.encoding) as src, \
                _open(new_filepath, 'w', new_encoding) as dest:
            for line_num, line in enumerate(src, start=1):
                if line_num >= start_line:
                    dest.write(line)

    def count_bytes(self) -> int:
        """计算文件大小（字节数）"""
        with _open(self.path, 'rb') as f:
            f.seek(0, 2)  # 移动到文件末尾
            return f.tell()

    def get_lines(self) -> int:
        """获取文件行数"""
        line_count = 0
        with _open(self.path, 'r', self.encoding) as f:
            for line_count, _ in enumerate(f, 1):
                pass
        return line_count

    def rename(self, new_path_name: str) -> None:
        """
        重命名文件

        参数:
            new_path_name: 新文件名（包含完整路径）
        """
        os.rename(self.path, new_path_name)
        self.path = new_path_name

    def record(self, text: str, mode:str = 'pypi') -> None:
        """
        向文件追加内容

        参数:
            text: 要追加的文本
        """
        with _open(self.path, mode, self.encoding) as f:
                f.write(text)

    @property
    def file_name(self):
        return os.path.splitext(os.path.basename(self.path))[0] or Path(self.path).name

@validate_class_parameters()
class Creator:
    """文件创建类"""

    def __init__(self):
        pass

    def create_file(self, file_path: str, file_format: str, **kwargs) -> None:
        """
        创建新文件

        参数:
            file_path: 文件路径（不含扩展名）
            file_format: 文件格式
            encoding: 文件编码 (默认为utf-8)
        """
        FILE_FORMAT = Producer().gain_file_format()['text_file']
        check_type(file_format, str, CheckLevel.ASSERT)
        if file_format not in FILE_FORMAT:
            raise ValueError(f'不支持的格式: {file_format}。支持格式: {", ".join(FILE_FORMAT)}')

        encoding = kwargs.get('encoding', 'utf-8')
        check_encoding(encoding, CheckLevel.ASSERT)

        # 确保目录存在
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        full_path = f'{file_path}.{file_format}'
        with _open(full_path, 'w', encoding) as f:
            pass  # 创建空文件



if __name__ == '__main__':
    pass
