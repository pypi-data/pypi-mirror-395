# 模块结构：包含键盘处理、配置管理、国际化、颜色控制、菜单项、菜单类型、命令行工具等 7 大核心类，以及对外接口函数。
# 关键功能：
# 跨平台键盘输入（支持特殊键如箭头键、Esc 等）
# 多语言支持（中文 / 英文切换）
# 丰富的文本打印模式（普通 / 交互式 / 彩虹 / 段落）
# 两种菜单交互方式（箭头键选择 / 数字输入选择）
# 可自定义的颜色和样式配置
# 进度条、倒计时、键定义、双环境支持(命令行、pygame(可暂不实现省略具体逻辑))


import os
import sys
import time
import random
import textwrap
import msvcrt
from typing import List, Callable, Optional, Dict, Any, Tuple
from colorama import init, Fore, Back, Style

# 初始化colorama库，实现跨平台的终端颜色输出
init(autoreset=True)

# 只在非Windows系统导入termios和tty模块
if os.name != 'nt':
    import termios
    import tty

# 环境常量
ENV_COMMAND_LINE = "0"
ENV_PYGAME = "1"

# 颜色名称映射表
COLOR_NAMES = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "bright_red": Fore.LIGHTRED_EX,
    "bright_green": Fore.LIGHTGREEN_EX,
    "bright_yellow": Fore.LIGHTYELLOW_EX,
    "bright_blue": Fore.LIGHTBLUE_EX,
    "bright_magenta": Fore.LIGHTMAGENTA_EX,
    "bright_cyan": Fore.LIGHTCYAN_EX,
    "bright_white": Fore.LIGHTWHITE_EX,
    "orange": Fore.LIGHTYELLOW_EX,  # 用亮黄色模拟橙色
    "purple": Fore.MAGENTA
}

# 背景颜色映射表
BACKGROUND_COLORS = {
    "black": Back.BLACK,
    "red": Back.RED,
    "green": Back.GREEN,
    "yellow": Back.YELLOW,
    "blue": Back.BLUE,
    "magenta": Back.MAGENTA,
    "cyan": Back.CYAN,
    "white": Back.WHITE
}

# 样式映射表
STYLES = {
    "normal": Style.NORMAL,
    "bright": Style.BRIGHT,
    "dim": Style.DIM
}


# 打印模式枚举类
class PrintMode:
    NORMAL = "normal"  # 普通打印
    INTERACTIVE = "interactive"  # 交互式打印（按回车继续）
    RAINBOW = "rainbow"  # 彩虹色打印
    PARAGRAPH = "paragraph"  # 段落式打印
    TYPEWRITER = "typewriter"  # 打字机效果
    RANDOM_LINE = "random_line"  # 整行随机颜色
    RANDOM_CHAR = "random_char"  # 每个字符随机颜色
    ENHANCED_TYPEWRITER = "enhanced_typewriter"  # 增强版打字机效果（支持加速）


# 键盘按键常量定义
class KeyboardKeys:
    ESC = "\x1b"
    ENTER = "\r"
    BACKSPACE = "\x08"
    TAB = "\t"
    SPACE = " "
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


# 键盘输入处理类（跨平台兼容）
class KeyBoard:
    ANSI_PREFIX = "\x1b["
    UP_ANSI = f"{ANSI_PREFIX}A"
    DOWN_ANSI = f"{ANSI_PREFIX}B"
    RIGHT_ANSI = f"{ANSI_PREFIX}C"
    LEFT_ANSI = f"{ANSI_PREFIX}D"

    KEY_MAP = {
        KeyboardKeys.ESC: "esc",
        KeyboardKeys.ENTER: "enter",
        KeyboardKeys.BACKSPACE: "backspace",
        KeyboardKeys.TAB: "tab",
        KeyboardKeys.SPACE: "space"
    }

    @classmethod
    def get_key(cls, block: bool = False) -> Optional[str]:
        """获取按键，block=True时会阻塞等待按键"""
        while True:
            if cls._kbhit():
                # 读取原始字节（不解码）
                first_byte = cls._getch()

                # Windows系统特殊键处理
                if os.name == 'nt' and first_byte == b'\xe0':
                    # Windows系统特殊键（箭头键等）
                    second_byte = cls._getch()
                    arrow_map = {
                        b'H': KeyboardKeys.UP,
                        b'P': KeyboardKeys.DOWN,
                        b'K': KeyboardKeys.LEFT,
                        b'M': KeyboardKeys.RIGHT
                    }
                    if second_byte in arrow_map:
                        return arrow_map[second_byte]
                    return None

                # Unix系统特殊键处理
                if first_byte == b'\x1b':  # ESC的字节码
                    if cls._kbhit():
                        second_byte = cls._getch()
                        if second_byte == b'[':  # ANSI转义序列的第二个字节
                            if cls._kbhit():
                                third_byte = cls._getch()
                                # 直接通过字节判断箭头方向
                                arrow_map = {
                                    b'A': KeyboardKeys.UP,
                                    b'B': KeyboardKeys.DOWN,
                                    b'C': KeyboardKeys.RIGHT,
                                    b'D': KeyboardKeys.LEFT
                                }
                                if third_byte in arrow_map:
                                    return arrow_map[third_byte]
                    return KeyboardKeys.ESC  # 单独的ESC键

                # 处理Enter键
                if first_byte in [b'\r', b'\n']:
                    return KeyboardKeys.ENTER

                # 处理可打印字符
                try:
                    key = first_byte.decode("utf-8")
                    if key.isprintable():
                        return key.lower()
                except UnicodeDecodeError:
                    pass

                return cls.KEY_MAP.get(first_byte.decode("utf-8", errors="ignore"))

            if not block:
                return None
            time.sleep(0.01)

    @classmethod
    def flush(cls) -> None:
        """清空键盘缓冲区"""
        while cls._kbhit():
            cls._getch()

    @classmethod
    def _kbhit(cls) -> bool:
        """检测是否有按键按下（跨平台实现）"""
        if os.name == 'nt':  # Windows系统
            return msvcrt.kbhit()
        else:  # Unix/Linux/macOS系统
            fd = sys.stdin.fileno()
            old_attr = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                import select
                return select.select([sys.stdin], [], [], 0)[0] != []
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_attr)

    @classmethod
    def _getch(cls) -> bytes:
        """读取单个按键（不等待回车，跨平台实现）"""
        if os.name == 'nt':  # Windows系统
            return msvcrt.getch()
        else:  # Unix/Linux/macOS系统
            fd = sys.stdin.fileno()
            old_attr = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1).encode()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_attr)

    @classmethod
    def get_key_with_buffer(cls, buffer_time: float = 0.1) -> Optional[str]:
        """带缓冲的按键获取，避免绘制过程中按键被立即处理"""
        start_time = time.time()
        key = None
        while time.time() - start_time < buffer_time:
            if cls._kbhit():
                key = cls.get_key(block=False)
                if key:
                    break
            time.sleep(0.01)
        return key


