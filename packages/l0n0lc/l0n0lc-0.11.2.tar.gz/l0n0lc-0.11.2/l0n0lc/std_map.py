
from .cpp类型 import 字典初始化列表, C变量
from .工具 import 转C字符串


class 标准无序映射(C变量):
    def __init__(
            self,
            初始化列表: 字典初始化列表,
            名称: str, 
            是否参数: bool) -> None:
        self.初始化列表 = 初始化列表
        super().__init__(
            f'std::unordered_map<{初始化列表.键类型名}, {初始化列表.值类型名}>', 名称, 是否参数)

    def __getitem__(self, key):
        return f'{self}[{转C字符串(key)}]'

    def __setitem__(self, key, value):
        left = f'{self}[{转C字符串(key)}]'
        right = 转C字符串(value)
        return f'{left} = {right};'
