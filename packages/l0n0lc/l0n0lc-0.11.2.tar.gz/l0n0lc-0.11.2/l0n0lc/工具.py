import re
import os
from typing import List, Optional, Any, Dict, Set

def 十进制转进制(value: int, base: int, digits="0123456789ABCDEF") -> str:
    """将十进制整数转换为任意进制字符串"""
    if value == 0:
        return "0"
    result = ""
    is_negative = value < 0
    value = abs(value)
    while value > 0:
        value, remainder = divmod(value, base)
        result = digits[remainder] + result
    return ("-" if is_negative else "") + result


class Cpp函数映射:
    """
    存储 Python 函数到 C++ 函数的映射关系。
    包含目标函数名（或代码生成器）、头文件依赖和库文件依赖。
    """
    def __init__(
            self, 目标函数: str,
            包含目录: Optional[List[str]] = None,
            库: Optional[List[str]] = None,
            库目录: Optional[List[str]] = None) -> None:
        self.目标函数 = 目标函数
        self.包含目录 = 包含目录 or []
        self.库 = 库 or []
        self.库目录 = 库目录 or []

    def __str__(self) -> str:
        return self.目标函数


class Cpp类型映射:
    """
    存储 Python 类型到 C++ 类型的映射关系。
    包含目标类型名、ctypes 类型以及相关的编译依赖。
    """
    def __init__(
            self, 目标类型: str,
            包含目录: Optional[List[str]] = None,
            库: Optional[List[str]] = None,
            库目录: Optional[List[str]] = None,
            ctypes类型=None) -> None:
        self.目标类型 = 目标类型
        self.包含目录 = 包含目录 or []
        self.库 = 库 or []
        self.库目录 = 库目录 or []
        self.ctypes类型 = ctypes类型

    def __str__(self) -> str:
        return self.目标类型


class 全局上下文:
    """
    全局上下文，存储所有的函数/类型映射配置、内置函数列表以及全局编译设置。
    """
    直接调用函数集: Set = set() # 直接在 Python 端执行的函数集合 (如 range)
    函数映射表: Dict[Any, Cpp函数映射] = {} # 函数映射表
    类型映射表: Dict[Any, Cpp类型映射] = {} # 类型映射表
    包含集合: Set = set()
    链接库集合: Set = set()
    最大变量ID = 0
    Python内置映射 = {}
    使用Unicode = True
    工作目录 = './l0n0lcoutput' # 编译输出目录

    @staticmethod
    def 缓存直接调用():
        全局上下文.直接调用函数集.add(range)

    @staticmethod
    def 添加内置映射(v):
        全局上下文.Python内置映射[v.__name__] = v

    @staticmethod
    def 初始化内置():
        # 初始化常用的 Python 内置函数映射
        for v in [int, float, str, bool, range, complex, set, tuple, list, dict,
                  print, input, abs, round, pow, divmod, sum, min, max,
                  isinstance, len, open]:
            全局上下文.添加内置映射(v)


全局上下文.初始化内置()


def 可直接调用(fn):
    """
    装饰器：注册一个 Python 函数为"直接调用"模式。
    转译器遇到此函数时不会尝试转换为 C++ 调用，而是回调 Python 解释器执行。
    """
    全局上下文.直接调用函数集.add(fn)
    return fn


def 映射函数(
        mapped_function,
        包含目录: Optional[List[str]] = None,
        库: Optional[List[str]] = None,
        库目录: Optional[List[str]] = None):
    """
    装饰器：将 Python 函数映射到 C++ 代码片段或函数。
    
    :param mapped_function: 被映射的原 Python 函数
    :param 包含目录: 需要包含的头文件
    """
    def decorator(target):
        全局上下文.函数映射表[mapped_function] = Cpp函数映射(target, 包含目录, 库, 库目录)
        return target
    return decorator


def 映射类型(mapped_type,
             包含目录: Optional[List[str]] = None,
             库: Optional[List[str]] = None,
             库目录: Optional[List[str]] = None,
             ctypes类型=None):
    """
    装饰器：将 Python 类型映射到 C++ 类型。
    """
    def decorator(target):
        全局上下文.类型映射表[target] = Cpp类型映射(mapped_type, 包含目录, 库, 库目录, ctypes类型)
        return target
    return decorator


def 含非ASCII字符(s: str) -> bool:
    """检查字符串是否包含非 ASCII 字符（如中文）"""
    return bool(re.search(r'[^A-Za-z0-9_]', s))


def 生成变量ID(original_name: Optional[str] = None) -> str:
    """
    生成合法的 C++ 变量/函数标识符。
    如果 original_name 是 ASCII 且 use_unicode=True 则直接使用，
    否则生成唯一的临时 ID。
    """
    if original_name is not None and (全局上下文.使用Unicode or not 含非ASCII字符(original_name)):
        return original_name
    ret = f'_{全局上下文.最大变量ID}'
    全局上下文.最大变量ID += 1
    return ret


def 确保目录存在(dir_name: str):
    """确保目录存在，不存在则创建"""
    if os.path.exists(dir_name):
        return
    os.makedirs(dir_name, exist_ok=True)


def 转C字符串(v) -> str:
    """将 Python 值转换为 C++ 字符串表示"""
    if isinstance(v, str):
        return f'u8"{v}"'
    return str(v)

# Backward compatibility (向下兼容别名)
toCString = 转C字符串
