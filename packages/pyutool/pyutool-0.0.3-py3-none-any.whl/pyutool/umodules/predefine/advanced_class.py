# -*- coding: utf-8 -*-
"""
@Project : pyutool
@File    : advanced_class
@Author  : YL_top01
@Date    : 2025/10/11 21:00
"""

# Built-in modules
# (无内置模块)

# Third-party modules
# (无第三方依赖)

# Local modules
# (无本地依赖)


class AdvancedClass:
    # 类属性：存储当前类自身的非魔法成员（仅计算一次）
    _class_members = []

    @classmethod
    def _update_class_members(cls):
        """更新类自身的非魔法成员列表（可手动调用以支持动态更新）"""
        cls._class_members = []
        for name, value in cls.__dict__.items():
            # 过滤：排除魔法成员、类方法/静态方法（可选，根据需求调整）
            if not (name.startswith("__") and name.endswith("__")):
                cls._class_members.append(name)

    def __init__(self):
        # 实例属性指向类属性，避免重复计算
        self.available_members = self._class_members

    # 可选：支持实例动态添加属性后更新（若需实时反映实例属性）
    def add_attr(self, name, value):
        setattr(self, name, value)
        # 若需将实例动态属性加入列表，可扩展逻辑（需区分类属性和实例属性）


# 类定义后初始化一次类成员列表
AdvancedClass._update_class_members()


# 测试
if __name__ == "__main__":
    a = AdvancedClass()
    print("类自身成员：", AdvancedClass._class_members)  # 仅包含当前类定义的成员
    print("实例可用成员：", a.available_members)

    # 动态添加类成员后更新
    def new_method(self): pass
    AdvancedClass.new_method = new_method
    AdvancedClass._update_class_members()
    print("动态添加类方法后：", AdvancedClass._class_members)  # 包含 'new_method'


