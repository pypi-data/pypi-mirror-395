
from typing import Union, List, get_origin, get_args
import ctypes
from .工具 import 生成变量ID, 转C字符串, 全局上下文
from .异常 import 类型不一致错误


class Cpp类型:
    """
    预定义的 C++ 类型字符串常量。
    """
    INT8_T = 'int8_t'
    INT16_T = 'int16_t'
    INT32_T = 'int32_t'
    INT64_T = 'int64_t'
    UINT8_T = 'uint8_t'
    UINT16_T = 'uint16_t'
    UINT32_T = 'uint32_t'
    UINT64_T = 'uint64_t'
    HALF = 'half'
    FLOAT = 'float'
    字符串 = 'std::string'
    布尔 = 'bool'
    任意 = 'std::any'
    自动 = 'auto'
    空指针 = 'void*'


class 指针:
    """
    表示 C++ 指针类型的包装类。
    """
    def __init__(self, 基础类型) -> None:
        self.基础类型 = 基础类型

    def __str__(self) -> str:
        return f'{self.基础类型}*'


class 代码块:
    """
    用于生成 C++ 代码块的上下文管理器（包含大括号）。
    """
    def __init__(self, 编译器) -> None:
        self.编译器 = 编译器

    def __enter__(self, *args, **kwargs):
        self.编译器.添加代码('{')
        self.编译器.进入作用域()

    def __exit__(self, *args, **kwargs):
        self.编译器.退出作用域()
        self.编译器.添加代码('}\n')


class C代码:
    """
    表示单行 C++ 代码，主要负责缩进处理。
    """
    def __init__(self, 代码: str, 层级: int) -> None:
        self.代码 = 代码
        self.层级 = 层级

    def __str__(self) -> str:
        return '  ' * self.层级 + self.代码


class C获取下标:
    """
    表示 C++ 数组或 Vector 的下标访问表达式。
    """
    def __init__(self, 变量, 下标) -> None:
        self.变量 = 变量
        self.下标 = 下标

    def __str__(self) -> str:
        return f'{self.变量}[{转C字符串(self.下标)}]'


class C获取属性:
    """
    表示 C++ 对象属性或成员函数访问表达式。
    自动处理指针 -> 以及对象 . 的访问差异。
    """
    def __init__(self, 变量, 属性) -> None:
        self.变量 = 变量
        self.属性 = 属性

    def __str__(self) -> str:
        if isinstance(self.变量, C变量):
            if self.变量.类型名.endswith('*'):
                return f'{self.变量}->{self.属性}'
        return f'{self.变量}.{self.属性}'


class C函数调用:
    """
    表示 C++ 函数调用表达式。
    """
    def __init__(self, 函数名, 参数字符串, 返回C类型=None) -> None:
        self.函数名 = 函数名
        self.参数字符串 = 参数字符串
        self.返回C类型 = 返回C类型

    def __str__(self) -> str:
        return f'{self.函数名}({self.参数字符串})'


class C布尔:
    """
    表示 C++ 布尔值 (true/false)。
    """
    def __init__(self, v) -> None:
        self.v = v

    def __str__(self) -> str:
        return 'true' if self.v else 'false'


def 执行额外函数(函数列表: List, *args):
    """
    执行额外的类型转换函数列表，用于扩展类型系统的灵活性。
    """
    for fn in 函数列表:
        ret = fn(*args)
        if ret is not None:
            return ret
    return None


EXTRA_PY_TO_CTYPES_FUNCTIONS = []
PY_TO_CTYPES_MAP = {
    int: ctypes.c_int64,
    float: ctypes.c_float,
    str: ctypes.c_char_p,
    bool: ctypes.c_bool,
    指针: ctypes.c_void_p,
}


def Python类型转ctypes(py_type):
    """
    将 Python 类型转换为 ctypes 类型，用于函数签名定义。
    """
    ret = 执行额外函数(EXTRA_PY_TO_CTYPES_FUNCTIONS, py_type)
    if ret is not None:
        return ret

    ret = 全局上下文.类型映射表.get(py_type)
    if ret is not None and ret.ctypes类型 is not None:
        return ret.ctypes类型

    origin = get_origin(py_type)
    args = get_args(py_type)

    if origin is list and args:
         elem_type = args[0]
         return ctypes.POINTER(Python类型转ctypes(elem_type))

    return PY_TO_CTYPES_MAP.get(py_type)


EXTRA_PY_TO_C_FUNCTIONS = []
PY_TO_C_MAP = {
    int: Cpp类型.INT64_T,
    float: Cpp类型.FLOAT,
    str: Cpp类型.字符串,
    bool: Cpp类型.布尔,
    指针: Cpp类型.空指针,
}


