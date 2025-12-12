'''
一个密码本管理系统
核心逻辑(密码本逻辑):pyutool.umodules.password.password_book_editor.py
配置文件：D:\__ALL__\coding\configs\config.cfg
密码本路径：D:\__ALL__\coding\configs\book.dark
密码本格式就是.dark不要是json 不要有生成秘钥
最后 请给我完整的代码 (假如一次发得完整个模块时)
核心功能：...
'''

import os
import configparser
from typing import List, Tuple, Dict, Any, Optional
import tkinter.messagebox as messagebox

from pyutool import _open, check_path, CheckLevel, check_encoding


class PassWordBook:
    """密码本核心类（明文存储），管理密码文件的增删改查"""

    def __init__(self, password_file_path, config_path, encoding='utf-8'):
        check_encoding(encoding, CheckLevel.ASSERT)
        self.encoding = encoding
        self.config_path = config_path
        self.password_file_path = password_file_path  # 密码本路径
        self.show_password_when_adding = False
        self.show_password_when_viewing = False
        self._temp_accounts = []  # 用于导入功能的临时账号存储
        self.data = {}  # 内存数据存储

        # 加载配置（若存在）
        self._load_config()
        # 确保密码文件存在
        self._ensure_file_exists()

    def _load_config(self):
        """加载配置文件，处理显示密码相关设置"""
        if not os.path.exists(self.config_path):
            return

        cp = configparser.ConfigParser()
        try:
            cp.read(self.config_path, encoding=self.encoding)
        except Exception as e:
            print(f"配置文件损坏，使用默认配置：{e}")
            self._reset_config()  # 配置损坏时重置
            return

        if 'Settings' in cp:
            # 处理布尔值配置（非布尔值用默认）
            self.show_password_when_adding = self._str_to_bool(
                cp['Settings'].get('show_password_when_adding', 'False')
            )
            self.show_password_when_viewing = self._str_to_bool(
                cp['Settings'].get('show_password_when_viewing', 'False')
            )
            # 处理密码文件路径（无效路径用初始化时的路径）
            pwd_path = cp['Settings'].get('password_file_path', self.password_file_path)
            self.password_file_path = pwd_path if os.path.isfile(pwd_path) else self.password_file_path

    def _reset_config(self):
        """重置并保存默认配置"""
        try:
            cp = configparser.ConfigParser()
            cp['Settings'] = {
                'show_password_when_adding': str(self.show_password_when_adding),
                'show_password_when_viewing': str(self.show_password_when_viewing),
                'password_file_path': self.password_file_path
            }
            with _open(self.config_path, 'w', encoding=self.encoding) as f:
                cp.write(f)
        except Exception as e:
            print(f"重置配置文件失败：{e}")

    def _str_to_bool(self, s):
        s = s.lower()
        return s == 'true' if s in ['true', 'false'] else False

    # region 基础工具方法

    def _is_account(self, line: str) -> bool:
        return line.strip().startswith("-account:")

    def _is_password(self, line: str) -> bool:
        return line.strip().startswith("-password:")

    def _is_url_platform(self, line: str) -> bool:
        return line.strip().lower().startswith("url_platform:")

    def _is_remark(self, line: str) -> bool:
        return line.strip().startswith("-remark:")

    def _extract_value(self, line: str, prefix: str) -> Optional[str]:
        line_stripped = line.strip()
        if line_stripped.startswith(prefix):
            value = line_stripped[len(prefix):].strip()
            return value if value else None
        return None

    # endregion

    # region 平台相关方法
    def _url_platform_exists(self, url_platform: str) -> bool:
        return url_platform.strip() in [p.strip() for p in self.get_all_url_platform()]

    def get_url_platform_line(self, url_platform: str) -> int:
        lines = self._read_lines()
        for line_num, line in enumerate(lines, 1):
            plat = self._extract_value(line, "url_platform:")
            if plat and plat.strip() == url_platform.strip():
                return line_num
        return -1

    def get_all_url_platform(self) -> List[str]:
        platforms = []
        lines = self._read_lines()
        print("正在解析平台...")
        for line in lines:
            if line.lower().startswith("url_platform:"):
                platform = line.split("url_platform:")[-1].strip()
                if platform and platform not in platforms:
                    platforms.append(platform)
                    print(f"找到平台：{platform}")
        print(f"最终识别到 {len(platforms)} 个平台：{platforms}")
        return platforms

    # endregion

    # region 账号相关方法
    def get_all_item(self, url_platform: str) -> Tuple[Dict, int]:
        items = {"url_platform": url_platform, "items": []}
        lines = self._read_lines()
        in_target = False
        current_acc = None
        current_pwd = None
        current_remark = "无备注"
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.lower().startswith("url_platform:"):
                current_plat = line_stripped.split("url_platform:")[-1].strip()
                if current_acc is not None and current_pwd is not None:
                    items["items"].append({
                        "account": current_acc,
                        "password": current_pwd,
                        "remark": current_remark
                    })
                in_target = (current_plat == url_platform.strip())
                current_acc = None
                current_pwd = None
                current_remark = "无备注"
                continue
            if not in_target:
                continue
            if line_stripped.startswith("-account:"):
                if current_acc is not None and current_pwd is not None:
                    items["items"].append({
                        "account": current_acc,
                        "password": current_pwd,
                        "remark": current_remark
                    })
                current_acc = line_stripped.split("-account:")[-1].strip() or ""
                current_pwd = None
                current_remark = "无备注"
            elif line_stripped.startswith("-password:") and current_acc is not None:
                current_pwd = line_stripped.split("-password:")[-1].strip() or ""
            elif line_stripped.startswith("-remark:") and current_acc is not None:
                current_remark = line_stripped.split("-remark:")[-1].strip() or "无备注"
        if current_acc is not None and current_pwd is not None:
            items["items"].append({
                "account": current_acc,
                "password": current_pwd,
                "remark": current_remark
            })
        print(f"平台「{url_platform}」下共找到 {len(items['items'])} 个账号")
        return items, len(items["items"])

    def get_items_len(self, url_platform: str) -> int:
        return self.get_all_item(url_platform)[1]

    def account_exists(self, url_platform: str, account: str) -> bool:
        items, _ = self.get_all_item(url_platform)
        return any(item["account"].strip() == account.strip() for item in items["items"])

    # endregion

    # region 核心操作功能（增删改）

    def add_account(self, url_platform: str, account: str, password: str, remark: str = "") -> None:
        url_platform_stripped = url_platform.strip()
        account_stripped = account.strip()
        password_stripped = password.strip()
        if not self._url_platform_exists(url_platform_stripped):
            raise ValueError(f"平台「{url_platform_stripped}」不存在")
        if self.account_exists(url_platform_stripped, account_stripped):
            raise ValueError(f"平台「{url_platform_stripped}」下账号「{account_stripped}」已存在")
        if not account_stripped:
            raise ValueError("账号不能为空")
        if not password_stripped:
            raise ValueError("密码不能为空")
        # 明文存储，直接使用原始密码
        new_lines = [
            f"-account:{account_stripped}",
            f"-password:{password_stripped}",
            f"-remark:{remark.strip() or '无备注'}",
            ""
        ]
        all_lines = self._read_lines()
        platform_line_idx = self.get_url_platform_line(url_platform_stripped) - 1
        if platform_line_idx == -1:
            raise ValueError(f"平台「{url_platform_stripped}」不存在")
        insert_pos = platform_line_idx + 1
        while insert_pos < len(all_lines):
            line_stripped = all_lines[insert_pos].strip()
            if line_stripped.lower().startswith("url_platform:"):
                break
            insert_pos += 1
        all_lines[insert_pos:insert_pos] = new_lines
        self._write_lines(all_lines)

    def update_remark(self, url_platform: str, account: str, new_remark: str) -> None:
        url_platform_stripped = url_platform.strip()
        account_stripped = account.strip()
        if not self._url_platform_exists(url_platform_stripped):
            raise ValueError(f"平台「{url_platform_stripped}」不存在")
        if not self.account_exists(url_platform_stripped, account_stripped):
            raise ValueError(f"账号「{account_stripped}」不存在")
        lines = self._read_lines()
        new_lines = []
        in_target_platform = False
        editing_target_account = False
        has_written_new_remark = False
        found_password = False
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.lower().startswith("url_platform:"):
                current_platform = line_stripped.split("url_platform:")[-1].strip()
                in_target_platform = (current_platform == url_platform_stripped)
                editing_target_account = False
                has_written_new_remark = False
                found_password = False
                new_lines.append(line)
                continue
            if in_target_platform:
                if self._is_account(line_stripped) and self._extract_value(line_stripped,
                                                                           "-account:").strip() == account_stripped:
                    new_lines.append(line)
                    editing_target_account = True
                    has_written_new_remark = False
                    found_password = False
                    continue
                if editing_target_account and self._is_password(line_stripped):
                    new_lines.append(line)
                    found_password = True
                    continue
                if editing_target_account and found_password and not has_written_new_remark:
                    new_remark_str = new_remark.strip() or "无备注"
                    new_lines.append(f"-remark:{new_remark_str}")
                    has_written_new_remark = True
                    editing_target_account = False
                    if self._is_remark(line_stripped):
                        continue
                if editing_target_account and self._is_remark(line_stripped):
                    continue
            new_lines.append(line)
        if in_target_platform and editing_target_account and found_password and not has_written_new_remark:
            new_remark_str = new_remark.strip() or "无备注"
            new_lines.append(f"-remark:{new_remark_str}")
        self._write_lines(new_lines)

    def update_account(self, url_platform: str, old_account: str, new_account: Optional[str] = None,
                       new_password: Optional[str] = None) -> None:
        url_platform_stripped = url_platform.strip()
        old_account_stripped = old_account.strip()
        if not new_account and not new_password:
            raise ValueError("必须传入新账号名或新密码")
        if not self._url_platform_exists(url_platform_stripped):
            raise ValueError(f"平台「{url_platform_stripped}」不存在")
        if not self.account_exists(url_platform_stripped, old_account_stripped):
            raise ValueError(f"账号「{old_account_stripped}」不存在")
        if new_password is not None and not new_password.strip():
            raise ValueError("新密码不能为空")
        if new_account:
            new_account_stripped = new_account.strip()
            if new_account_stripped != old_account_stripped and self.account_exists(url_platform_stripped,
                                                                                    new_account_stripped):
                raise ValueError(f"新账号「{new_account_stripped}」已存在")
        lines = self._read_lines()
        new_lines = []
        in_target_platform = False
        editing_target_account = False

        for line in lines:
            line_stripped = line.strip()
            if line_stripped.lower().startswith("url_platform:"):
                current_platform = line_stripped.split("url_platform:")[-1].strip()
                in_target_platform = (current_platform == url_platform_stripped)
                editing_target_account = False
                new_lines.append(line)
                continue

            if in_target_platform:
                if self._is_account(line_stripped) and self._extract_value(line_stripped,
                                                                           "-account:").strip() == old_account_stripped:
                    editing_target_account = True
                    if new_account:
                        new_lines.append(f"-account:{new_account.strip()}")
                    else:
                        new_lines.append(line)
                    continue

                if editing_target_account and self._is_password(line_stripped):
                    if new_password:
                        # 明文存储，直接使用新密码
                        new_lines.append(f"-password:{new_password.strip()}")
                    else:
                        new_lines.append(line)
                    editing_target_account = False
                    continue

            new_lines.append(line)

        self._write_lines(new_lines)

    def _save_temp_account(self, platform: str, account: str, password: str, remark: str = ""):
        """临时保存导入的账号信息"""
        self._temp_accounts.append({
            "platform": platform.strip(),
            "account": account.strip(),
            "password": password.strip(),
            "remark": remark.strip()
        })

    def save_imported_accounts(self):
        """保存临时存储的导入账号"""
        platforms_added = set()
        for item in self._temp_accounts:
            platform = item["platform"]
            if not platform:
                continue
            if platform not in platforms_added and not self._url_platform_exists(platform):
                self.add_platform(
                    url_platform=platform,
                    account=item["account"],
                    password=item["password"],
                    remark=item["remark"]
                )
                platforms_added.add(platform)
            elif self._url_platform_exists(platform) and not self.account_exists(platform, item["account"]):
                self.add_account(
                    url_platform=platform,
                    account=item["account"],
                    password=item["password"],
                    remark=item["remark"]
                )
        self._temp_accounts.clear()  # 清空临时数据

    def get_config(self) -> Dict[str, Any]:
        """获取当前配置信息"""
        return {
            "show_password_when_adding": self.show_password_when_adding,
            "show_password_when_viewing": self.show_password_when_viewing,
            "password_file_path": self.password_file_path
        }

    def save_config(self) -> None:
        """保存配置到文件"""
        try:
            cp = configparser.ConfigParser()
            cp['Settings'] = {
                'show_password_when_adding': str(self.show_password_when_adding),
                'show_password_when_viewing': str(self.show_password_when_viewing),
                'password_file_path': self.password_file_path
            }
            with _open(self.config_path, 'w', encoding=self.encoding) as f:
                cp.write(f)
        except Exception as e:
            print(f"保存配置失败：{e}")
            messagebox.showerror("错误", f"保存配置失败：{str(e)}")

    def delete_platform(self, url_platform: str) -> None:
        """删除指定平台及其所有账号"""
        url_platform_stripped = url_platform.strip()
        if not self._url_platform_exists(url_platform_stripped):
            raise ValueError(f"平台「{url_platform_stripped}」不存在")

        lines = self._read_lines()
        new_lines = []
        skip = False

        for line in lines:
            line_stripped = line.strip()
            if line_stripped.lower().startswith("url_platform:"):
                current_platform = line_stripped.split("url_platform:")[-1].strip()
                skip = (current_platform == url_platform_stripped)

            if not skip:
                new_lines.append(line)
            else:
                # 遇到下一个平台时停止跳过
                if line_stripped.lower().startswith("url_platform:") and line_stripped != line_stripped:
                    skip = False
                    new_lines.append(line)

        self._write_lines(new_lines)

    def delete_account(self, url_platform: str, account: str) -> None:
        """删除指定平台下的账号"""
        url_platform_stripped = url_platform.strip()
        account_stripped = account.strip()

        if not self._url_platform_exists(url_platform_stripped):
            raise ValueError(f"平台「{url_platform_stripped}」不存在")
        if not self.account_exists(url_platform_stripped, account_stripped):
            raise ValueError(f"账号「{account_stripped}」不存在")

        lines = self._read_lines()
        new_lines = []
        in_target_platform = False
        deleting = False

        for line in lines:
            line_stripped = line.strip()

            if line_stripped.lower().startswith("url_platform:"):
                current_platform = line_stripped.split("url_platform:")[-1].strip()
                in_target_platform = (current_platform == url_platform_stripped)
                deleting = False
                new_lines.append(line)
                continue

            if in_target_platform:
                if self._is_account(line_stripped) and self._extract_value(line_stripped,
                                                                           "-account:").strip() == account_stripped:
                    deleting = True
                    continue

                if deleting:
                    if line_stripped.lower().startswith("url_platform:") or (self._is_account(line_stripped)):
                        deleting = False
                        new_lines.append(line)
                    continue

            new_lines.append(line)

        self._write_lines(new_lines)

    def clear_all(self, confirm: bool = False):
        """清空所有内容，添加确认机制"""
        if not confirm:
            raise ValueError("请确认清空操作")
        self.data = {}
        self._write_lines([])  # 写入空内容清空文件

    def import_plaintext_data(self, file_path: str):
        """导入明文数据（每行格式：平台名,账号,密码,备注）"""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]  # 跳过空行

        for line in lines:
            try:
                platform, account, password, remark = line.split(',', 3)  # 分割为4部分
            except ValueError:
                continue  # 跳过格式错误行

            # 检查账号是否已存在
            if platform in self.data and account in self.data[platform]:
                continue  # 跳过重复账号

            # 明文存储，直接保存原始密码
            if platform not in self.data:
                self.data[platform] = {}
            self.data[platform][account] = {
                'password': password,
                'remark': remark
            }

        # 将内存数据同步到文件
        self._sync_data_to_file()

    def _sync_data_to_file(self):
        """将内存数据同步到文件"""
        lines = []
        for platform, accounts in self.data.items():
            lines.append(f"url_platform:{platform}")
            for account, info in accounts.items():
                lines.append(f"-account:{account}")
                lines.append(f"-password:{info['password']}")
                lines.append(f"-remark:{info['remark'] or '无备注'}")
                lines.append("")  # 账号间空行分隔
        self._write_lines(lines)

    def add_platform(self, url_platform: str, account: str, password: str, remark: str = "") -> None:
        url_platform_stripped = url_platform.strip()
        if self._url_platform_exists(url_platform_stripped):
            raise ValueError(f"平台「{url_platform_stripped}」已存在")
        if not url_platform_stripped:
            raise ValueError("平台名不能为空")
        if not account.strip():
            raise ValueError("初始账号不能为空")
        if not password.strip():
            raise ValueError("初始密码不能为空")
        # 移除末尾的空行，由 _write_lines 自动处理空行分隔
        lines = [
            f"url_platform:{url_platform_stripped}",
            f"-account:{account.strip()}",
            f"-password:{password.strip()}",
            f"-remark:{remark.strip() or '无备注'}"
        ]
        self._append_lines(lines)

    def _write_lines(self, lines: List[str]) -> None:
        valid_lines = []
        last_empty = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if not last_empty:
                    valid_lines.append("")
                    last_empty = True
            else:
                valid_lines.append(line.rstrip('\n'))
                last_empty = False
        data = "\n".join(valid_lines) if valid_lines else ""
        try:
            with _open(self.password_file_path, 'w', encoding=self.encoding) as f:
                f.write(data)
        except Exception as e:
            print(f"写入文件失败：{e}")
            messagebox.showerror("错误", f"写入密码本失败：{str(e)}")

    def _append_lines(self, lines: List[str]) -> None:
        try:  # 添加异常捕获
            current_lines = self._read_lines()
            current_lines.extend(lines)
            self._write_lines(current_lines)
        except Exception as e:
            print(f"追加内容失败：{str(e)}")
            raise  # 重新抛出异常

    def _read_lines(self) -> List[str]:
        """读取文件内容（明文，无需解密）"""
        if not check_path(self.password_file_path, True, CheckLevel.BOOL):
            return []
        try:
            with _open(self.password_file_path, 'r', encoding=self.encoding) as f:
                content = f.read()
            # 处理空文件，直接返回空列表
            if not content:
                lines = []
            else:
                lines = [line.rstrip('\n') for line in content.split("\n")]
            print(f"读取成功，共读取 {len(lines)} 行数据")
            return lines
        except Exception as e:
            print(f"读取失败：{str(e)}")
            messagebox.showerror("错误", f"读取密码本失败：{str(e)}")
            return []

    def _ensure_file_exists(self) -> None:
        """确保密码文件存在（不存在则创建空文件）"""
        if not check_path(self.password_file_path, True, CheckLevel.BOOL):
            parent_dir = os.path.dirname(self.password_file_path)
            if not check_path(parent_dir, True, CheckLevel.BOOL):
                os.makedirs(parent_dir, exist_ok=True)
            # 创建空文件，不写入任何内容
            with _open(self.password_file_path, 'w', encoding=self.encoding) as f:
                pass  # 仅创建文件，不写入内容
        # 移除文件为空时的写入操作，避免添加空行