# 配置管理类
class ConfigManager:
    def __init__(self, config_path: str = "config.ini"):
        self.config_path = config_path
        self.environment = self._get_environment()
        self.language = self._get_language()

    def _get_environment(self) -> str:
        try:
            return os.getenv("CLI_ENV", ENV_COMMAND_LINE)
        except Exception:
            return ENV_COMMAND_LINE

    def _get_language(self) -> str:
        try:
            return os.getenv("CLI_LANG", "zh")
        except Exception:
            return "zh"

    def set_environment(self, env: str) -> None:
        """设置环境"""
        if env in [ENV_COMMAND_LINE, ENV_PYGAME]:
            os.environ["CLI_ENV"] = env
            self.environment = env

    def set_language(self, lang: str) -> None:
        """设置语言"""
        if lang in ["zh", "en"]:
            os.environ["CLI_LANG"] = lang
            self.language = lang


# 国际化管理类
class I18nManager:
    def __init__(self, language: str = "zh"):
        self.language = language
        self.translations = self._load_translations()

    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        return {
            "zh": {
                "按Enter键返回主菜单...": "按Enter键返回主菜单...",
                "进度": "进度",
                "剩余": "剩余",
                "倒计时": "倒计时",
                "完成！": "完成！",
                "菜单无选项": "菜单无选项",
                "按回车继续...": "按回车继续...",
                "Esc返回主菜单  ↑↓切换  Enter选择": "Esc返回主菜单  ↑↓切换  Enter选择",
                "请输入选项编号:": "请输入选项编号:",
                "上下箭头选择菜单项": "上下箭头选择菜单项",
                "按数字键选择菜单项": "按数字键选择菜单项",
                "按任意键继续...": "按任意键继续...",
                "确认删除? (y/n)": "确认删除? (y/n)",
                "已删除": "已删除",
                "取消删除": "取消删除"
            },
            "en": {
                "按Enter键返回主菜单...": "Press Enter to return to main menu...",
                "进度": "Progress",
                "剩余": "Remaining",
                "倒计时": "Countdown",
                "完成！": "Completed!",
                "菜单无选项": "Menu has no options",
                "按回车继续...": "Press Enter to continue...",
                "Esc返回主菜单  ↑↓切换  Enter选择": "Esc return to main menu  ↑↓ to switch  Enter to select",
                "请输入选项编号:": "Please enter option number:",
                "上下箭头选择菜单项": "Use arrow keys to select menu items",
                "按数字键选择菜单项": "Press number keys to select menu items",
                "按任意键继续...": "Press any key to continue...",
                "确认删除? (y/n)": "Confirm deletion? (y/n)",
                "已删除": "Deleted",
                "取消删除": "Deletion cancelled"
            }
        }

    def gettext(self, text: str) -> str:
        return self.translations.get(self.language, {}).get(text, text)


