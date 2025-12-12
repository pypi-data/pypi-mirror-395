
# game_engine.py
# Built-in modules
import copy

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)

class Things:
    def __init__(self, data:dict):
        # 使用完全独立的深拷贝
        self.initial_data = copy.deepcopy(data)
        # 当前状态
        self.data = copy.deepcopy(data)

    def full_reset(self):
        # 完全重置所有状态
        self.data = copy.deepcopy(self.initial_data)

class Item:
    pass

class Equipment:
    pass

class State:
    pass

class Tag:
    pass