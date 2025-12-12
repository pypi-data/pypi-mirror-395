'''
pyutool.umodules.set_default.py
This module is designed to provide common default values.
提供通用默认值的模块
'''

'''  待处理
·.-﹉..–ａｂｃｄｅｆ‥★☆●○◎◆◇▲▼△▽□■¤°▪⭐✦✧✯
✡✩✫✭✮✶✷✸✹✨🌟◉☼∧∨∪∩⊥∠∟Ω°⊞⊟⊠◌◯⦿►◄◂▸▷◁▻◃◅▿▾▴▵▣◾▢▫❐❒
▯▰▱◈❑◢◣◤◥▒◊◘◙◚◛▤▥▦▧▨▩◧◨◳◲◱◰◫◪◩▙▛▜▟１２３ⅰⅱⅲⅳⅴ
ⅵⅶⅷⅸⅹⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁᵂⱽ⁺⁻⁼⁽⁾₊₋₌₍
₎ₐₔₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵥₓ᙮ᵩᵦ˪៳៷ᵨ៴ᵤᵪᵧᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴄᴅᴇғᴏᴘǫʀsᴛᴜᴠsᴛᴜᴡᴠxʏᴢ︵︶
︷︸︹︺︿﹀︽︾﹁﹂﹃︖︕︔︑︐︒︓︾﹁﹂﹃﹄︻︼︗︘_¯＿￣﹏﹋﹍﹉
﹎﹊¦︴¡¿^ˇ¨ˊαβγδεζηθικλμνξοπφωΑΒΓΔΕавА↺↻➠⇦⇧⇨⇩➤➣➢➨⬆⬇⬅の
丶╔ ╚ ╗ ╝╬▉▊▋▌▍▎▏▔▕♺♻🎦⏬⏪⏩⏫
'''


# -*- coding: utf-8 -*-

# Built-in modules
from enum import Enum
from typing import Dict, List, Tuple, Any
from string import ascii_uppercase

# Third-party modules
from colorama import Fore, Back, Style

# Local modules
# (无本地依赖)
space = ' '


# 字母常量
A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = tuple(ascii_uppercase)
LETTERS = (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z)

# 图标管理
ICONS = {
    'grass': '▨',
    'wall': '▣',
    'electric': '◩',
    'award': '◆',
    'white': '■',
    'radiation': '☢',
    'biochemical': '☣',
    'thunder': '⚡',
    'music': '♪♬♫',
    'crown': '♛♕',
    'refresh': '🔄'
}

def get_letter_location(LETTER: str) -> int:
    return LETTERS.index(LETTER)

def get_specified_letters(location: Tuple[int, int]) -> Tuple[str, ...]:
    return LETTERS[location[0]+1:location[1]+1]

class FileFormat(Enum):
    """文件格式枚举"""
    TEXT = ('txt', 'cfg', 'ini', 'py', 'md')
    BINARY = ('bin', 'exe', 'dll')
    IMAGE = ('png', 'jpg', 'gif')

class WindowsSign(Enum):
    """Windows支持的特殊符号枚举"""
    WINDOWS_SIGNS = {
        'arrows': ['▷', '▼▲'],
        'blocks': ['▁▂▃']
    }
    BRACKETS = ('『』', '「」')
    BLOCKS = ('▁', '▂', '▃', '▄', '▅', '▆', '▇', '█')  # 拆分单个符号为元组元素
    SHAPES = ('◆◇□■', '★☆●○◎')
    DECORATIVE = ('﹁﹂﹃﹄︻︼︗︘', '︵︶︷︸')
# pyutool.umodules.set_adfult.WindowsSign.WINDOWS_SIGNS["arrows"][0]

class OPERATORS:
    addition = '+'
    subtraction = '-'
    multiplication = '*'
    division = '/'
    OPERATORS = (addition, subtraction, multiplication, division)

class Producer:
    """默认值生成器类"""

    BASIC_TYPES = (int, bytes, bool, str, set, list, dict, tuple, type(None), float)
    NUMBERS = tuple(range(1, 10))
    SMALL_NUMBERS = '⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉'
    SERIAL_NUMBERS = '⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑'


    @property
    def basic_data(self) -> Dict[str, Any]:
        """返回基础数据类型的示例值"""
        return {
            'int': 1,
            'str': "1",
            'bool': True,
            'None': None,
            'set': set('1'),
            'list': [],
            'dict': {},
            'tuple': (1, 1),
            'float': 1.0,
        }

    @property
    def numbers(self) -> Tuple[int, ...]:
        """返回数字序列"""
        return self.NUMBERS

    @property
    def basic_types(self) -> Tuple[type, ...]:
        """返回基础类型元组"""
        return self.BASIC_TYPES

    @property
    def letters(self) -> Tuple[str, ...]:
        """返回字母元组"""
        return LETTERS

    def gain_file_format(self) -> Dict[str, Tuple[str, ...]]:
        """返回文件格式信息"""
        return {
            'text_file': FileFormat.TEXT.value,
            'all_format': tuple(format_.value for format_ in FileFormat)
        }

    @property
    def iters(self) -> List[type]:
        """返回可迭代类型列表"""
        return [list, tuple, dict]

    def get_icons(self) -> Dict[str, str]:
        """返回所有图标"""
        return ICONS

    def get_windows_support_sign(self) -> Tuple[str, ...]:
        """返回Windows支持的符号"""
        return tuple(sign.value for sign in WindowsSign)

    def test(self):
        """测试方法，打印所有特殊字符"""
        test_items = [
            self.SERIAL_NUMBERS,
            self.SMALL_NUMBERS,
            ICONS['thunder'],
            ICONS['refresh'],
            ICONS['crown'],
            ICONS['radiation'],
            ICONS['music'],
            ICONS['biochemical'],
            WindowsSign.BRACKETS.value
        ]

        for item in test_items:
            print(item)
        input('按下回车结束..')

class AppIdentity:
    Master = '管理员'
    User = "游戏用户"
    Developer = '开发者'



if __name__ == '__main__':
    # Producer().test()

    DEEPSEEK_API_KEY = "sk-1fd613757f2f409c98f8092a0c03f339"
