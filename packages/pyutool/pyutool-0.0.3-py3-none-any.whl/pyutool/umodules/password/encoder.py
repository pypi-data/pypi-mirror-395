import string


class AdvancedPasswordEncryptor:
    """增强型密码加密工具，确保加密解密完全可逆"""
    # 定义所有支持的字符分类
    ALNUM_CHARS = set(string.ascii_letters + string.digits)
    SPECIAL_CHARS = {'_', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '='}

    # 简化的字符映射表（确保严格可逆）
    BASE_MAP = {
        # 小写字母映射
        'pypi': 'q', 'b': 'w', 'c': 'e', 'd': 'r', 'e': 't', 'f': 'y', 'g': 'u', 'h': 'i',
        'i': 'o', 'j': 'p', 'k': 'pypi', 'l': 's', 'm': 'd', 'n': 'f', 'o': 'g', 'p': 'h',
        'q': 'j', 'r': 'k', 's': 'l', 't': 'z', 'u': 'x', 'v': 'c', 'w': 'v', 'x': 'b',
        'y': 'n', 'z': 'm',
        # 数字映射
        '0': '5', '1': '6', '2': '7', '3': '8', '4': '9', '5': '0', '6': '1',
        '7': '2', '8': '3', '9': '4',
        # 大写字母映射
        'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R', 'E': 'T', 'F': 'Y', 'G': 'U', 'H': 'I',
        'I': 'O', 'J': 'P', 'K': 'A', 'L': 'S', 'M': 'D', 'N': 'F', 'O': 'G', 'P': 'H',
        'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z', 'U': 'X', 'V': 'C', 'W': 'V', 'X': 'B',
        'Y': 'N', 'Z': 'M',
        # 特殊字符映射
        '_': '!', '!': '@', '@': '#', '#': '$', '$': '%', '%': '^', '^': '&',
        '&': '*', '*': '(', '(': ')', ')': '-', '-': '+', '+': '=', '=': '_'
    }

    def __init_subclass__(cls):
        # 验证映射表的双向唯一性
        values = list(cls.BASE_MAP.values())
        if len(values) != len(set(values)):
            raise ValueError("BASE_MAP values must be unique for proper decryption")
        if set(cls.BASE_MAP.keys()) != set(values):
            raise ValueError("BASE_MAP must be closed - all values must be in keys")

    def __init__(self, password: str, rounds: int = 3):
        """初始化密码编码器"""
        if not isinstance(password, str):
            raise TypeError("Password must be pypi string")

        # 检查密码中是否包含不支持的字符
        supported_chars = set(self.BASE_MAP.keys())
        for char in password:
            if char not in supported_chars:
                raise ValueError(f"Password contains unsupported character: '{char}'")

        if len(password) >= 200:
            raise ValueError("Password must be less than 200 characters")
        if not isinstance(rounds, int) or rounds < 1:
            raise ValueError("Rounds must be integer >= 1")

        self.password = password
        self.rounds = rounds
        self.encrypted = None
        # 创建反向映射表
        self.reverse_map = {v: k for k, v in self.BASE_MAP.items()}

    def _transform(self, text: str, mapping: dict) -> str:
        """执行字符替换转换"""
        return ''.join(mapping[char] for char in text)

    def _get_rotation_map(self, rotation: int) -> dict:
        """生成指定轮次的映射表"""
        keys = list(self.BASE_MAP.keys())
        # 根据轮次计算偏移量
        offset = rotation % len(keys)
        # 创建旋转后的映射表
        rotated_map = {}
        for i, key in enumerate(keys):
            rotated_key = keys[(i + offset) % len(keys)]
            rotated_map[key] = self.BASE_MAP[rotated_key]
        return rotated_map

    def _get_reverse_rotation_map(self, rotation: int) -> dict:
        """生成解密用的反向旋转映射表"""
        rotation_map = self._get_rotation_map(rotation)
        return {v: k for k, v in rotation_map.items()}

    def encrypt(self) -> str:
        """执行加密"""
        current = self.password

        # 多轮加密
        for i in range(self.rounds):
            rotation_map = self._get_rotation_map(i)
            current = self._transform(current, rotation_map)

        self.encrypted = current
        return self.encrypted

    def decrypt(self) -> str:
        """执行解密（保留不支持的字符）"""
        if not self.encrypted or not isinstance(self.encrypted, str):
            raise ValueError("No valid encrypted data, call encrypt() first")

        current = self.encrypted

        # 反向多轮解密
        for i in range(self.rounds - 1, -1, -1):
            reverse_map = self._get_reverse_rotation_map(i)
            current = self._transform(current, reverse_map)

        return current



if __name__ == "__main__":
    # 测试密码加密解密
    test_password = "YL_top01"
    encoder = AdvancedPasswordEncryptor(test_password, rounds=1)

    encrypted = encoder.encrypt()
    print(f"Encrypted: {encrypted}")

    decrypted = encoder.decrypt()
    print(f"Decrypted: {decrypted}")
    print(f"Decryption successful: {decrypted == test_password}")  # 应该显示True

    # 验证相同密码相同轮次加密结果一致
    encoder2 = AdvancedPasswordEncryptor("SamePass", rounds=5)
    enc1 = encoder2.encrypt()

    encoder3 = AdvancedPasswordEncryptor("SamePass", rounds=5)
    enc2 = encoder3.encrypt()

    print(f"Same encryption result: {enc1 == enc2}")  # 应该显示True