# 文本渲染类
class TextRenderer:
    """文本渲染类，处理不同环境下的文本渲染"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.rainbow_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        self.all_colors = list(COLOR_NAMES.keys())
        self.pygame_initialized = False
        self.screen = None

    def _init_pygame(self) -> None:
        """初始化Pygame环境（仅在需要时）"""
        if not self.pygame_initialized and self.config.environment == ENV_PYGAME:
            try:
                import pygame
                pygame.init()
                self.screen = pygame.display.set_mode((800, 600))
                pygame.display.set_caption("CLI Utils Pygame Environment")
                self.pygame_initialized = True
            except ImportError:
                print("Pygame not installed, falling back to command line environment")
                self.config.set_environment(ENV_COMMAND_LINE)

    def render_cli(self, text: str, color: str = 'white', back: str = 'black',
                   style: str = 'normal', end: str = '\n', **kwargs) -> None:
        """命令行环境文本渲染"""
        # 获取颜色和样式
        fore_color = COLOR_NAMES.get(color.lower(), Fore.WHITE)
        back_color = BACKGROUND_COLORS.get(back.lower(), Back.BLACK)
        text_style = STYLES.get(style.lower(), Style.NORMAL)

        # 移除通用打印语句（避免重复）
        # 确保颜色在打印时生效 - 原重复打印位置

        # 获取打印模式和参数
        mode = kwargs.get('mode', PrintMode.NORMAL)
        delay = kwargs.get('delay', True)
        wait_time = kwargs.get('wait_time', 0.05)
        lines_per_pause = kwargs.get('lines_per_pause', 5)
        para_length = kwargs.get('para_length', 80)

        # 所有模式的打印末尾统一处理end参数（移至各模式内部）
        # 原重复的end处理语句

        # 应用延迟（优化部分）
        if delay and wait_time > 0:
            if mode not in [PrintMode.RAINBOW, PrintMode.TYPEWRITER, PrintMode.RANDOM_CHAR]:
                time.sleep(wait_time)

        if mode == PrintMode.NORMAL:
            # 仅在NORMAL模式下打印一次
            print(f"{fore_color}{back_color}{text_style}{text}{Style.RESET_ALL}", end=end, flush=True)

        elif mode == PrintMode.INTERACTIVE:
            # 等待用户按回车才继续
            KeyBoard.get_key(block=True)
            print(f"{fore_color}{back_color}{text_style}{text}{Style.RESET_ALL}", end=end, flush=True)


        elif mode == PrintMode.RAINBOW:

            # 彩虹色效果

            color_idx = 0

            for char in text:

                if char == "\n":
                    print(char, end="")

                    continue

                c = COLOR_NAMES.get(self.rainbow_colors[color_idx], Fore.WHITE)

                print(f"{c}{back_color}{text_style}{char}", end="")

                color_idx = (color_idx + 1) % len(self.rainbow_colors)

                if delay:
                    time.sleep(wait_time / 5)

            print(f"{Style.RESET_ALL}", end=end, flush=True)

        elif mode == PrintMode.PARAGRAPH:
            # 段落式输出
            paras = textwrap.wrap(text, width=para_length)
            for i, para in enumerate(paras):
                print(f"{fore_color}{back_color}{text_style}{para}", end=" ")
                if (i + 1) % 2 == 0:
                    print()
                    if delay:
                        time.sleep(wait_time)
            print(end=end)


        elif mode == PrintMode.TYPEWRITER:

            # 打字机效果（添加中断检查）

            for char in text:

                # 检查是否有按键按下（如ESC），有则立即中断

                if KeyBoard._kbhit():

                    key = KeyBoard.get_key(block=False)

                    if key == KeyboardKeys.ESC:
                        KeyBoard.flush()  # 清空缓冲

                        break

                print(f"{fore_color}{back_color}{text_style}{char}", end="", flush=True)

                if char not in [' ', '\t', '\n'] and delay:
                    time.sleep(wait_time)

            print(end=end)

        elif mode == PrintMode.RANDOM_LINE:
            # 整行随机颜色
            random_color = random.choice(self.all_colors)
            line_color = COLOR_NAMES.get(random_color, Fore.WHITE)
            print(f"{line_color}{back_color}{text_style}{text}", end=end)

        elif mode == PrintMode.RANDOM_CHAR:
            # 每个字符随机颜色
            for char in text:
                if char == "\n":
                    print(char, end="")
                    continue
                random_color = random.choice(self.all_colors)
                char_color = COLOR_NAMES.get(random_color, Fore.WHITE)
                print(f"{char_color}{back_color}{text_style}{char}", end="")
                if delay:
                    time.sleep(wait_time / 10)
            print(end=end)

        elif mode == PrintMode.ENHANCED_TYPEWRITER:
            # 增强版打字机效果，支持按Enter加速
            speed = kwargs.get('speed', 0.05)  # 初始速度
            accelerated = False
            for i, char in enumerate(text):
                # 检查是否有按键按下（加速）
                if KeyBoard._kbhit():
                    key = KeyBoard.get_key(block=False)
                    if key == KeyboardKeys.ENTER:
                        accelerated = True
                        KeyBoard.flush()  # 清空按键缓冲区

                print(f"{fore_color}{back_color}{text_style}{char}", end="", flush=True)

                # 根据加速状态调整延迟
                if not accelerated and char not in [' ', '\t', '\n']:
                    time.sleep(speed)
                elif accelerated:
                    # 加速模式下的微小延迟，确保可见性
                    time.sleep(speed / 10)

            print(end=end)
        print(Style.RESET_ALL, end="", flush=True)

        # 应用延迟
        if delay and wait_time > 0 and mode not in [PrintMode.RAINBOW, PrintMode.TYPEWRITER, PrintMode.RANDOM_CHAR]:
            time.sleep(wait_time)

    def render_pygame(self, text: str, color: str = 'white', back: str = 'black',
                      style: str = 'normal', end: str = '\n', pos: tuple = (50, 50), **kwargs) -> None:
        """Pygame环境文本渲染（简化实现）"""
        self._init_pygame()
        if self.config.environment != ENV_PYGAME or not self.pygame_initialized:
            return

        import pygame
        # 颜色映射（简化版）
        color_map = {
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'yellow': (255, 255, 0),
            'blue': (0, 0, 255),
            'magenta': (255, 0, 255),
            'cyan': (0, 255, 255),
            'white': (255, 255, 255),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128)
        }

        # 获取颜色
        text_color = color_map.get(color.lower(), (255, 255, 255))

        # 设置字体
        font_size = kwargs.get('font_size', 36)
        font = pygame.font.Font(None, font_size)

        # 渲染文本
        text_surface = font.render(text, True, text_color)

        # 绘制到屏幕
        self.screen.blit(text_surface, pos)
        pygame.display.flip()

        # 处理延迟
        delay = kwargs.get('delay', True)
        wait_time = kwargs.get('wait_time', 0.1)
        if delay and wait_time > 0:
            time.sleep(wait_time)


# 进度条和倒计时工具类
class ProgressTools:
    def __init__(self, i18n: I18nManager):
        self.i18n = i18n

    def progress_bar(self, progress: float, length: int = 20, title: str = "") -> None:
        """显示进度条"""
        if not title:
            title = self.i18n.gettext("进度")

        percent = min(1.0, max(0.0, progress))
        filled_length = int(length * percent)
        bar = '#' * filled_length + '-' * (length - filled_length)
        print(f"\r{title}: [{bar}] {percent:.1%}", end='', flush=True)

        if percent == 1.0:
            print()  # 完成时换行

    def countdown(self, seconds: int, title: str = "") -> None:
        """显示倒计时"""
        if not title:
            title = self.i18n.gettext("倒计时")

        for i in range(seconds, 0, -1):
            print(f"\r{title}: {i}...", end='', flush=True)
            time.sleep(1)
        print(f"\r{self.i18n.gettext('完成！')}      ")


# 菜单项类
class MenuItem:
    def __init__(self, text: str, action: Callable, shortcut: Optional[str] = None,
                 color: str = "white", selected_color: str = "green"):
        self.text = text  # 菜单项文本
        self.action = action  # 点击动作
        self.shortcut = shortcut  # 快捷键
        self.color = color  # 正常状态颜色
        self.selected_color = selected_color  # 选中状态颜色


# 菜单基类
class BaseMenu:
    def __init__(self, title: str, items: List[MenuItem], **kwargs):
        self.title = title
        self.items = items.copy()  # 复制一份避免外部修改影响
        self.kwargs = kwargs

        # 关键修复：确保cli参数被正确传递，否则抛出明确错误
        self.cli = kwargs.get("")
        if self.cli is None:
            raise ValueError("菜单初始化必须提供'cli'参数（CLIUtils实例）。请使用cli.create_menu()方法创建菜单。")

        self.title_color = kwargs.get("title_color", "yellow")
        self.subtitle_color = kwargs.get("subtitle_color", "green")
        self.hint_color = kwargs.get("hint_color", "cyan")
        self.border_color = kwargs.get("border_color", "blue")
        self.indent = kwargs.get("indent", 4)
        self.show_border = kwargs.get("show_border", False)
        self.subtitle = kwargs.get("subtitle", "")
        self.bottom_hint = kwargs.get("bottom_hint", "")
        self.bottom_subtitle = kwargs.get("bottom_subtitle", "")
        self.memory = kwargs.get("memory", False)  # 是否记忆上次选择
        self.last_selected = kwargs.get("last_selected", 0)  # 上次选择的索引
        self.align = kwargs.get("align", "center")  # 新增：对齐方式
        self.terminal_width = get_terminal_width()  # 新增：终端宽度
        self.draw_mode = kwargs.get("draw_mode", "full")  # full: 整屏绘制, incremental: 逐行绘制
        # 位置控制（9个可选位置）
        self.position = kwargs.get("position", "center")  # 新增：9个位置选项
        self._valid_positions = [
            "center", "top-left", "top-right",
            "bottom-left", "bottom-right", "left-half",
            "right-half", "top-half", "bottom-half"
        ]
        if self.position not in self._valid_positions:
            self.position = "center"

        # 绘制模式扩展
        self.draw_style = kwargs.get("draw_style", "progressive")  # progressive/entire
        self.draw_speed = kwargs.get("draw_speed", 0.05)  # 逐行绘制速度
        # 新增配置参数
        self.bg_color = kwargs.get("bg_color", "black")  # 背景颜色
        self.exit_option = kwargs.get("exit_option", True)  # 是否显示退出选项
        self.selected_arrow = kwargs.get("selected_arrow", "→")  # 选中项箭头
        self.arrow_color = kwargs.get("arrow_color", "green")  # 箭头颜色
        self.bottom_title = kwargs.get("bottom_title", "")  # 底部主标题

        # 如果需要显示退出选项，自动添加到菜单末尾
        if self.exit_option and not any(item.text.lower() == "退出" for item in items):
            items.append(MenuItem(
                text="退出",
                action=lambda: None,  # 空动作，通过ESC处理退出
                shortcut="q",
                color="red"
            ))

    def _prepare_menu_elements(self, max_width):
        elements = []
        # 基于终端宽度计算居中缩进（修复对齐核心）
        terminal_width = get_terminal_width()
        indent = max(0, (terminal_width - max_width) // 2)
        indent_str = " " * indent

        if self.show_border:
            # 边框长度严格等于max_width（修复右歪）
            elements.append(f"{indent_str}{'=' * max_width}\n")
        elements.append(f"{indent_str}{self.title.center(max_width)}\n")
        if self.subtitle:
            elements.append(f"{indent_str}{self.subtitle.center(max_width)}\n")
        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")  # 统一使用max_width

        # 菜单项渲染
        for i, item in enumerate(self.items):
            shortcut = f" ({item.shortcut})" if item.shortcut else ""
            full_text = f"{i + 1}. {item.text}{shortcut}"
            elements.append(f"{indent_str}{full_text.center(max_width)}\n")

        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")
        if self.bottom_subtitle:
            elements.append(f"{indent_str}{self.bottom_subtitle.center(max_width)}\n")
        if self.bottom_hint:
            elements.append(f"{indent_str}{self.bottom_hint.center(max_width)}\n")

        return elements  # 注意：原代码此处缩进错误，导致返回值丢失

    def calculate_indent(self, content_length: int = None) -> int:
        """修复：更精确的缩进计算，兼容不同终端宽度"""
        if content_length is None:
            content_length = self.calculate_max_width()

        try:
            # 获取实际终端宽度（考虑窗口大小变化）
            screen_width = os.get_terminal_size().columns
        except (AttributeError, OSError):
            screen_width = 80  # fallback

        # 确保缩进不为负，且内容不超过终端宽度
        return max(0, (screen_width - min(content_length, screen_width)) // 2)

    def _prepare_grid_menu_elements(self, max_width, cols=3):
        """新增：网格菜单元素准备（适配多列布局）"""
        elements = []
        terminal_width = get_terminal_width()
        indent = self.calculate_indent(max_width)
        indent_str = " " * indent

        # 计算每列宽度（平均分配）
        col_width = (max_width - (cols - 1) * 2) // cols  # 减去列间距

        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")
        elements.append(f"{indent_str}{self.title.center(max_width)}\n")
        if self.subtitle:
            elements.append(f"{indent_str}{self.subtitle.center(max_width)}\n")
        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")

        # 按列组织菜单项
        row_elements = []
        for i, item in enumerate(self.items):
            shortcut = f" ({item.shortcut})" if item.shortcut else ""
            item_text = f"{i + 1}. {item.text}{shortcut}"
            # 每列左对齐，填充固定宽度
            row_elements.append(f"{item_text.ljust(col_width)}  ")

            # 达到列数或最后一项时换行
            if (i + 1) % cols == 0 or i == len(self.items) - 1:
                elements.append(f"{indent_str}{''.join(row_elements)}\n")
                row_elements = []

        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")
        if self.bottom_hint:
            elements.append(f"{indent_str}{self.bottom_hint.center(max_width)}\n")

        return elements

    def render_bottom_title(self, max_width: int):
        """渲染底部主标题"""
        if self.bottom_title:
            indent = self.calculate_indent(len(self.bottom_title))
            indent_str = " " * indent
            self.cli.print_text(
                f"{indent_str}{self.bottom_title}",
                color=self.title_color,
                style="bright"
            )

    def calculate_max_width(self):
        """计算最大宽度（确保所有内容都能显示）"""
        if not self.items and not self.title and not self.subtitle:
            return 40  # 默认宽度

        text_elements = [self.title, self.subtitle, self.bottom_hint, self.bottom_subtitle]
        # 计算完整菜单项文本长度（编号 + 文本 + 快捷键）
        for i, item in enumerate(self.items):
            shortcut = f" ({item.shortcut})" if item.shortcut else ""
            full_item_text = f"{i + 1}. {item.text}{shortcut}"
            text_elements.append(full_item_text)

        # 取最长文本长度，增加适当边距
        max_len = max(len(text) for text in text_elements if text)
        return max_len + 4  # 增加边距

    def calculate_position_offsets(self) -> Tuple[int, int]:
        """计算菜单的起始位置偏移（行，列）"""
        terminal_width = get_terminal_width()
        terminal_height = get_terminal_height()
        menu_height = len(self.items) + 6  # 估算菜单高度
        menu_width = self.calculate_max_width()

        row_offset = 0
        col_offset = 0

        # 居中显示时的精确计算
        if self.position == "center":
            row_offset = max(0, (terminal_height - menu_height) // 2)
            col_offset = max(0, (terminal_width - menu_width) // 2)
        elif self.position == "top-left":
            row_offset = 1
            col_offset = 1
        elif self.position == "top-right":
            row_offset = 1
            col_offset = max(0, terminal_width - menu_width - 1)
        elif self.position == "bottom-left":
            row_offset = max(0, terminal_height - menu_height - 1)
            col_offset = 1
        elif self.position == "bottom-right":
            row_offset = max(0, terminal_height - menu_height - 1)
            col_offset = max(0, terminal_width - menu_width - 1)
        elif self.position == "left-half":
            row_offset = max(0, (terminal_height - menu_height) // 2)
            col_offset = max(0, (terminal_width // 2 - menu_width) // 2)
        elif self.position == "right-half":
            row_offset = max(0, (terminal_height - menu_height) // 2)
            col_offset = max(0, terminal_width // 2 + (terminal_width // 2 - menu_width) // 2)
        elif self.position == "top-half":
            row_offset = 1
            col_offset = max(0, (terminal_width - menu_width) // 2)
        elif self.position == "bottom-half":
            row_offset = max(0, (terminal_height // 2 - menu_height) // 2 + terminal_height // 2)
            col_offset = max(0, (terminal_width - menu_width) // 2)

        return row_offset, col_offset

    def render_menu(self):
        """统一渲染入口，所有子类应调用此方法"""
        self.clear_for_redraw()  # 根据绘制模式清屏
        row_offset, col_offset = self.calculate_position_offsets()  # 计算位置
        self.set_cursor_position(row_offset, col_offset)  # 定位光标

        max_width = self.calculate_max_width()
        elements = self._prepare_menu_elements(max_width)  # 准备菜单元素

        # 根据绘制样式渲染
        if self.draw_style == "entire":
            print(''.join(elements), flush=True)
        else:
            for element in elements:
                print(element, end='', flush=True)
                time.sleep(self.draw_speed)

    def set_cursor_position(self, row: int = 0, col: int = 0):
        """设置光标位置到指定的行和列"""
        # 使用ANSI转义序列设置光标位置：\033[行;列H
        print(f"\033[{row};{col}H", end="")

    def clear_for_redraw(self):
        """根据绘制模式清除屏幕或移动光标"""
        if self.draw_mode == "full":
            self.cli.clear_console()
        else:
            # 对于逐行绘制模式，只需将光标移动到菜单起始位置
            # 这里使用ANSI转义序列移动光标
            print("\033[0;0H", end="")  # 移动到左上角

    def render_title(self):
        """渲染标题，确保居中对齐"""
        title_length = len(self.title)
        border = "=" * title_length
        indent = self.calculate_indent(title_length)
        indent_str = " " * indent

        print(f"{indent_str}{border}")
        print(f"{indent_str}{self.title}")
        print(f"{indent_str}{border}")

    def render_full_menu(self):
        """整屏绘制菜单"""
        self.cli.clear_console()
        max_width = self.calculate_max_width()

        # 渲染菜单框架
        if self.show_border:
            self.render_border(max_width)
        self.render_title(max_width)
        self.render_subtitle(max_width)
        if self.show_border:
            self.render_border(max_width)

        # 渲染选项
        for i, item in enumerate(self.items):
            # 渲染每个选项...
            pass

        # 渲染底部信息
        if self.show_border:
            self.render_border(max_width)
        self.render_bottom_subtitle(max_width)
        self.render_bottom_hint(max_width)

    def render_incremental_menu(self):
        """逐行绘制菜单"""
        max_width = self.calculate_max_width()

        # 渲染菜单框架
        if self.show_border:
            self.render_border(max_width)
        self.render_title(max_width)
        self.render_subtitle(max_width)
        if self.show_border:
            self.render_border(max_width)

        # 渲染选项
        for i, item in enumerate(self.items):
            # 渲染每个选项...
            pass

        # 渲染底部信息
        if self.show_border:
            self.render_border(max_width)
        self.render_bottom_subtitle(max_width)
        self.render_bottom_hint(max_width)

    def render_subtitle(self, max_width: int):
        """渲染居中副标题（可选）"""
        if self.subtitle:
            subtitle_length = len(self.subtitle)
            indent = self.calculate_indent(subtitle_length)
            indent_str = " " * indent
            self.cli.print_text(
                f"{indent_str}{self.subtitle}",
                color=self.subtitle_color
            )

        # 修复菜单项渲染的居中对齐

    def render_border(self, max_width: int):
        """渲染居中边框"""
        indent = self.calculate_indent(max_width)
        indent_str = " " * indent
        border = f"{indent_str}{'=' * max_width}"
        self.cli.print_text(border, color=self.border_color)

    def render_bottom_hint(self, max_width: int):
        """渲染底部提示（修复居中）"""
        if self.bottom_hint:
            # 基于终端宽度计算居中，而不是菜单最大宽度
            hint_length = len(self.bottom_hint)
            indent = self.calculate_indent(hint_length)
            indent_str = " " * indent
            self.cli.print_text(
                f"{indent_str}{self.bottom_hint}",
                color=self.hint_color
            )

    def render_bottom_subtitle(self, max_width: int):
        """渲染底部子标题"""
        if self.bottom_subtitle:
            indent_str = " " * self.indent
            self.cli.print_text(
                f"{indent_str}{self.bottom_subtitle:^{max_width}}",
                color=self.subtitle_color
            )

    def run(self):
        # 清空键盘缓冲区
        KeyBoard.flush()

        while True:
            # 绘制菜单
            self.render_menu()

            # 处理输入（添加超时，避免阻塞）
            start_time = time.time()
            key = None
            while time.time() - start_time < 0.1:  # 100ms超时
                key = KeyBoard.get_key(block=False)
                if key:
                    break
                time.sleep(0.01)
        raise NotImplementedError("子类必须实现run()方法")


# 箭头键选择菜单
class ArrowKeyMenu(BaseMenu):
    def run(self):
        if not self.items:
            self.cli.print_warning(self.cli._("菜单无选项"))
            self.cli.pause()
            return

        selected_index = self.last_selected if self.memory and 0 <= self.last_selected < len(self.items) else 0
        option_count = len(self.items)

        while True:
            # 强制清屏（确保旧内容被完全覆盖）
            self.cli.clear_console()
            max_width = self.calculate_max_width()
            indent = self.calculate_indent(max_width)
            indent_str = " " * indent

            # 渲染菜单框架
            if self.show_border:
                print(f"{indent_str}{'=' * max_width}")
            print(f"{indent_str}{self.title.center(max_width)}", flush=True)
            if self.subtitle:
                print(f"{indent_str}{self.subtitle.center(max_width)}", flush=True)
            if self.show_border:
                print(f"{indent_str}{'=' * max_width}")

            # 渲染选项时添加颜色
            for i, item in enumerate(self.items):
                shortcut = f" ({item.shortcut})" if item.shortcut else ""
                full_text = f"{i + 1}. {item.text}{shortcut}"

                if i == selected_index:
                    # 选中项：使用配置的箭头和颜色
                    arrow_color = COLOR_NAMES.get(self.arrow_color, Fore.GREEN)
                    item_color = COLOR_NAMES.get(item.selected_color, Fore.GREEN)
                    print(
                        f"{indent_str}{arrow_color}{self.selected_arrow} "
                        f"{item_color}{full_text.ljust(max_width - 2)}{Style.RESET_ALL}",
                        flush=True
                    )
                else:
                    # 未选中项
                    color = COLOR_NAMES.get(item.color, Fore.WHITE)
                    print(f"{indent_str}  {color}{full_text.ljust(max_width - 2)}{Style.RESET_ALL}", flush=True)

            # 渲染底部信息
            if self.show_border:
                print(f"{indent_str}{'=' * max_width}")
            if self.bottom_subtitle:
                print(f"{indent_str}{self.bottom_subtitle.center(max_width)}", flush=True)
            if self.bottom_hint:
                print(f"{indent_str}{self.bottom_hint.center(max_width)}", flush=True)

            # 处理输入
            key = KeyBoard.get_key(block=True)
            if key == KeyboardKeys.UP:
                # 上箭头：索引减1，最小为0
                selected_index = (selected_index - 1) % option_count
            elif key == KeyboardKeys.DOWN:
                # 下箭头：索引加1，最大为option_count-1（修复核心）
                selected_index = (selected_index + 1) % option_count  # 使用取模确保不越界
            elif key == KeyboardKeys.ENTER:
                # 执行选中项动作
                selected_item = self.items[selected_index]
                if selected_item.text.lower() == "退出":  # 仅退出选项触发退出
                    break
                selected_item.action()  # 执行菜单动作
                self.cli.pause()  # 动作执行后暂停
            elif key == KeyboardKeys.ESC:
                # ESC键退出菜单
                break
            # 处理快捷键（如果有）
            elif key and key.isdigit():
                index = int(key) - 1
                if 0 <= index < option_count:
                    selected_index = index

            return selected_index

    def _prepare_menu_elements(self, max_width):
        """重写父类方法，添加选中状态样式"""
        elements = []
        indent = " " * self.calculate_position_offsets()[1]

        if self.show_border:
            elements.append(f"{indent}{'=' * max_width}\n")
        elements.append(f"{indent}{self.title.center(max_width)}\n")
        if self.subtitle:
            elements.append(f"{indent}{self.subtitle.center(max_width)}\n")
        if self.show_border:
            elements.append(f"{indent}{'=' * max_width}\n")

        # 渲染菜单项（添加选中状态箭头）
        for i, item in enumerate(self.items):
            shortcut = f" ({item.shortcut})" if item.shortcut else ""
            full_text = f"{i + 1}. {item.text}{shortcut}"
            # 选中项添加箭头并高亮
            if i == self.last_selected:
                elements.append(f"{indent}→ {full_text.ljust(max_width - 2)}\n")
            else:
                elements.append(f"{indent}  {full_text.ljust(max_width - 2)}\n")

        if self.show_border:
            elements.append(f"{indent}{'=' * max_width}\n")
        if self.bottom_subtitle:
            elements.append(f"{indent}{self.bottom_subtitle.center(max_width)}\n")
        if self.bottom_hint:
            elements.append(f"{indent}{self.bottom_hint.center(max_width)}\n")

        return elements


# 网格式菜单类（继承自BaseMenu）
class GridMenu(BaseMenu):
    def __init__(self, title: str, items: List[MenuItem], **kwargs):
        super().__init__(title, items, **kwargs)
        # 网格配置参数（带默认值）
        self.cols = kwargs.get("cols", 3)  # 列数
        self.draw_mode = kwargs.get("draw_mode", "whole")  # 绘制模式：whole(整体)/line(逐行)
        self.alignment = kwargs.get("alignment", "center")  # 对齐方式：center(居中)/left(靠左)
        self.cell_padding = kwargs.get("cell_padding", 2)  # 单元格内边距
        self.row_delay = kwargs.get("row_delay", 0.1)  # 逐行绘制时的行间隔时间
        self.last_selected = 0  # 记忆上次选中项
        self.memory = kwargs.get("memory", True)  # 是否记忆选中状态

    def _get_terminal_width(self) -> int:
        """获取终端宽度（用于居中对齐计算）"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80  # fallback默认值

    # 修复网格项宽度计算，确保整体对齐
    def _calculate_cell_width(self, items: List[MenuItem]) -> int:
        if not items:
            return 20
        max_text_len = max(len(item.text) for item in items)
        return max_text_len + self.cell_padding * 2 + 2  # 增加额外边距

    def run(self) -> None:
        if not self.items:
            self.cli.print_warning(self.cli._("菜单无选项"))
            self.cli.pause()
            return

        renderer = self.cli.text_renderer
        selected_idx = self.last_selected if self.memory and 0 <= self.last_selected < len(self.items) else 0
        total_items = len(self.items)
        rows = (total_items + self.cols - 1) // self.cols
        max_width = self.calculate_max_width()  # 计算整体宽度
        indent = self.calculate_indent(max_width)  # 居中缩进
        indent_str = " " * indent

        # 计算每个单元格的宽度
        cell_width = max_width // self.cols

        while True:
            self.cli.clear_console()

            # 顶部边框和标题
            if self.show_border:
                print(f"{indent_str}{'=' * max_width}")
            print(f"{indent_str}{self.title.center(max_width)}", flush=True)
            if self.subtitle:
                print(f"{indent_str}{self.subtitle.center(max_width)}", flush=True)
            if self.show_border:
                print(f"{indent_str}{'=' * max_width}")
            print()  # 标题与内容间空行

            # 绘制网格 - 修复：将print放入行循环内，确保每行都打印
            for row_idx in range(rows):
                row_text = ""
                for col_idx in range(self.cols):
                    item_idx = row_idx * self.cols + col_idx
                    if item_idx < total_items:
                        item = self.items[item_idx]
                        # 确定文本颜色（选中项高亮）
                        color = item.selected_color if item_idx == selected_idx else item.color
                        fore_color = COLOR_NAMES.get(color.lower(), Fore.WHITE)

                        # 格式化单元格文本，确保宽度一致
                        cell_content = f"{item.text}"
                        if item.shortcut:
                            cell_content += f" ({item.shortcut})"

                        # 确保每个单元格宽度一致
                        cell_text = cell_content.ljust(cell_width)
                        row_text += f"{fore_color}{cell_text}{Style.RESET_ALL}"
                # 修复：缩进调整，确保每行都打印
                print(f"{indent_str}{row_text}")

            print()  # 内容与底部提示间空行

            # 底部边框和提示
            if self.show_border:
                print(f"{indent_str}{'=' * max_width}")
            print(f"{indent_str}{self.cli._('Esc返回  ↑↓←→移动  Enter选择').center(max_width)}", flush=True)

            key = KeyBoard.get_key(block=True)
            if key == KeyboardKeys.ESC:
                self.last_selected = selected_idx
                KeyBoard.flush()  # 清空缓冲区
                return  # 退出子菜单，返回上级
            elif key == KeyboardKeys.ENTER:
                self.items[selected_idx].action()
                KeyBoard.flush()
                break  # 执行后退出
            elif key == KeyboardKeys.UP:
                new_idx = selected_idx - self.cols
                selected_idx = new_idx if new_idx >= 0 else selected_idx
            elif key == KeyboardKeys.DOWN:
                new_idx = selected_idx + self.cols
                selected_idx = new_idx if new_idx < total_items else selected_idx
            elif key == KeyboardKeys.LEFT:
                selected_idx = max(0, selected_idx - 1)
            elif key == KeyboardKeys.RIGHT:
                selected_idx = min(total_items - 1, selected_idx + 1)

    # 修复网格菜单项的颜色和对齐
    def _draw_row(self, row_items: List[MenuItem], row_idx: int, selected_idx: int, renderer: TextRenderer):
        """绘制单行菜单项"""
        cell_width = self._calculate_cell_width(self.items)
        row_text = ""
        terminal_width = self._get_terminal_width()

        for col_idx, item in enumerate(row_items):
            # 计算当前项索引
            item_idx = row_idx * self.cols + col_idx
            if item_idx >= len(self.items):
                break  # 处理最后一行可能不满的情况

            # 确定文本颜色（选中项高亮）
            color = item.selected_color if item_idx == selected_idx else item.color

            # 格式化单元格文本（带内边距）
            padded_text = f"{' ' * self.cell_padding}{item.text}{' ' * self.cell_padding}"
            # 左对齐填充到单元格宽度
            cell_text = padded_text.ljust(cell_width)

            # 添加到行文本，应用颜色
            fore_color = COLOR_NAMES.get(color.lower(), Fore.WHITE)
            row_text += f"{fore_color}{cell_text}{Style.RESET_ALL}"

        # 处理对齐方式
        if self.alignment == "center":
            row_text = row_text.center(terminal_width)

        # 绘制行
        print(row_text)


