# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# 读取 README.md 作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # 1. 包的基本信息
    name="pyutool",  # 你的包在 PyPI 上的名称，必须唯一
    version="0.1.6",  # 版本号，遵循语义化版本规范
    author="YL_top01",
    author_email="2787284002@qq.com",
    description="A brief description of your Vientiane Arena project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YLtop01/my-awesome-project",  # 项目的 GitHub 地址
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # 2. 包的源代码配置 (关键)
    package_dir={"": "src"},  # 告诉 setuptools 所有包都在 'src' 目录下
    packages=find_packages(where="src"),  # 自动查找 'src' 下的所有包

    # 3. 命令行入口配置 (非常重要)
    # 这部分让用户可以在安装后直接在终端运行你的程序
    entry_points={
        'console_scripts': [
            # 格式: '终端命令 = 包.模块:函数'
            # 假设你的主程序入口是 game_engine.py 里的 main 函数
            # 'pyutool = pyutool.game_engine:main',
        ],
    },

    # 4. 包含非 Python 文件 (如 .txt, .ini)
    # 如果你的包需要这些资源文件才能运行，必须在这里声明
    package_data={
        # 'pyutool': ['__modules__.txt'],  # 包含 pyutool 目录下的 __modules__.txt
        'pyutool.umodules': ['config.ini'], # 包含 pyutool/umodules 目录下的 config.ini
    },

    # 5. 项目依赖
    # 如果你的代码依赖其他第三方库 (如 requests, numpy)，在这里列出
    install_requires=[
        # 'requests>=2.25.1',
        # 'numpy',
    ],

    # 6. Python 版本要求
    python_requires=">=3.6",
)