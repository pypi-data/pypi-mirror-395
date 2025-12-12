
# -*- coding: utf-8 -*-
import os
import sys

# -*- coding: utf-8 -*-


python = sys.version[0:3]
int_python = float(python)
if 2.6 <= int_python < 3.5:
    condition = 'format'
elif int_python >= 3.5:
    condition = 'f'
elif int_python < 2.6:
    condition = 's'
else:
    condition = 'error'


def resolve_path(path):
    """处理路径，移除引号并进行基本验证"""
    try:
        # 去除首尾可能的引号
        path = path.strip('"').strip("'")

        # 如果输入的是桌面上的快捷方式或重命名的文件
        if 'Desktop' in path and 'run_code' in path:
            # 直接使用实际文件的路径
            actual_path = r'/pyutool/utools/run_code.py'
            if os.path.isfile(actual_path):
                print(f"找到实际文件: {actual_path}")
                return actual_path

        # 如果不是特殊情况，使用输入的路径
        abs_path = os.path.abspath(path)
        print(f"使用路径: {abs_path}")
        return abs_path
    except Exception as e:
        print(f"处理路径时出错: {e}")
        return path


while True:
    path = input("请输入执行路径:")
    target_path = resolve_path(path)

    if os.path.isfile(target_path):
        print(f"准备执行文件: {target_path}")
        if condition == 'f':
            os.system(f'python "{target_path}"')
            exit()
        elif condition == 'format':
            os.system('python "{path}"'.format(path=target_path))
            exit()
        elif condition == 's':
            os.system('python "%s"' % target_path)
            exit()
    elif condition == 'error':
        print('python版本出错了')
        input()
    else:
        print(f'路径不存在: {target_path}')
        print('请检查文件是否存在，或直接输入.py文件的完整路径')