# 数字键选择菜单
class NumberKeyMenu(BaseMenu):
    """数字键选择菜单：用户通过输入数字编号选择菜单项"""

    def run(self):
        KeyBoard.flush()
        back_to_parent = False  # 新增标记：是否返回父菜单
        if not self.items:
            self.cli.print_warning(self.cli._("菜单无选项"))
            self.cli.pause()
            return

        selected_index = self.last_selected if self.memory and 0 <= self.last_selected < len(self.items) else 0

        while True:
            self.render_menu()
            key = KeyBoard.get_key(block=True)

            if key == KeyboardKeys.ESC:
                back_to_parent = True  # 标记为返回父菜单
                break  # 直接退出循环，不显示额外提示
            elif key == KeyboardKeys.ENTER:
                self.last_selected = selected_index
                KeyBoard.flush()
                self.cli.clear_console()  # 增加清屏
                self.items[selected_index].action()
                self.cli.pause()
                return selected_index
            elif key and key.isdigit():
                idx = int(key) - 1
                if 0 <= idx < len(self.items):
                    selected_index = idx
                    self.last_selected = selected_index
                    KeyBoard.flush()
                    self.cli.clear_console()
                    # 只执行一次动作
                    self.items[selected_index].action()
                    # 等待用户确认
                    self.cli.pause(message=self.cli._("按Enter键返回..."))
                    return selected_index
        if back_to_parent:
            # 仅显示一次返回提示
            self.cli.print_text(self.cli._("按Enter键返回主菜单..."), mode=PrintMode.INTERACTIVE)
            return  # 确保退出后不再进入循环

            return selected_index


    # 在NumberKeyMenu的_prepare_menu_elements方法中修改
    def _prepare_menu_elements(self, max_width):
        elements = []
        # 使用位置计算的列偏移作为缩进，与其他菜单保持一致
        _, col_offset = self.calculate_position_offsets()
        indent_str = " " * col_offset

        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")

        # 标题居中显示
        elements.append(f"{indent_str}{self.title.center(max_width)}\n")
        if self.subtitle:
            elements.append(f"{indent_str}{self.subtitle.center(max_width)}\n")

        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")

        # 菜单项渲染
        for i, item in enumerate(self.items):
            shortcut = f" ({item.shortcut})" if item.shortcut else ""
            full_text = f"{i + 1}. {item.text}{shortcut}"
            elements.append(f"{indent_str}{full_text.ljust(max_width)}\n")

        # 底部元素保持一致缩进
        if self.show_border:
            elements.append(f"{indent_str}{'=' * max_width}\n")
        if self.bottom_subtitle:
            elements.append(f"{indent_str}{self.bottom_subtitle.center(max_width)}\n")

        default_hint = self.cli._("按数字键选择菜单项")
        elements.append(f"{indent_str}{(self.bottom_hint or default_hint).center(max_width)}\n")

        return elements


