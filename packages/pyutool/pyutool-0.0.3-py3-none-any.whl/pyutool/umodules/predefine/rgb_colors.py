"""
合并后的颜色模块
提供控制台颜色控制和RGB颜色定义及操作
"""


# Built-in modules
from typing import Tuple

# Third-party modules
from colorama import Fore, Back, Style


# Local modules
# (无本地依赖)

class Colors:
    """统一颜色管理类（控制台颜色+RGB颜色，含Pygame专用效果色）"""
    # 控制台前景色
    FORE_COLOR = {
        'white': Fore.WHITE, 'black': Fore.BLACK, 'yellow': Fore.YELLOW,
        'green': Fore.GREEN, 'cyan': Fore.CYAN, 'magenta': Fore.MAGENTA,
        'blue': Fore.BLUE, 'red': Fore.RED, 'gray': Fore.LIGHTBLACK_EX,
        'bright_red': Fore.LIGHTRED_EX, 'bright_green': Fore.LIGHTGREEN_EX
    }

    # 控制台背景色
    BACK_COLOR = {
        'black': Back.BLACK, 'red': Back.RED, 'green': Back.GREEN,
        'yellow': Back.YELLOW, 'blue': Back.BLUE, 'magenta': Back.MAGENTA,
        'cyan': Back.CYAN, 'white': Back.WHITE, 'gray': Back.LIGHTBLACK_EX
    }

    # 控制台文本样式
    STYLE = {
        'normal': Style.NORMAL, 'dim': Style.DIM, 'bright': Style.BRIGHT
    }

    # RGB颜色（合并基础+扩展+Pygame专用色）
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (190, 190, 190)  # 原PredefinedColors的Grey
    LIGHT_SKY_BLUE = (135, 206, 250)  # 原PredefinedColors的LightSkyBlue
    LAVENDER = (230, 230, 250)        # 原PredefinedColors的lavender
    DARK_GRAY = (50, 50, 50)
    LIGHT_RED = (255, 150, 150)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    HIGHLIGHT = (255, 255, 224)
    SELECTED = (70, 130, 180)
    DISABLED = (180, 180, 180)
    BLINK = (200, 200, 200)  # 保留Pygame按钮点击效果色

    # 颜色映射字典（统一访问入口）
    COLORS = {
        'black': BLACK, 'white': WHITE, 'red': RED, 'green': GREEN, 'blue': BLUE,
        'yellow': YELLOW, 'cyan': CYAN, 'magenta': MAGENTA, 'gray': GRAY,
        'light_sky_blue': LIGHT_SKY_BLUE, 'lavender': LAVENDER,
        'dark_gray': DARK_GRAY, 'light_red': LIGHT_RED, 'orange': ORANGE,
        'purple': PURPLE, 'pink': PINK, 'highlight': HIGHLIGHT,
        'selected': SELECTED, 'disabled': DISABLED, 'blink': BLINK
    }

    # 彩虹色序列（用于彩色打印）
    RAINBOW_COLORS = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

    @classmethod
    def get_fore_color(cls, color_name: str) -> str:
        """获取控制台前景色（默认白色）"""
        return cls.FORE_COLOR.get(color_name.lower(), Fore.WHITE)

    @classmethod
    def get_back_color(cls, color_name: str) -> str:
        """获取控制台背景色（默认黑色）"""
        return cls.BACK_COLOR.get(color_name.lower(), Back.BLACK)

    @classmethod
    def get_style(cls, style_name: str) -> str:
        """获取文本样式（默认正常）"""
        return cls.STYLE.get(style_name.lower(), Style.NORMAL)

    @classmethod
    def get_rgb_color(cls, color_name: str) -> Tuple[int, int, int]:
        """获取RGB颜色（默认白色）"""
        return cls.COLORS.get(color_name.lower(), cls.WHITE)

    @classmethod
    def blend(cls, color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float = 0.5) -> Tuple[int, int, int]:
        """混合两种RGB颜色"""
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return (r, g, b)

    @classmethod
    def darken(cls, color: Tuple[int, int, int], factor: float = 0.7) -> Tuple[int, int, int]:
        """变暗RGB颜色"""
        return tuple(int(c * factor) for c in color)

    @classmethod
    def lighten(cls, color: Tuple[int, int, int], factor: float = 1.3) -> Tuple[int, int, int]:
        """变亮RGB颜色（不超过255）"""
        return tuple(min(255, int(c * factor)) for c in color)
COLORS = Colors()