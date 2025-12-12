
import os
from typing import Callable, Optional
from .Py转Cpp转译器 import Py转Cpp转译器
from .cpp编译器 import Cpp编译器
from .工具 import 全局上下文

def 即时编译(
    转译器类=None, 
    编译器类=None, 
    总是重编: bool = False, 
    可执行文件名: Optional[str] = None
):
    """
    JIT (即时编译) 装饰器。
    
    能够将受支持的 Python 函数转换为 C++ 代码，编译为动态库并加载执行。
    大大提高计算密集型任务的性能。

    :param 转译器类: 自定义转译器类 (可选)
    :param 编译器类: 自定义编译器类 (可选)
    :param 总是重编: 是否每次运行都强制重新编译 (默认为 False，利用缓存)
    :param 可执行文件名: 如果指定，将编译为独立的可执行文件而不是动态库
    """
    def 装饰器(fn: Callable):
        _编译器类 = 编译器类 or Cpp编译器
        _转译器类 = 转译器类 or Py转Cpp转译器
        
        编译器 = _转译器类(fn, _编译器类(), 可执行文件名)
        库文件名 = 编译器.获取库文件名()
        
        库路径 = f'{全局上下文.工作目录}/{库文件名}'
        
        # 检查缓存：如果文件存在且不需要强制重编，则跳过编译步骤
        if 总是重编 or not os.path.exists(库路径):
            编译器.编译()
        else:
            # 即使加载缓存，也需要分析 AST 以确定函数签名（特别是返回类型）
            编译器.分析()
            
        编译器.加载库()
        return 编译器
    return 装饰器

jit = 即时编译