import os
import argparse
import sys


def find_project_root(start_path=None):
    """自动检测项目根目录"""
    if start_path is None:
        start_path = os.path.abspath(os.path.dirname(__file__))

    current = start_path
    while True:
        markers = [
            "password_book_editor.py", "README.md", ".git", "requirements.txt",
            "pyproject.toml", "setup.py"
        ]
        if any(os.path.exists(os.path.join(current, marker)) for marker in markers):
            return current

        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    return os.path.dirname(os.path.dirname(start_path))


def generate_tree(path, prefix='', depth=0, max_depth=3, ignore_list=None, is_last=False):
    """生成格式正确的项目结构树"""
    if ignore_list is None:
        ignore_list = [
            ".git", "__pycache__", ".pytest_cache",
            ".coverage", ".idea", ".venv", "htmlcov",
            ".coverage.*", "coverage.xml", ".coveragerc"
        ]

    # 特别允许显示的资源目录（以点开头）
    allowed_dot_dirs = {'.text', '.music', '.ttf', '.logs', '.ico', '.ini'}

    current_name = os.path.basename(path)
    if current_name in ignore_list or any(current_name.startswith(ig) for ig in ignore_list):
        return ""

    name = os.path.basename(path) if depth > 0 or path != project_root else '.'
    output = prefix + name + '\n'

    if depth >= max_depth:
        return output

    if os.path.isdir(path):
        try:
            # 获取目录内容，应用忽略规则但保留允许的点开头目录
            entries = []
            for e in sorted(os.listdir(path)):
                # 允许点开头目录中的特定资源目录
                if e in allowed_dot_dirs:
                    entries.append(e)
                # 普通文件/目录：忽略点开头文件但保留其他
                elif not e.startswith('.') and e not in ignore_list:
                    entries.append(e)

            for i, entry in enumerate(entries):
                child_path = os.path.join(path, entry)
                last_entry = (i == len(entries) - 1)

                if depth == 0:
                    new_prefix = prefix + ("└── " if last_entry else "├── ")
                else:
                    new_prefix = prefix + ("    " if is_last else "│   ") + ("└── " if last_entry else "├── ")

                output += generate_tree(
                    child_path,
                    new_prefix,
                    depth + 1,
                    max_depth,
                    ignore_list,
                    last_entry
                )
        except PermissionError:
            pass
        except Exception as e:
            output += f"{new_prefix}[Error: {str(e)}]\n"

    return output


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    global project_root
    project_root = find_project_root(script_dir)

    parser = argparse.ArgumentParser(description='生成项目结构树')
    parser.add_argument("--dir", default=project_root, help="项目根目录")
    parser.add_argument("--depth", type=int, default=3, help="最大深度")
    parser.add_argument("--output", help="输出到文件")
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        print(f"错误: 目录不存在 {args.dir}")
        sys.exit(1)

    tree = f"项目结构 (根目录: {os.path.basename(args.dir)}, 最大深度: {args.depth}):\n"
    tree += generate_tree(args.dir, max_depth=args.depth)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(tree)
        print(f"结构树已保存到: {args.output}")
    else:
        print(tree)


if __name__ == "__main__":
    main()
    # print(__file__)