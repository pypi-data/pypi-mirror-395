# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : directory_structure
@Author  : YL_top01
@Date    : 2025/6/8 9:53
"""
import os
import argparse
import sys

'''
# 方式1：命令行使用
python directory_structure.py --dir=/path/to/project --depth=4 --output=structure.txt

# 方式2：作为模块导入使用
from your_package import directory_structure

# 生成当前目录结构并打印
print(directory_structure.generate_directory_structure())

# 生成指定目录结构并保存到文件
result = directory_structure.generate_directory_structure(
    target_dir="/path/to/project",
    max_depth=5,
    output_file="project_structure.txt"
)

'''
def generate_tree(root_path, prefix='', depth=0, max_depth=3, ignore_list=None, is_last=False):
    """
    生成格式正确的目录结构树

    参数:
    root_path -- 要生成结构的根目录路径
    prefix -- 用于格式化的前缀字符串
    depth -- 当前深度
    max_depth -- 最大遍历深度
    ignore_list -- 要忽略的目录/文件列表
    is_last -- 当前项是否是父目录的最后一项
    """
    if ignore_list is None:
        ignore_list = [".git", "__pycache__", ".pytest_cache", ".coverage",
                       ".idea", ".venv", ".gitignore", "node_modules", "dist"]

    # 获取当前项的基本名称
    name = os.path.basename(root_path)

    # 跳过忽略项
    if name in ignore_list:
        return ""

    # 当前节点显示
    output = prefix + name + '\n'

    # 检查深度限制
    if depth >= max_depth:
        return output

    # 如果是目录，递归处理子项
    if os.path.isdir(root_path):
        try:
            # 获取并排序子项，过滤忽略项和隐藏文件
            entries = sorted(os.listdir(root_path))
            entries = [e for e in entries
                       if e not in ignore_list and not e.startswith('.')]

            for i, entry in enumerate(entries):
                child_path = os.path.join(root_path, entry)
                last_entry = (i == len(entries) - 1)  # 是否是最后一项

                # 计算新的前缀
                if depth == 0:
                    # 根目录的子项
                    new_prefix = prefix + ("└── " if last_entry else "├── ")
                else:
                    # 非根目录的子项
                    connector = "    " if is_last else "│   "
                    new_prefix = prefix + connector + ("└── " if last_entry else "├── ")

                # 递归生成子树
                output += generate_tree(
                    child_path,
                    new_prefix,
                    depth + 1,
                    max_depth,
                    ignore_list,
                    last_entry
                )
        except PermissionError:
            # 无权限访问目录
            pass
        except Exception as e:
            # 其他异常处理
            output += f"{new_prefix}[Error: {str(e)}]\n"

    return output


def generate_directory_structure(target_dir=None, max_depth=3, output_file=None):
    """
    生成目录结构

    参数:
    target_dir -- 目标目录路径（如果为None，则使用当前目录的父目录）
    max_depth -- 最大遍历深度
    output_file -- 输出文件路径（如果为None，则打印到控制台）
    """
    # 确定目标目录
    if target_dir is None:
        # 默认使用当前脚本所在目录的父目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.dirname(script_dir)

    # 确保目录存在
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"目录不存在: {target_dir}")

    # 生成结构树
    tree = f"目录结构 (根目录: {os.path.abspath(target_dir)}, 最大深度: {max_depth}):\n"
    tree += generate_tree(target_dir, max_depth=max_depth)

    # 输出结果
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(tree)
        return f"结构树已保存到: {output_file}"
    else:
        return tree


def main():
    """命令行接口主函数"""
    parser = argparse.ArgumentParser(description='生成目录结构树')
    parser.add_argument("--dir", help="目标目录路径（默认：当前脚本的父目录）")
    parser.add_argument("--depth", type=int, default=3, help="最大深度（默认：3）")
    parser.add_argument("--output", help="输出文件路径（不指定则打印到控制台）")

    args = parser.parse_args()

    try:
        result = generate_directory_structure(
            target_dir=args.dir,
            max_depth=args.depth,
            output_file=args.output
        )
        print(result)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


# 作为模块使用的示例
if __name__ == "__main__":
    main()