def Python类型转C类型(py_type, 类型实例=None):
    """
    将 Python 类型转换为 C++ 类型字符串。
    支持基础类型、List[T]、Dict[K, V] 以及自定义映射类型。
    
    :param py_type: Python 类型对象 (如 int, List[int])
    :param 类型实例: 类型实例 (可选)，用于推断返回类型明确的函数调用等
    """
    ret = 执行额外函数(EXTRA_PY_TO_C_FUNCTIONS, py_type)
    if ret is not None:
        return ret

    ret = 全局上下文.类型映射表.get(py_type)
    if ret is not None:
        return ret.目标类型

    # 1. 基础类型
    ret = PY_TO_C_MAP.get(py_type)
    if ret is not None:
        return ret

    origin = get_origin(py_type)
    args = get_args(py_type)

    if origin is Union:
        return Cpp类型.任意

    # 2. List[...] -> std::vector<...>
    if origin is list:
        if args:
            elem_type = args[0]
            return f'std::vector<{Python类型转C类型(elem_type)}>'

    # 3. Dict[K, V] -> std::unordered_map<K, V>
    if origin is dict:
        if len(args) == 2:
            key_type = Python类型转C类型(args[0])
            val_type = Python类型转C类型(args[1])
            return f"std::unordered_map<{key_type}, {val_type}>&"

    # 4. 直接传入的字符串类型名称 (例如 'int')
    if isinstance(py_type, str):
        return py_type

    if py_type is C布尔:
        return Cpp类型.布尔

    # 5. 特殊处理：如果类型实例是函数调用且已知返回类型
    if isinstance(类型实例, C函数调用) and 类型实例.返回C类型 is not None:
        return 类型实例.返回C类型

    raise TypeError(f"Unsupported type: {py_type}")


class 列表初始化列表:
    """
    表示 C++ 的初始化列表 {e1, e2, ...}，用于 std::vector 初始化。
    """
    def __init__(
            self,
            代码: str,
            类型名: str,
            长度: int) -> None:
        self.代码 = 代码
        self.类型名 = 类型名
        self.长度 = 长度

    def __str__(self) -> str:
        return self.代码


def 从列表构建初始化列表(value: List):
    """
    将 Python List 转换为 C++ 初始化列表字符串。
    会自动检查元素类型一致性。
    """
    if not value:
        return 列表初始化列表('{}', 'auto', 0)

    data_types = []
    init_items = []
    for v in value:
        dtype = type(v)
        data_types.append(dtype)
        init_items.append(转C字符串(v))
    
    # 构建初始化列表字符串
    init_list_str = '{' + ','.join(init_items) + '}'

    # 一致性检查：目前只检查基本 Python 类型是否一致
    # 对于混合了 C变量 或 C函数调用 的情况，检查比较宽松
    first_type = data_types[0]
    if not all(t == first_type for t in data_types):
         raise 类型不一致错误(f"List elements must have the same type, got {set(data_types)}")

    type_name = 'auto'
    if value:
         # 根据第一个元素值推断 C++ 类型
         type_name = Python类型转C类型(first_type, value[0])

    return 列表初始化列表(init_list_str, type_name, len(value))


class 字典初始化列表:
    """
    表示 C++ 的字典初始化列表 {{k1, v1}, {k2, v2}, ...}，用于 std::unordered_map。
    """
    def __init__(
            self,
            代码: str,
            键类型名: str,
            值类型名: str) -> None:
        self.代码 = 代码
        self.键类型名 = 键类型名
        self.值类型名 = 值类型名

    def __str__(self) -> str:
        return self.代码


def 从字典构建初始化列表(value: dict):
    """
    将 Python Dict 转换为 C++ 初始化列表字符串。
    要求 key 和 value 类型一致。
    """
    if not value:
        return 字典初始化列表('{}', 'auto', 'auto')

    code_items = []
    key_types = []
    value_types = []
    
    # 需要捕获第一个 key/value 实例来解析类型
    first_key = None
    first_value = None
    
    for i, (k, v) in enumerate(value.items()):
        if i == 0:
            first_key = k
            first_value = v
            
        key_type = type(k)
        value_type = type(v)
        key_types.append(key_type)
        value_types.append(value_type)
        code_items.append(f'{{ {转C字符串(k)}, {转C字符串(v)} }}')

    first_key_type = key_types[0]
    if not all(t == first_key_type for t in key_types):
        raise 类型不一致错误(f"Dict keys must have the same type")
        
    first_value_type = value_types[0]
    if not all(t == first_value_type for t in value_types):
         raise 类型不一致错误(f"Dict values must have the same type")

    init_list_str = '{' + ','.join(code_items) + '}'

    key_type_name = Python类型转C类型(first_key_type, first_key)
    value_type_name = Python类型转C类型(first_value_type, first_value)

    return 字典初始化列表(init_list_str, key_type_name, value_type_name)


class C变量:
    """
    表示一个 C++ 变量。
    包含变量类型、名称、生成的 C 变量名以及初始化代码生成逻辑。
    """
    def __init__(self, 类型名: str, 名称: str, 是否参数: bool, 默认值=None) -> None:
        self.类型名 = 类型名
        self.名称 = 名称
        self.C名称 = 生成变量ID(名称)
        self.是否参数 = 是否参数
        self.默认值 = 默认值

    def __str__(self):
        return self.C名称

    @property
    def decltype(self):
        return f'decltype({self})'

    def 初始化代码(self, initial_value, cast_type: str | None = None):
        """生成变量声明和初始化代码"""
        if cast_type:
            return f'{self.类型名} {self.C名称} = (({cast_type})({initial_value}));'
        else:
            return f'{self.类型名} {self.C名称} = {initial_value};'
