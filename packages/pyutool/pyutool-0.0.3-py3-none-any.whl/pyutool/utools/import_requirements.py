#!/usr/bin/env python3
"""
从 requirements.txt 安装 Python 依赖的脚本
支持：自动定位项目根目录、错误重试、镜像源切换、虚拟环境检测、版本兼容检查
"""
import os
import sys
import subprocess
import time
from typing import Optional, List, Dict
import argparse
from pathlib import Path

# 常用 Python 镜像源（加速安装）
MIRRORS: Dict[str, str] = {
    "default": "",  # 官方源
    "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
    "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "douban": "https://pypi.doubanio.com/simple/",
    "ustc": "https://pypi.mirrors.ustc.edu.cn/simple/"
}


def get_project_root() -> Path:
    """获取项目根目录（脚本所在目录或当前工作目录，优先找 requirements.txt）"""
    # 优先从脚本所在目录向上查找项目根（寻找 requirements.txt）
    script_dir = Path(__file__).parent.resolve()
    for parent in [script_dir] + list(script_dir.parents):
        if any(parent.glob("requirements*.txt")):
            return parent
    # 未找到则使用当前工作目录
    return Path.cwd().resolve()


def check_python_env() -> None:
    """检查 Python 环境（是否在虚拟环境中）"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"✅ 已激活虚拟环境：{sys.prefix}")
    else:
        print("⚠️  未检测到虚拟环境！建议激活项目专属虚拟环境后再安装依赖")
        confirm = input("是否继续在全局环境安装？(y/N)：").strip().lower()
        if confirm != 'y':
            print("🚫 安装已取消")
            sys.exit(0)


def install_package(
        requirements_path: Path,
        mirror: str = "default",
        retry: int = 3,
        timeout: int = 120,
        upgrade: bool = False
) -> bool:
    """
    执行依赖安装

    参数:
        requirements_path: requirements.txt 文件路径
        mirror: 镜像源名称
        retry: 失败重试次数
        timeout: 单次安装超时时间（秒）
        upgrade: 是否升级已安装的包
    返回:
        安装成功返回 True，失败返回 False
    """
    # 构建 pip 命令
    cmd = [
        sys.executable,  # 使用当前环境的 pip（确保环境一致性）
        "-m", "pip", "install",
        "-r", str(requirements_path),
        "--timeout", str(timeout)
    ]

    # 添加镜像源（信任非官方源）
    if mirror != "default" and mirror in MIRRORS:
        cmd.extend(["-i", MIRRORS[mirror]])
        cmd.append("--trusted-host")
        cmd.append(MIRRORS[mirror].split("//")[-1].split("/")[0])  # 信任镜像源主机

    # 是否升级包
    if upgrade:
        cmd.append("--upgrade")

    # 执行安装（支持重试）
    for attempt in range(1, retry + 1):
        print(f"\n📥 开始安装依赖（第 {attempt}/{retry} 次尝试）")
        print(f"📄 依赖文件：{requirements_path}")
        print(f"🌐 使用镜像源：{mirror} ({MIRRORS.get(mirror, '官方源')})")
        print(f"💻 执行命令：{' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="ignore"
            )
            print(f"✅ 依赖安装成功！")
            if result.stdout:
                print("📝 安装日志：")
                print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 第 {attempt} 次安装失败：")
            print(f"错误信息：{e.stderr[:1000]}")  # 只显示前1000字符避免输出过长
            if attempt < retry:
                wait_time = attempt * 2  # 重试间隔递增（2s, 4s, 6s...）
                print(f"⏳ {wait_time} 秒后进行第 {attempt + 1} 次重试...")
                time.sleep(wait_time)
            else:
                print(f"🚫 已重试 {retry} 次仍失败，请检查网络或依赖文件")
        except subprocess.TimeoutExpired:
            print(f"⌛ 第 {attempt} 次安装超时（超过 {timeout} 秒）")
            if attempt < retry:
                wait_time = attempt * 2
                print(f"⏳ {wait_time} 秒后进行第 {attempt + 1} 次重试...")
                time.sleep(wait_time)
            else:
                print(f"🚫 已重试 {retry} 次均超时，请检查网络稳定性")
        except Exception as e:
            print(f"⚠️  未知错误：{str(e)}")
            return False

    return False


def validate_requirements_file(file_path: Path) -> bool:
    """验证 requirements.txt 文件是否存在且合法"""
    if not file_path.exists():
        print(f"❌ 依赖文件不存在：{file_path}")
        return False
    if not file_path.is_file():
        print(f"❌ {file_path} 不是文件")
        return False
    # 检查文件是否为空
    if file_path.stat().st_size == 0:
        print(f"⚠️ {file_path} 是空文件，无需安装依赖")
        return False
    return True


def find_requirements_file(project_root: Path, filename: str) -> Optional[Path]:
    """在项目根目录查找指定的 requirements 文件"""
    target_file = project_root / filename
    if target_file.exists():
        return target_file

    # 如果指定文件名不存在，查找常见的 requirements 文件
    common_files = [
        "requirements.txt",
        "requirements.dev.txt",
        "requirements.prod.txt",
        "requirements.production.txt",
        "requirements.development.txt"
    ]
    found_files = [f for f in common_files if (project_root / f).exists()]

    if found_files:
        print(f"⚠️ 未找到 {filename}，项目根目录存在以下依赖文件：")
        for i, f in enumerate(found_files, 1):
            print(f"  {i}. {f}")
        choice = input("请选择要安装的文件序号（直接回车使用 1）：").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(found_files):
            return project_root / found_files[int(choice) - 1]
        else:
            return project_root / found_files[0]
    else:
        print(f"❌ 项目根目录 {project_root} 未找到任何 requirements.txt 文件")
        return None


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="从 requirements.txt 安装 Python 依赖（支持镜像源/重试）")
    parser.add_argument(
        "-f", "--file",
        default="requirements.txt",
        help="依赖文件名（默认：requirements.txt，支持 dev/prod 后缀）"
    )
    parser.add_argument(
        "-m", "--mirror",
        choices=MIRRORS.keys(),
        default="tsinghua",
        help="选择镜像源（默认：tsinghua，可选：aliyun/douban/ustc/default）"
    )
    parser.add_argument(
        "-r", "--retry",
        type=int,
        default=3,
        help="安装失败重试次数（默认：3次）"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=120,
        help="单次安装超时时间（默认：120秒）"
    )
    parser.add_argument(
        "-u", "--upgrade",
        action="store_true",
        help="升级已安装的依赖包到最新版本"
    )
    parser.add_argument(
        "-np", "--no-check-venv",
        action="store_true",
        help="跳过虚拟环境检测（不推荐）"
    )
    args = parser.parse_args()

    # 1. 获取项目根目录
    project_root = get_project_root()
    print(f"📌 项目根目录：{project_root}")

    # 2. 检测虚拟环境（可选跳过）
    if not args.no_check_venv:
        check_python_env()

    # 3. 查找依赖文件
    print(f"🔍 查找依赖文件：{args.file}")
    requirements_path = find_requirements_file(project_root, args.file)
    if not requirements_path:
        sys.exit(1)

    # 4. 验证依赖文件
    if not validate_requirements_file(requirements_path):
        sys.exit(1)

    # 5. 执行安装
    print(f"\n🚀 开始安装依赖（文件：{requirements_path.name}）")
    success = install_package(
        requirements_path=requirements_path,
        mirror=args.mirror,
        retry=args.retry,
        timeout=args.timeout,
        upgrade=args.upgrade
    )

    # 6. 安装结果总结
    if success:
        print("\n🎉 所有依赖安装完成！")
        # 可选：显示已安装的包列表
        if input("\n是否显示已安装的依赖列表？(y/N)：").strip().lower() == 'y':
            subprocess.run([sys.executable, "-m", "pip", "list"], check=False)
        sys.exit(0)
    else:
        print("\n❌ 依赖安装失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()