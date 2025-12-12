# -*- coding: utf-8 -*-
"""
@File    : configer
@Author  : YL_top01
@Date    : 2025/2/1 22:54
"""
# Built-in modules
import os
import sys
from typing import Any

# Third-party modules
# (无第三方依赖)

# Local modules
from pyutool.recording import check_encoding, check_path
from pyutool.recording import CheckLevel, validate_class_parameters
from pyutool import _open, TextFile
@validate_class_parameters()
class Config:
    def __init__(self, config_path: str, encoding: str = 'utf-8'):
        if not check_encoding(encoding, CheckLevel.BOOL, None):
            encoding = 'utf-8'
        if not check_path(
                path=config_path,
                check_exists=True,
                level=CheckLevel.BOOL
        ):
            check_path(config_path, check_exists=False, level=CheckLevel.ASSERT)
            f = TextFile(config_path, encoding)
            f.record("[DEFAULT]\n", 'w')

        self.path = config_path
        self.encoding = encoding

    def sections(self):
        sections = []
        with _open(self.path, mode='rt', encoding=self.encoding) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):  # 忽略注释行
                    continue
                if line.startswith('[') and line.endswith(']'):
                    sections.append(line[1:-1])
        return sections

    def options(self, section: str):
        options = []
        with _open(self.path, mode='rt', encoding=self.encoding) as f:
            in_section = False
            for line in f:
                line = line.strip()
                if line.startswith('#'):  # 忽略注释行
                    continue
                if line.startswith('[') and line.endswith(']'):
                    in_section = line[1:-1] == section
                elif in_section and (':' in line or '=' in line):
                    options.append(line.split(':', 1)[0].strip() if ':' in line else line.split('=', 1)[0].strip())
        return options

    def values(self, section: str):
        values = []
        with _open(self.path, mode='rt', encoding=self.encoding) as f:
            in_section = False
            for line in f:
                line = line.strip()
                if line.startswith('#'):  # 忽略注释行
                    continue
                if line.startswith('[') and line.endswith(']'):
                    in_section = line[1:-1] == section
                elif in_section and (':' in line or '=' in line):
                    values.append(line.split(':', 1)[-1].strip() if ':' in line else line.split('=', 1)[-1].strip())
        return values

    def get_value(self, section: str, option: str, default_value: Any=None):
        """获取指定 section 和 option 的值"""
        with _open(self.path, mode='rt', encoding=self.encoding) as f:
            in_section = False
            for line in f:
                line = line.strip()
                if line.startswith('#'):  # 忽略注释行
                    continue
                if line.startswith('[') and line.endswith(']'):
                    in_section = line[1:-1] == section
                elif in_section and (option in line):
                    if ':' in line:
                        key, value = line.split(':', 1)
                    elif '=' in line:
                        key, value = line.split('=', 1)
                    else:
                        continue

                    if key.strip() == option:
                        return value.strip()
        return default_value

    def get_items(self, section: str):
        options = self.options(section)
        values = self.values(section)
        return dict(zip(options, values))

    def get_section(self, section: str):
        with _open(self.path, encoding=self.encoding, mode='rt') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip().startswith('#'):  # 忽略注释行
                    continue
                if line.strip()[1:-1] == section:
                    return line_num
        return None

    def set_option(self, section: str, option: str, value: any):
        sections = self.sections()
        if section not in sections:
            return

        new_file = self.path + '.tmp'
        with _open(self.path, mode='rt', encoding=self.encoding) as f, _open(new_file, mode='wt', encoding=self.encoding) as nf:
            in_section = False
            for line in f:
                stripped_line = line.strip()
                if stripped_line.startswith('#'):  # 忽略注释行
                    nf.write(line)
                    continue
                if stripped_line.startswith('[') and stripped_line.endswith(']'):
                    in_section = stripped_line[1:-1] == section
                if in_section and (option + ':' in line or option + '=' in line):
                    line = f'{option} = {value}\n'
                nf.write(line)
        os.replace(new_file, self.path)

    # Placeholder for add_section method
    def add_section(self):
        pass

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')
    configer = Config(CONFIG_PATH)
    print(configer.sections())