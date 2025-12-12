#!/usr/bin/env python3
"""
自动生成 requirements.txt 的 Python 脚本
默认在项目根目录生成，支持过滤无用依赖、开发/生产依赖分离等
"""
import os
import sys
import subprocess
from typing import List, Optional, Set
import argparse
from pathlib import Path

# 常见的系统级/基础依赖（通常不需要写入 requirements.txt）
SYSTEM_DEPENDENCIES = {
    "python", "pip", "setuptools", "wheel", "distlib",
    "pkg-resources", "wincertstore", "certifi",  # 证书相关
    "easy_install", "pipenv", "poetry",  # 包管理工具
    "virtualenv", "venv",  # 虚拟环境工具
}


def get_project_root(project_path: Optional[str] = None) -> Path:
    """
    获取项目根目录（优先使用指定路径，否则用脚本所在目录）
    确保生成的 requirements.txt 在项目根目录下
    """
    if project_path:
        root = Path(project_path).resolve()
        if not root.is_dir():
            print(f"⚠️ 指定的项目路径 {root} 不是目录，将使用脚本所在目录作为项目根")
            root = Path(__file__).parent.resolve()
    else:
        # 默认为脚本所在目录（即项目根目录，建议将脚本放在项目根目录运行）
        root = Path(__file__).parent.resolve()
    return root


def get_installed_packages() -> List[str]:
    """获取当前环境中安装的所有 Python 包（名称==版本）"""
    try:
        # 使用当前环境的 Python 解释器，确保依赖准确性
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        # 按行分割，过滤空行
        packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return packages
    except subprocess.CalledProcessError as e:
        print(f"❌ 获取安装包失败：{e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ 未找到 Python 解释器：{sys.executable}", file=sys.stderr)
        sys.exit(1)


def filter_packages(packages: List[str], exclude: Set[str]) -> List[str]:
    """过滤不需要的依赖包"""
    filtered = []
    for pkg in packages:
        # 分离包名和版本（处理带 extras 的情况，如 requests[security]==2.31.0）
        pkg_name = pkg.split("[")[0].split("==")[0].lower()
        if pkg_name not in exclude:
            filtered.append(pkg)
    return filtered


def get_project_dependencies(project_root: Path) -> Optional[Set[str]]:
    """分析项目实际依赖的包（基于导入语句）"""
    try:
        import ast

        imported_packages = set()
        for py_file in project_root.rglob("*.py"):
            # 跳过虚拟环境、__pycache__、测试目录等无关目录
            skip_dirs = ["venv", "__pycache__", "test", "_tests", ".git", ".idea", "dist", "build"]
            if any(part in str(py_file).lower() for part in skip_dirs):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                # 分析导入语句（取顶级包名）
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imported_packages.add(alias.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imported_packages.add(node.module.split(".")[0])
            except SyntaxError:
                continue  # 忽略语法错误的文件
            except PermissionError:
                continue  # 忽略无权限访问的文件

        return imported_packages if imported_packages else None
    except ImportError:
        print("⚠️ 无法分析项目依赖（缺少必要模块），将导出所有非系统依赖")
        return None


def generate_requirements(
        project_path: Optional[str] = None,
        output_filename: str = "requirements.txt",
        include_system: bool = False,
        dev: bool = False
) -> None:
    """
    生成 requirements.txt 文件（默认在项目根目录）

    参数:
        project_path: 项目目录路径（默认：脚本所在目录）
        output_filename: 输出文件名（默认：requirements.txt）
        include_system: 是否包含系统级依赖（默认：不包含）
        dev: 是否生成开发环境依赖（文件名改为 requirements.dev.txt）
    """
    # 1. 确定项目根目录（核心：确保文件生成在根目录）
    project_root = get_project_root(project_path)
    print(f"📌 项目根目录：{project_root}")

    # 2. 获取所有安装的包
    print("🔍 获取当前环境安装的包...")
    all_packages = get_installed_packages()
    print(f"✅ 找到 {len(all_packages)} 个已安装包")

    # 3. 过滤依赖
    print("🚀 过滤依赖包...")
    exclude_packages = SYSTEM_DEPENDENCIES if not include_system else set()

    # 分析项目实际导入的依赖（只保留需要的包，减少冗余）
    project_imports = get_project_dependencies(project_root)
    if project_imports:
        project_imports_lower = {pkg.lower() for pkg in project_imports}
        filtered_packages = [
            pkg for pkg in all_packages
            if pkg.split("[")[0].split("==")[0].lower() in project_imports_lower
        ]
        print(f"✅ 过滤后保留 {len(filtered_packages)} 个项目实际依赖包")
    else:
        filtered_packages = filter_packages(all_packages, exclude_packages)
        print(f"✅ 过滤系统依赖后保留 {len(filtered_packages)} 个包")

    # 4. 处理输出文件名和路径（确保在项目根目录）
    if dev:
        # 开发环境依赖：requirements.dev.txt
        base, ext = os.path.splitext(output_filename)
        output_filename = f"{base}.dev{ext}"
    output_path = project_root / output_filename  # 直接拼接根目录和文件名

    # 5. 写入文件
    print(f"📝 写入依赖到：{output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(filtered_packages)))  # 排序后写入，便于版本控制

    print(f"🎉 成功生成！文件位置：{output_path}")
    print(f"📊 共包含 {len(filtered_packages)} 个依赖包")


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="自动生成 requirements.txt（默认在项目根目录）")
    parser.add_argument(
        "-p", "--project",
        help="项目目录路径（默认：脚本所在目录，即项目根目录）"
    )
    parser.add_argument(
        "-f", "--filename",
        default="requirements.txt",
        help="输出文件名（默认：requirements.txt）"
    )
    parser.add_argument(
        "-s", "--include-system",
        action="store_true",
        help="是否包含系统级依赖（默认：不包含）"
    )
    parser.add_argument(
        "-d", "--dev",
        action="store_true",
        help="生成开发环境依赖（文件名改为 requirements.dev.txt）"
    )
    args = parser.parse_args()

    # 执行生成
    generate_requirements(
        project_path=args.project,
        output_filename=args.filename,
        include_system=args.include_system,
        dev=args.dev
    )


if __name__ == "__main__":
    main()