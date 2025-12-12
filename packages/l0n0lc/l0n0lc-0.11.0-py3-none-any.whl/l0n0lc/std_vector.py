
from .cpp类型 import C变量, Cpp类型, 列表初始化列表


class 标准列表(C变量):
    def __init__(
            self,
            初始化列表: 列表初始化列表,
            名称: str, 
            是否参数: bool) -> None:
        self.初始化列表 = 初始化列表
        if 初始化列表.类型名 == Cpp类型.任意:
            super().__init__(f'std::vector<{初始化列表.类型名}>', 名称, 是否参数)
        else:
            super().__init__(f'std::vector<{初始化列表.类型名}>', 名称, 是否参数)

    def __getitem__(self, key):
        return f'{self}[{key}]'

    def __setitem__(self, key, value):
        return f'{self}[{key}] = {value};'
    
    # 使用父类的 init_code (即 初始化代码) 即可，因为 vector 初始化可以用 = { ... }
    # 如果需要特殊处理，可以重写 初始化代码 方法
