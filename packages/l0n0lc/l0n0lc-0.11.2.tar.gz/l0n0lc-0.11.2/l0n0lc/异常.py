

class Jit错误(Exception):
    """JIT 基础异常类"""
    pass

class 编译错误(Jit错误):
    """当 C++ 编译失败时抛出"""
    pass

class 类型不匹配错误(Jit错误):
    """当类型不匹配预期时抛出"""
    pass

class 类型不一致错误(类型不匹配错误):
    """当容器（如列表）中的元素类型不一致时抛出"""
    pass