# 鼠标菜单（预留接口）
class MouseMenu(BaseMenu):
    def run(self):
        self.cli.print_warning("鼠标菜单暂未实现")
        self.cli.pause()


# 命令行工具主类
class CLIUtils:
    def __init__(self):
        self.config = ConfigManager()
        self.i18n = I18nManager(self.config.language)
        self._ = self.i18n.gettext  # 简化国际化调用
        self.text_renderer = TextRenderer(self.config)
        self.progress = ProgressTools(self.i18n)
        self.menus = {}  # 存储菜单实例，用于记忆功能

    def update_all_menu_texts(self):
        """切换语言后，更新所有已创建菜单的文本"""
        for menu in self.menus.values():
            # 更新箭头键菜单
            if isinstance(menu, ArrowKeyMenu):
                menu.bottom_hint = self._("Esc返回主菜单  ↑↓切换  Enter选择")
            # 更新数字键菜单
            elif isinstance(menu, NumberKeyMenu):
                menu.bottom_hint = self._("按数字键选择菜单项")
            # 更新网格菜单
            elif isinstance(menu, GridMenu):
                pass  # 网格菜单提示在run中动态获取，无需提前设置

    def set_environment(self, env: str) -> None:
        """设置运行环境"""
        self.config.set_environment(env)

    def set_language(self, lang: str) -> None:
        """设置语言"""
        self.config.set_language(lang)
        self.i18n = I18nManager(lang)
        self._ = self.i18n.gettext
        self.progress = ProgressTools(self.i18n)

    def set_console_background(self, color: str):
        """设置命令行背景颜色"""
        set_console_color(background=color)

    def reset_console_color(self):
        """重置命令行颜色为默认值（白色前景，黑色背景）"""
        set_console_color()

    def clear_console(self) -> None:
        """清空控制台"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self, message: str = None, key_press: bool = False) -> None:
        """
        暂停程序，等待用户输入
        key_press=True 时按任意键继续，否则按Enter继续
        """
        if message is None:
            message = self._("按Enter键返回主菜单...") if not key_press else self._("按任意键继续...")

        print(f"\n{message}", end=" " if not key_press else "", flush=True)

        if key_press:
            KeyBoard.get_key(block=True)
            print()
        else:
            input()

        KeyBoard.flush()

    def wrap_color(self, text: str, color: str = "white", style: str = "normal") -> str:
        """包装带颜色的文本，不立即打印"""
        fore_color = COLOR_NAMES.get(color.lower(), Fore.WHITE)
        text_style = STYLES.get(style.lower(), Style.NORMAL)
        return f"{fore_color}{text_style}{text}{Style.RESET_ALL}"

    def print_text(self, text: str, color: str = 'white', back: str = 'black',
                   style: str = 'normal', end: str = '\n', **kwargs) -> None:
        """统一打印文本接口"""
        if self.config.environment == ENV_COMMAND_LINE:
            self.text_renderer.render_cli(text, color, back, style, end, **kwargs)
        else:
            # 从kwargs中取出pos并移除，避免重复传递
            pos = kwargs.pop('pos', (50, 50))  # 使用pop()而不是get()，移除kwargs中的pos
            self.text_renderer.render_pygame(
                text, color, back, style, end,
                pos=pos,  # 显式指定pos参数
                **kwargs  # 此时kwargs中已无pos，避免重复
            )

    def print_success(self, text: str) -> None:
        """打印成功消息"""
        self.print_text(text, color="green", style="bright")

    def print_error(self, text: str) -> None:
        """打印错误消息"""
        self.print_text(text, color="red", style="bright")

    def print_warning(self, text: str) -> None:
        """打印警告消息"""
        self.print_text(text, color="yellow", style="bright")

    def print_info(self, text: str) -> None:
        """打印信息消息"""
        self.print_text(text, color="blue", style="bright")

    def create_menu(self, menu_id: str, title: str, items: List[MenuItem], **kwargs) -> None:
        """
        创建并运行菜单（推荐方式）
        menu_id: 菜单唯一标识，用于记忆功能
        """
        # 菜单类型
        menu_type = kwargs.get("menu_type", "arrow")  # arrow, number, grid, mouse
        layout = kwargs.get("layout", "list")  # list, grid

        # 底部提示默认值
        if menu_type == "arrow" and "bottom_hint" not in kwargs:
            kwargs["bottom_hint"] = self._("Esc返回主菜单  ↑↓切换  Enter选择")
        elif menu_type == "number" and "bottom_hint" not in kwargs:
            kwargs["bottom_hint"] = self._("按数字键选择菜单项")

        # 强制传递CLI实例（关键修复）
        kwargs["cli"] = self

        # 检查是否已有该菜单实例（用于记忆功能）
        if menu_id in self.menus:
            menu = self.menus[menu_id]
            menu.title = title
            menu.items = items.copy()
            # 更新其他属性
            for key, value in kwargs.items():
                if hasattr(menu, key):
                    setattr(menu, key, value)
        else:
            # 创建新菜单
            if menu_type == "arrow" or (menu_type not in ["number", "grid", "mouse"] and layout == "list"):
                menu = ArrowKeyMenu(title, items, **kwargs)
            elif menu_type == "number":
                menu = NumberKeyMenu(title, items, **kwargs)
            elif menu_type == "grid" or layout == "grid":
                menu = GridMenu(title, items, **kwargs)
            else:  # mouse
                menu = MouseMenu(title, items, **kwargs)

            self.menus[menu_id] = menu

        # 运行菜单
        menu.run()

    def get_menu(self, menu_id: str) -> Optional[BaseMenu]:
        """获取菜单实例"""
        return self.menus.get(menu_id)


# 全局CLI工具实例
cli = CLIUtils()


# 对外接口函数
def render(text: str, color: str = 'white', back: str = 'black', style: str = 'normal',
           end: str = '\n', pos: tuple = (50, 50), **kwargs) -> None:
    """统一渲染函数接口"""
    cli.print_text(text, color, back, style, end, pos=pos, **kwargs)


def clear_console() -> None:
    """清空控制台接口"""
    cli.clear_console()


def get_terminal_width() -> int:
    """获取终端宽度，默认80列"""
    try:
        return os.get_terminal_size().columns
    except (AttributeError, OSError):
        return 80  # 兼容不支持的环境


def get_terminal_height() -> int:
    """获取终端高度，默认24行"""
    try:
        return os.get_terminal_size().lines
    except (AttributeError, OSError):
        return 24  # 兼容不支持的环境



def set_console_color(foreground: str = "white", background: str = "black"):
    """
    设置Windows命令行的前景色和背景色
    颜色支持: black, red, green, yellow, blue, magenta, cyan, white
    """
    color_map = {
        "black": "0",
        "blue": "1",
        "green": "2",
        "cyan": "3",
        "red": "4",
        "magenta": "5",
        "yellow": "6",
        "white": "7"
    }

    # 转换为大写字母以符合color命令要求
    fg = color_map.get(foreground.lower(), "7")  # 默认白色前景
    bg = color_map.get(background.lower(), "0")  # 默认黑色背景

    # 执行color命令设置颜色
    os.system(f"color {fg}{bg}")


class ComprehensiveTestMenu(ArrowKeyMenu):
    def __init__(self, cli):
        def test_arrow_menu():
            items = [
                MenuItem("选项 1", lambda: cli.print_success("选择了选项 1"), "1"),
                MenuItem("选项 2", lambda: cli.print_success("选择了选项 2"), "2"),
                MenuItem("选项 3", lambda: cli.print_success("选择了选项 3"), "3")
            ]
            cli.create_menu(
                "test_arrow",
                "箭头键菜单测试",
                items,
                menu_type="arrow",
                show_border=True,
                memory=True
            )

        def test_number_menu():
            items = [
                MenuItem("选项 A", lambda: cli.print_success("选择了选项 A"), "pypi"),
                MenuItem("选项 B", lambda: cli.print_success("选择了选项 B"), "b"),
                MenuItem("选项 C", lambda: cli.print_success("选择了选项 C"), "c")
            ]
            cli.create_menu(
                "test_number",
                "数字键菜单测试",
                items,
                menu_type="number",
                show_border=True
            )

        def test_grid_menu():
            items = [
                MenuItem("项目 1", lambda: cli.print_success("选择了项目 1"), "1"),
                MenuItem("项目 2", lambda: cli.print_success("选择了项目 2"), "2"),
                MenuItem("项目 3", lambda: cli.print_success("选择了项目 3"), "3"),
                MenuItem("项目 4", lambda: cli.print_success("选择了项目 4"), "4"),
                MenuItem("项目 5", lambda: cli.print_success("选择了项目 5"), "5"),
                MenuItem("项目 6", lambda: cli.print_success("选择了项目 6"), "6")
            ]
            cli.create_menu(
                "test_grid",
                "网格菜单测试",
                items,
                menu_type="grid",
                cols=3,
                show_border=True
            )

        def switch_language_action(cli):
            def inner():  # 增加内部函数作为可调用的action
                current_lang = cli.config.language
                new_lang = "en" if current_lang == "zh" else "zh"
                cli.config.set_language(new_lang)
                cli.i18n = I18nManager(new_lang)
                cli._ = cli.i18n.gettext  # 更新翻译函数
                cli.update_all_menu_texts()  # 更新所有菜单文本
                cli.print_text(f"已切换到{'英文' if new_lang == 'en' else '中文'}模式")

            return inner  # 返回内部函数

        # 正确赋值
        self.toggle_language = switch_language_action(cli)


        self.test_arrow_menu = test_arrow_menu
        self.test_number_menu = test_number_menu
        self.test_grid_menu = test_grid_menu

        items = [
            MenuItem("测试箭头键菜单", self.test_arrow_menu, "1"),
            MenuItem("测试数字键菜单", self.test_number_menu, "2"),
            MenuItem("测试网格菜单", self.test_grid_menu, "3"),
            MenuItem("切换语言", self.toggle_language, "4")]

        super().__init__(
            title="综合测试菜单",
            items=items,
            cli=cli,
            subtitle="选择要测试的功能",
            bottom_hint=cli._("Esc返回主菜单  ↑↓切换  Enter选择"),
            position="center",  # 使用居中位置
            show_border=True
        )
