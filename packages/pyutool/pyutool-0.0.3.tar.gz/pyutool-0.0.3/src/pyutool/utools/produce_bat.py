import os
import sys
import subprocess


def create_bat_and_shortcut(file_path):
    # 处理路径，去除可能的双引号
    file_path = file_path.strip('"').strip("'")

    # 获取桌面路径
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

    # 获取文件名（不含扩展名）
    filename = os.path.splitext(os.path.basename(file_path))[0]

    # 创建BAT文件
    bat_path = os.path.join(desktop, f"{filename}.bat")
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(f'@echo off\n"{file_path}"\npause')

    # 创建快捷方式 (使用 VBScript)
    vbs_content = f'''
    Set ws = WScript.CreateObject("WScript.Shell")
    Set link = ws.CreateShortcut("{desktop}\\{filename}.lnk")
    link.TargetPath = "{file_path}"
    link.WorkingDirectory = "{os.path.dirname(file_path)}"
    link.Save
    '''

    # 创建临时vbs文件
    vbs_path = os.path.join(desktop, "temp_create_shortcut.vbs")
    with open(vbs_path, 'w', encoding='utf-8') as f:
        f.write(vbs_content)

    # 执行vbs脚本
    subprocess.run(['cscript', '//Nologo', vbs_path])

    # 删除临时vbs文件
    os.remove(vbs_path)

    print(f"BAT文件已创建：{bat_path}")
    print(f"快捷方式已创建：{desktop}\\{filename}.lnk")


def main():
    # 检查是否有参数传入
    if len(sys.argv) < 2:
        # 如果没有参数，提示用户输入
        file_path = input("请输入文件完整路径：").strip()
        if not file_path:
            print("未输入路径，程序退出")
            return
    else:
        # 如果有参数，使用第一个参数
        file_path = sys.argv[1]

    create_bat_and_shortcut(file_path)

    input("操作完成，按任意键退出...")


if __name__ == "__main__":
    main()
