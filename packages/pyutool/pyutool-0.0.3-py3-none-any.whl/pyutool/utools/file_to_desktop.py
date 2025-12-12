#!/usr/bin/env python3
"""
跨平台桌面快捷方式生成脚本（修复Windows KeyError问题）
支持：Windows（.lnk）、macOS（.app 替身）、Linux（.desktop）
"""
import os
import sys
import shutil
import platform
from typing import Optional, Tuple
import argparse
from pathlib import Path

# 系统类型定义
SYSTEM = platform.system()
DESKTOP_DIR = Path.home() / "Desktop"  # 桌面目录（跨平台兼容）


def validate_target_file(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    验证目标文件是否合法
    返回：(是否合法, 错误信息/None)
    """
    if not file_path.exists():
        return False, f"文件不存在：{file_path}"
    if not file_path.is_file():
        return False, f"不是有效文件：{file_path}"
    # 检查文件是否可执行（脚本/程序类文件）
    if SYSTEM in ["Windows", "Linux"] and not os.access(file_path, os.X_OK):
        print(f"⚠️ 警告：文件 {file_path} 没有可执行权限，可能无法直接运行")
    return True, None


def get_file_info(file_path: Path) -> Tuple[str, str]:
    """
    获取文件信息（用于快捷方式名称和描述）
    返回：(快捷方式名称, 文件描述)
    """
    # 快捷方式名称：默认使用文件名（去掉后缀）
    shortcut_name = file_path.stem
    # 文件描述：使用文件路径+后缀
    file_desc = f"启动 {file_path.name}"
    return shortcut_name, file_desc


def create_windows_shortcut(target_path: Path, shortcut_name: str) -> bool:
    """
    Windows 系统：创建 .lnk 快捷方式（依赖 pywin32 库）
    优化：如果是Python脚本，自动关联当前Python解释器
    """
    try:
        import win32com.client
        from win32com.shell import shell, shellcon

        # 快捷方式保存路径（桌面 + 名称.lnk）
        shortcut_path = DESKTOP_DIR / f"{shortcut_name}.lnk"
        if shortcut_path.exists():
            print(f"⚠️ 已存在同名快捷方式，将覆盖：{shortcut_path}")
            shortcut_path.unlink()

        # 创建快捷方式对象
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))

        # 特殊处理：如果是.py文件，使用当前Python解释器启动
        if target_path.suffix.lower() == ".py":
            python_exe = Path(sys.executable).resolve()
            shortcut.TargetPath = str(python_exe)  # Python解释器路径
            shortcut.Arguments = str(target_path)  # 脚本路径作为参数
            print(f"ℹ️ 检测到Python脚本，将使用：{python_exe} 启动")
        else:
            shortcut.TargetPath = str(target_path)  # 目标文件路径

        shortcut.WorkingDirectory = str(target_path.parent)  # 工作目录（目标文件所在目录）
        shortcut.Description = f"快捷方式：{target_path.name}"  # 描述
        shortcut.Save()  # 保存快捷方式

        print(f"✅ Windows 快捷方式创建成功！")
        print(f"📁 位置：{shortcut_path}")
        return True
    except ImportError:
        print("❌ 缺少依赖库：pywin32（Windows 系统创建快捷方式必需）")
        print("请先安装：pip install pywin32")
        return False
    except Exception as e:
        print(f"❌ Windows 快捷方式创建失败：{str(e)}")
        return False


def create_macos_shortcut(target_path: Path, shortcut_name: str) -> bool:
    """
    macOS 系统：创建 .app 替身（使用 AppleScript 命令）
    """
    try:
        # 快捷方式保存路径（桌面 + 名称.app）
        shortcut_path = DESKTOP_DIR / f"{shortcut_name}.app"
        if shortcut_path.exists():
            print(f"⚠️ 已存在同名快捷方式，将覆盖：{shortcut_path}")
            shutil.rmtree(shortcut_path)  # 删除原有替身

        # 使用 AppleScript 命令创建替身（macOS 原生方式）
        applescript = f'''
        tell application "Finder"
            make new alias file at POSIX file "{str(DESKTOP_DIR)}" to POSIX file "{str(target_path)}" with properties {{name:"{shortcut_name}"}}
        end tell
        '''
        # 执行 AppleScript
        result = os.system(f"osascript -e '{applescript}'")
        if result == 0:
            print(f"✅ macOS 快捷方式（替身）创建成功！")
            print(f"📁 位置：{shortcut_path}")
            return True
        else:
            raise Exception(f"AppleScript 执行失败（错误码：{result}）")
    except Exception as e:
        print(f"❌ macOS 快捷方式创建失败：{str(e)}")
        return False


def create_linux_shortcut(target_path: Path, shortcut_name: str, file_desc: str) -> bool:
    """
    Linux 系统：创建 .desktop 快捷方式（标准桌面文件格式）
    """
    try:
        # 快捷方式保存路径（桌面 + 名称.desktop）
        shortcut_path = DESKTOP_DIR / f"{shortcut_name}.desktop"
        if shortcut_path.exists():
            print(f"⚠️ 已存在同名快捷方式，将覆盖：{shortcut_path}")
            shortcut_path.unlink()

        # .desktop 文件内容（Linux 标准格式）
        desktop_content = f"""[Desktop Entry]
Name={shortcut_name}
Comment={file_desc}
Exec={str(target_path)}
Terminal=false
Type=Application
Categories=Utility;Application;
Icon=utilities-terminal  # 默认图标（可替换为自定义图标路径）
StartupNotify=true
"""
        # 写入 .desktop 文件
        with open(shortcut_path, "w", encoding="utf-8") as f:
            f.write(desktop_content)

        # 设置文件可执行权限（必需，否则无法启动）
        os.chmod(shortcut_path, 0o755)

        print(f"✅ Linux 快捷方式创建成功！")
        print(f"📁 位置：{shortcut_path}")
        return True
    except Exception as e:
        print(f"❌ Linux 快捷方式创建失败：{str(e)}")
        return False


def create_shortcut(target_path: Path, custom_name: Optional[str] = None) -> None:
    """
    主函数：根据系统类型创建对应格式的快捷方式（修复KeyError）
    """
    # 1. 验证目标文件
    valid, err_msg = validate_target_file(target_path)
    if not valid:
        print(f"❌ {err_msg}")
        sys.exit(1)
    print(f"✅ 验证通过，目标文件：{target_path}")

    # 2. 获取快捷方式名称和描述
    default_name, file_desc = get_file_info(target_path)
    shortcut_name = custom_name if custom_name else default_name
    print(f"📌 快捷方式名称：{shortcut_name}")

    # 3. 根据系统类型创建快捷方式
    print(f"🖥️  检测到系统：{SYSTEM}")
    success = False
    suffix = ""  # 快捷方式后缀
    if SYSTEM == "Windows":
        success = create_windows_shortcut(target_path, shortcut_name)
        suffix = ".lnk"
    elif SYSTEM == "Darwin":  # Darwin 是 macOS 的系统名称
        success = create_macos_shortcut(target_path, shortcut_name)
        suffix = ".app"
    elif SYSTEM == "Linux":
        success = create_linux_shortcut(target_path, shortcut_name, file_desc)
        suffix = ".desktop"
    else:
        print(f"❌ 不支持的系统：{SYSTEM}")
        sys.exit(1)

    # 4. 结果总结（修复KeyError：直接根据系统设置后缀）
    if success:
        final_path = DESKTOP_DIR / (shortcut_name + suffix)
        print(f"\n🎉 快捷方式已成功创建到桌面！")
        print(f"👉 路径：{final_path}")
    else:
        print(f"\n❌ 快捷方式创建失败，请检查上述错误信息")
        sys.exit(1)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="跨平台桌面快捷方式生成脚本")
    parser.add_argument(
        "-p", "--path",
        required=False,
        help="目标文件路径（如：C:/test.exe 或 /Users/test.py），不指定则手动输入"
    )
    parser.add_argument(
        "-n", "--name",
        required=False,
        help="快捷方式自定义名称（默认使用目标文件的文件名）"
    )
    args = parser.parse_args()

    # 1. 获取目标文件路径（命令行参数或手动输入）
    if args.path:
        target_path = Path(args.path).resolve()
    else:
        print("📥 请输入目标文件的完整路径（示例：")
        print("  Windows：C:\\Program Files\\Notepad++.exe 或 D:\\code\\script.py")
        print("  macOS/Linux：/Applications/WeChat.app 或 ~/code/script.sh）")
        target_path_str = input("文件路径：").strip()
        # 处理 ~ 路径（macOS/Linux）
        if target_path_str.startswith("~"):
            target_path_str = os.path.expanduser(target_path_str)
        target_path = Path(target_path_str).resolve()

    # 2. 执行创建快捷方式
    create_shortcut(target_path, args.name)


if __name__ == "__main__":
    main()