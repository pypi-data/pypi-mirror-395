# -*- coding: utf-8 -*-
import time
import os
import random
import inspect
import shutil

codes = input('输入要执行的Python代码:')

try:
    exec(codes, globals(), globals())
except Exception as e:
    print('发生了未知错误:', e)
input('按下任意键继续...')
