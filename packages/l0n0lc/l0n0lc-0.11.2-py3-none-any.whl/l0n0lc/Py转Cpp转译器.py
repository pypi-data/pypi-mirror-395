
import os
import ast
import hashlib
import inspect
import ctypes
from typing import Callable, Any, List, Dict, Set, Optional, Tuple, Union

from .cpp类型 import (
    C变量, Cpp类型, 代码块, C代码, C获取下标, C获取属性, 
    C函数调用, C布尔, Python类型转C类型, Python类型转ctypes, 
    从列表构建初始化列表, 从字典构建初始化列表, 
    列表初始化列表, 字典初始化列表
)
from .异常 import 类型不一致错误, Jit错误
from .std_vector import 标准列表
from .std_map import 标准无序映射
from .工具 import (
    全局上下文, 含非ASCII字符, 确保目录存在, Cpp类型映射, Cpp函数映射
)
from .cpp编译器 import Cpp编译器


class Py转Cpp转译器(ast.NodeVisitor):
    """
    AST 访问者类，负责将 Python 函数 AST 转换为 C++ 代码并进行编译。
    核心功能包括类型推断、代码生成、依赖管理和 C++ 编译器调用。
    """
    def __init__(self, 目标函数: Callable, 编译器: Cpp编译器, 可执行文件名: Optional[str] = None) -> None:
        """
        初始化转译器。
        
        :param 目标函数: 需要编译的 Python 函数对象
        :param 编译器: CppCompiler 实例，用于处理后续的 C++ 编译工作
        :param 可执行文件名: 如果提供，将编译为可执行文件而非动态库
        """
        self.目标函数 = 目标函数
        self.编译器 = 编译器
        self.可执行文件名 = 可执行文件名
        self.源代码 = inspect.getsource(目标函数)
        # 计算源码哈希值，用于缓存文件名生成
        self.代码哈希 = hashlib.blake2s(self.源代码.encode(), digest_size=8).hexdigest()
        
        if inspect.isclass(目标函数):
            import sys
            module = sys.modules.get(目标函数.__module__)
            self.全局变量 = module.__dict__ if module else {}
            self.是否为类 = True
            self.类成员变量: Dict[str, str] = {} # Python Name -> C Type
            self.构造函数 = None
        else:
            self.全局变量 = 目标函数.__globals__
            self.是否为类 = False

        self.本地变量 = {}
        self.参数变量 = {}
        self.ctypes参数类型 = []  # 保存参数的 ctypes 类型，用于 ctypes 调用
        self.ctypes返回类型 = ctypes.c_voidp # 保存返回值的 ctypes 类型
        self.类方法列表: List[Dict[str, Any]] = [] # 存储类方法信息
        self.作用域变量: List[Dict[str, Any]] = [{}] # 变量作用域栈
        self.当前作用域层级 = 0
        self.依赖函数: List['Py转Cpp转译器'] = [] # 递归依赖的其他 JIT 函数
        self.代码序列 = [] # 生成的 C++ 代码行
        self.代码块上下文 = 代码块(self) # 代码块上下文管理器
        self.正在直接调用 = False # 标记是否正在进行直接 Python 调用
        self.正在构建参数 = False # 标记是否正在处理函数参数
        
        self.包含头文件: Set[str] = {'<stdint.h>', '<string.h>'} # 需要包含的头文件
        self.链接库: Set[str] = set() # 需要链接的库
        self.库搜索目录: Set[str] = set() # 库搜索目录
        
        # 记录 List 类型的参数，用于将其拆解为指针和长度两个参数传递
        # 格式: 参数名 -> (指针变量, 长度变量)
        self.列表参数映射: Dict[str, Tuple[C变量, C变量]] = {} 

        self.函数名 = 目标函数.__name__
        
        if 可执行文件名:
            self.C函数名 = 'main' # 如果是可执行文件，入口函数为 main
        else:
            if 含非ASCII字符(self.函数名):
                # 防止中文函数名导致的编码问题，使用 hex 编码
                self.C函数名 = f'function_{self.函数名.encode().hex()}'
            else:
                self.C函数名 = self.函数名
                
        file_path = inspect.getfile(目标函数)
        file_name = os.path.split(file_path)[1]
        file_name_hash = hashlib.blake2s(file_path.encode(), digest_size=8).hexdigest()
        # 文件前缀，包含原文件名哈希、文件名、函数名，用于区分
        self.文件前缀 = f'{file_name_hash}_{file_name}_{self.函数名}_@'
        
        self.返回类型 = 'void' # 默认 C++ 返回类型
        self.目标库 = None # ctypes 加载的动态库对象
        self.cpp函数 = None # 加载后的 C++ 函数对象, 如果是类，这里可能不需要或者指向构造函数包装器

    def 分析(self):
        """
        解析 Python 源码，遍历 AST 以分析类型和依赖，但不进行编译。
        此步骤对于推断返回类型和参数类型至关重要。
        """
        # 清理源码缩进，防止因函数嵌套在类或其他块中导致的缩进错误
        lines = self.源代码.split('\n')
        cleaned_lines = []
        first_non_whitespace = None
        
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                first_non_whitespace = len(line) - len(stripped)
                break
        
        if first_non_whitespace is not None:
            for line in lines:
                stripped = line.lstrip()
                if not stripped:
                    continue
                cleaned_lines.append(line[first_non_whitespace:])
        
        cleaned_source = '\n'.join(cleaned_lines)
        if not cleaned_source: # 处理空函数的情况
             cleaned_source = "def dummy(): pass"

        tree = ast.parse(cleaned_source, mode='exec')
        self.visit(tree)

    def 编译(self):
        """
        执行完整的编译流程：分析 -> 生成 C++ 代码 -> 编译为动态库/可执行文件。
        """
        self.分析()
        
        # 收集依赖文件
        cpp_files = {f'{全局上下文.工作目录}/{self.获取cpp文件名()}'}
        for dep in self.依赖函数:
            self.包含头文件.add(f'"{dep.获取头文件名()}"')
            cpp_files.add(f'{全局上下文.工作目录}/{dep.获取cpp文件名()}')
            
        self.保存代码到文件()
        
        # 配置编译器
        self.编译器.添加库目录(list(self.库搜索目录))
        self.编译器.添加库(list(self.链接库))
        
        output_path = f'{全局上下文.工作目录}/{self.获取库文件名()}'
        
        if self.可执行文件名:
            self.编译器.添加编译选项("-O2")
            self.编译器.编译文件(list(cpp_files), output_path)
        else:
            self.编译器.编译共享库(list(cpp_files), output_path)

    def 添加代码(self, code: str):
        """添加一行 C++ 代码"""
        self.代码序列.append(C代码(code, self.当前作用域层级))

    def 抛出错误(self, message: str, node: Union[ast.stmt, ast.expr, ast.arg]):
         """抛出带行号的编译错误"""
         line_no = node.lineno if hasattr(node, 'lineno') else '?'
         raise Jit错误(f"Line {line_no}: {message}")

    def 进入作用域(self):
        """进入新的作用域（如 if/for 块内部）"""
        self.作用域变量.append({})
        self.当前作用域层级 += 1

    def 退出作用域(self):
        """退出当前作用域"""
        self.作用域变量.pop()
        self.当前作用域层级 -= 1

    def 获取C变量(self, name: str) -> Optional[Any]:
        """从当前及上层作用域查找 C 变量"""
        for i in range(self.当前作用域层级, -1, -1):
            v = self.作用域变量[i].get(name)
            if v is not None:
                return v
        return None

    def 添加C变量(self, variable: C变量):
        """在当前作用域注册 C 变量"""
        self.作用域变量[self.当前作用域层级][variable.名称] = variable

    def 获取值(self, value):
        """
        将 AST 节点转换为对应的值或 C++ 表达式字符串。
        处理常量、变量名、属性访问、函数调用、运算表达式等。
        """
        if isinstance(value, ast.Constant):
            if isinstance(value.value, bool):
                return C布尔(value.value)
            return value.value

        if isinstance(value, ast.Name):
            # 1. 查找 Python 内置对象
            v = 全局上下文.Python内置映射.get(value.id)
            if v is not None:
                return v
            # 2. 查找本地 Python 变量 (直接执行时使用)
            v = self.本地变量.get(value.id)
            if v is not None:
                return v
            # 3. 查找 C 变量
            v = self.获取C变量(value.id)
            if v is not None:
                return v
            # 4. 查找参数变量
            v = self.参数变量.get(value.id)
            if v is not None:
                return v
            # 5. 查找全局变量
            return self.全局变量.get(value.id)

        if isinstance(value, ast.Attribute):
            obj = self.获取值(value.value)
            if isinstance(obj, (C变量, Cpp类型映射)):
                return C获取属性(obj, value.attr)
            if obj is None:
                self.抛出错误(f'Name not found: {value.value}', value)
            return getattr(obj, value.attr)

        if isinstance(value, ast.UnaryOp):
            operand = self.获取值(value.operand)
            if isinstance(value.op, ast.UAdd):
                return f'(+{operand})'
            if isinstance(value.op, ast.USub):
                return f'(-{operand})'
            if isinstance(value.op, ast.Not):
                return f'(!{operand})'
            if isinstance(value.op, ast.Invert):
                return f'(~{operand})'

        if isinstance(value, ast.BoolOp):
             values = [f'({self.获取值(v)})' for v in value.values]
             if isinstance(value.op, ast.And):
                 return '&&'.join(values)
             if isinstance(value.op, ast.Or):
                 return '||'.join(values)

        if isinstance(value, ast.IfExp):
            test = self.获取值(value.test)
            body = self.获取值(value.body)
            orelse = self.获取值(value.orelse)
            return f'(({test}) ? ({body}) : ({orelse}))'

        if isinstance(value, ast.Compare):
            return self.计算比较(value)

        if isinstance(value, ast.BinOp):
            return self.计算二元运算(value)

        # 处理 List 字面量
        if isinstance(value, ast.List):
            l = [self.获取值(e) for e in value.elts]
            try:
                return 从列表构建初始化列表(l)
            except 类型不一致错误 as e:
                self.抛出错误(str(e), value)

        # 处理 Tuple 字面量
        if isinstance(value, ast.Tuple):
            l = [self.获取值(e) for e in value.elts]
            if not self.正在构建参数:
                 try:
                     # 在 C++ 中，Tuple 通常也转为 list/vector 处理，除非是 std::pair
                     # 这里尝试构建初始化列表
                     return 从列表构建初始化列表(l)
                 except 类型不一致错误:
                     pass
            return tuple(l)

        # 处理 Dict 字面量
        if isinstance(value, ast.Dict):
            d = {self.获取值(k): self.获取值(v) for k, v in zip(value.keys, value.values)}
            try:
                return 从字典构建初始化列表(d)
            except 类型不一致错误 as e:
                self.抛出错误(str(e), value)

        if isinstance(value, ast.Call):
            return self.处理调用(value)

        if isinstance(value, ast.Subscript):
            return self.获取下标(value)
            
        return None

    def 计算比较(self, node: ast.Compare) -> Any:
        # 处理比较运算 (==, !=, <, >, <=, >=)
        left = self.获取值(node.left)
        ret = '('
        first = True
        for op, comp in zip(node.ops, node.comparators):
            left_val = left if first else ''
            right = self.获取值(comp)
            
            op_str = ''
            if isinstance(op, ast.Eq): op_str = '=='
            elif isinstance(op, ast.NotEq): op_str = '!='
            elif isinstance(op, ast.Lt): op_str = '<'
            elif isinstance(op, ast.LtE): op_str = '<='
            elif isinstance(op, ast.Gt): op_str = '>'
            elif isinstance(op, ast.GtE): op_str = '>='
            
            if op_str:
                ret += f'({left_val} {op_str} {right})'
            
            left = right
            first = False
            
        if len(node.ops) == 1:
            return ret[1:] # 移除前导括号
        return ret + ')'

    def 计算二元运算(self, node: Union[ast.BinOp, ast.AugAssign]):
        """处理二元运算 (+, -, *, /, %, <<, >>, &, |, ^)"""
        if isinstance(node, ast.BinOp):
            left = self.获取值(node.left)
            right = self.获取值(node.right)
            op = node.op
        elif isinstance(node, ast.AugAssign):
            left = self.获取值(node.target)
            right = self.获取值(node.value)
            op = node.op
        else:
             return None

        op_str = ''
        if isinstance(op, ast.Add): op_str = '+'
        elif isinstance(op, ast.Sub): op_str = '-'
        elif isinstance(op, ast.Mult): op_str = '*'
        elif isinstance(op, (ast.Div, ast.FloorDiv)): op_str = '/'
        elif isinstance(op, ast.Mod): op_str = '%'
        elif isinstance(op, ast.BitAnd): op_str = '&'
        elif isinstance(op, ast.BitOr): op_str = '|'
        elif isinstance(op, ast.BitXor): op_str = '^'
        elif isinstance(op, ast.LShift): op_str = '<<'
        elif isinstance(op, ast.RShift): op_str = '>>'
        
        if op_str:
            return f'({left} {op_str} {right})'
        
        self.抛出错误(f"Unsupported operator: {type(op).__name__}", node)

    def 构建参数字符串(self, args: List[ast.expr]):
        arg_list = [str(self.获取值(arg)) for arg in args]
        return ','.join(arg_list)

    def 处理调用(self, node: ast.Call):
        func = self.获取值(node.func)

        # 1. 类型实例化 (例如 CppVectorInt())
        if inspect.isclass(func):
            c_type_map = 全局上下文.类型映射表.get(func)
            if c_type_map:
                self.包含头文件.update(c_type_map.包含目录)
                self.链接库.update(c_type_map.库)
                self.库搜索目录.update(c_type_map.库目录)
                args_str = self.构建参数字符串(node.args)
                # 构造函数调用
                return C函数调用(c_type_map.目标类型, args_str, c_type_map.目标类型)

        # 2. 直接调用 (例如 range(), print()) - 缓存在 GlobalContext 中
        if func in 全局上下文.直接调用函数集:
            args = [self.获取值(arg) for arg in node.args]
            self.正在直接调用 = True
            try:
                return func(*args)
            except Exception as e:
                 self.抛出错误(f"Error during direct call to {func.__name__}: {str(e)}", node)

        # 3. 映射的 C++ 函数
        mapped_func = 全局上下文.函数映射表.get(func)
        if mapped_func:
            args = [self.获取值(arg) for arg in node.args]
            self.包含头文件.update(mapped_func.包含目录)
            self.链接库.update(mapped_func.库)
            self.库搜索目录.update(mapped_func.库目录)
            
            # 如果目标是可调用的 (如宏函数生成器)，则直接调用生成代码
            if callable(mapped_func.目标函数):
                 return mapped_func.目标函数(*args)
            return C函数调用(mapped_func.目标函数, self.构建参数字符串(node.args))

        if not isinstance(func, Callable) and not isinstance(func, C获取属性):
             self.抛出错误(f"Cannot call object '{ast.dump(node.func)}'", node)
        
        if node.keywords:
             self.抛出错误("Keyword arguments not supported in C++ translation", node)

        args_str = self.构建参数字符串(node.args)
        
        # 4. 调用其他 JIT 编译的函数
        if isinstance(func, Py转Cpp转译器):
            self.依赖函数.append(func)
            return C函数调用(func.C函数名, args_str)
        # 5. C++ 对象方法调用
        elif isinstance(func, C获取属性):
            return C函数调用(func, args_str)
        else:
            # 6. 如果依赖是普通 Python 函数，尝试递归编译
            try:
                dep_compiler = self.__class__(func, self.编译器)
                dep_compiler.编译()
                self.依赖函数.append(dep_compiler)
                return C函数调用(func.__name__, args_str)
            except Exception as e:
                self.抛出错误(f"Failed to compile dependency {func.__name__}: {str(e)}", node)

    def 获取下标(self, node: ast.Subscript):
        """处理下标访问 obj[index]"""
        obj = self.获取值(node.value)
        slice_node = node.slice
        
        if isinstance(slice_node, ast.Slice):
            self.抛出错误("Slicing not supported for C++ vectors yet", node)
            
        index = self.获取值(slice_node)
        
        # 处理类型提示中的下标, 如 Union[int, float]
        if obj is Union:
            return Union[index]
        if obj is List:
            return List[index]
        if obj is Dict:
            if isinstance(index, tuple):
                 return Dict[index[0], index[1]]
            return Dict[index]
            
        # C++ 数组/Vector 下标访问
        return C获取下标(obj, index)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        if node.name != self.函数名:
             self.抛出错误(f"Nested classes not supported: {node.name}", node)

        # 1. 扫描成员变量
        for stmt in node.body:
             if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                  py_type = self.获取值(stmt.annotation)
                  c_type = Python类型转C类型(py_type)
                  self.类成员变量[stmt.target.id] = str(c_type)
        
        # 2. 访问方法
        for stmt in node.body:
             if isinstance(stmt, ast.FunctionDef):
                  # 重置参数变量，避免方法间干扰
                  self.参数变量 = {}
                  self.visit(stmt)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if self.是否为类:
             # 处理类方法
             is_init = node.name == '__init__'
             # 构造函数名为类名，否则为原名
             method_name = self.函数名 if is_init else node.name
             c_ret_type = ''
             
             # 临时保存 global code sequence
             original_code_seq = self.代码序列
             self.代码序列 = []
             
             # 参数处理
             args_node = node.args
             original_args = list(args_node.args)
             
             # 检查 self
             self_arg_name = None
             if original_args:
                 first_arg = original_args[0]
                 if first_arg.arg == 'self':
                     self_arg_name = first_arg.arg
                     # 从参数列表中移除 self，使其不出现在 C++ 参数签名中
                     args_node.args = original_args[1:]
                 else:
                     # 静态方法? 暂不支持，假设必须有 self
                     pass
             
             # 为方法体创建新的作用域
             with self.代码块上下文:
                 # 注册 self 变量 (作为 this 指针)
                 if self_arg_name:
                     self_var = C变量(f'{self.函数名}*', self_arg_name, False)
                     self_var.C名称 = 'this' # 关键：映射到 C++ this
                     self.添加C变量(self_var)

                 self.visit_arguments(args_node)
                 
                 for stmt in node.body:
                     self.visit(stmt)
             
             # 获取生成的代码块 (移除首尾的大括号，因为代码块上下文加了一层，
             # 但我们可能想要更精细的控制，或者直接使用包含大括号的代码块)
             # 代码块上下文会在 exit 时添加 '}' 和 entry 时添加 '{'
             # self.代码序列 现在包含了 { body }
             method_body = list(self.代码序列)
             
             # 恢复 global code sequence
             self.代码序列 = original_code_seq
             
             # 确定返回类型
             if is_init:
                  c_ret_type = '' # 构造函数无返回类型部分
             else:
                  if isinstance(node.returns, ast.Name):
                      ret_py_type = self.获取值(node.returns)
                      c_ret_type = str(Python类型转C类型(ret_py_type))
                  elif node.returns is None:
                      c_ret_type = 'void'
                  else:
                      c_ret_type = 'auto'
             
             # 构建参数字符串
             # visit_arguments 填充了 self.参数变量 (current scope)
             # 但这里的 self.参数变量 是在 with 代码块上下文 中填充的
             # 且 visit_arguments 对 self.参数变量 的修改是局部的吗？
             # 不，self.参数变量 是 global 的 (function scope).
             # 但是 visit_arguments 会清理旧的吗？ 不会。
             # 我们在 visit_FunctionDef 开始时应该清理参数变量?
             # 或者，我们应该使用一个临时的参数收集器。
             
             # 修正：我们需要从 args_node 重建参数字符串，因为 visit_arguments 逻辑较复杂
             # 简单起见，我们假设 visit_arguments 正确填充了 self.参数变量
             # 但我们需要区分哪些是当前方法的参数。
             # 實際上 `visit_arguments` 會把參數加到 `self.参数变量`。
             # 為了避免污染，我们在进入 method 前应该清空 参数变量?
             # 或者更好的是，visit_arguments logic should be reused but careful.
             
             # 让我们重新审视参数收集。
             # 在 class mode，每个 method 是一次独立的 "编译"。
             # 我们应该每次 method start reset self.参数变量。
             
             pass # Logic continued in next block adjustment (I need to reset state)
             
             # 实际上，上面的 `args_node.args = original_args[1:]` 修改了 AST 节点
             # 这可能影响后续访问？AST 通常是引用的。应该 copy。
             # 但这里只用一次。
             
             # 收集参数定义字符串
             # 因为 参数变量 是 Dict, 我们需要只获取本次新增的?
             # 简单处理：每次方法开始前清空 self.参数变量
             
             self.类方法列表.append({
                 'name': method_name,
                 'ret_type': c_ret_type,
                 'body': method_body,
                 'is_init': is_init,
                 'params': self._构建当前参数列表字符串()
             })
             
             return

        with self.代码块上下文:
            self.visit_arguments(node.args)
            
            # 在函数体开始处，使用指针和长度重建 std::vector (如果存在 List 参数)
            for param_name, (ptr_var, len_var) in self.列表参数映射.items():
                original_var = self.参数变量[param_name]
                # 重建代码: std::vector<T> vec(ptr, ptr + len);
                self.添加代码(f'{original_var.类型名} {original_var.C名称}({ptr_var.C名称}, {ptr_var.C名称} + {len_var.C名称});')

            for stmt in node.body:
                self.visit(stmt)
                
        # 分析返回类型
        if isinstance(node.returns, ast.Name):
            ret_py_type = self.获取值(node.returns)
            self.返回类型 = Python类型转C类型(ret_py_type)
            if not self.可执行文件名:
                self.ctypes返回类型 = Python类型转ctypes(ret_py_type)
        elif node.returns is None:
            self.返回类型 = 'void'
            self.ctypes返回类型 = None
        else:
            self.返回类型 = 'auto'

    def visit_arguments(self, node: ast.arguments) -> Any:
        self.正在构建参数 = True
        
        args = list(node.args)
        if node.vararg:
             # C++ 变长参数处理复杂，暂不支持
             self.抛出错误("*args not supported", node)
             
        for idx, arg in enumerate(args):
            default_val = None
            if idx >= len(args) - len(node.defaults):
                 default_val = node.defaults[idx - (len(args) - len(node.defaults))]
            self.处理参数(arg, default_val)
            
        self.正在构建参数 = False

    def 处理参数(self, node: ast.arg, default_val=None):
        name = node.arg
        
        if default_val is not None:
             # C++ 默认参数在声明中支持，此处简化处理，暂忽略
             pass

        if node.annotation is None:
            self.抛出错误(f"Argument '{name}' must have type annotation", node)
            
        py_type = self.获取值(node.annotation)
        c_type = Python类型转C类型(py_type)
        
        if c_type is None:
             self.抛出错误(f"Unsupported type {py_type}", node)
             
        # 检测是否为 std::vector 类型 (即 Python 的 List[T])
        # 如果是，则将其拆分为 指针 和 长度 两个参数传递，以兼容 ctypes
        if str(c_type).startswith('std::vector'):
            self.包含头文件.add('<vector>')
            # 提取基础类型 T: std::vector<int> -> int
            base_type = str(c_type)[12:-1] 
            
            ptr_name = f'{name}_ptr'
            len_name = f'{name}_len'
            
            ptr_var = C变量(f'{base_type}*', ptr_name, True)
            len_var = C变量('int64_t', len_name, True)
            
            self.列表参数映射[name] = (ptr_var, len_var)
            
            # 逻辑上的参数变量 (在 C++ 函数内部作为局部变量使用)
            impl_var = C变量(str(c_type), name, False) 
            self.参数变量[name] = impl_var
            
            if not self.可执行文件名:
                 # 设置 ctypes 参数类型
                 ctypes_t = Python类型转ctypes(py_type) 
                 
                 # 强制检查以确保正确映射
                 origin = getattr(py_type, '__origin__', None)
                 args = getattr(py_type, '__args__', [])
                 if origin is list and args:
                      elem_type = args[0]
                      ctypes_elem = Python类型转ctypes(elem_type)
                      self.ctypes参数类型.append(ctypes.POINTER(ctypes_elem))
                      self.ctypes参数类型.append(ctypes.c_int64)
                 else:
                      self.抛出错误(f"Complex list type {py_type} not supported for JIT args", node)
                       
        else:
            var = C变量(str(c_type), name, True)
            self.参数变量[name] = var
            if not self.可执行文件名:
                self.ctypes参数类型.append(Python类型转ctypes(py_type))

    def visit_Return(self, node: ast.Return) -> Any:
        ret_val = self.获取值(node.value) if node.value is not None else ''
        self.添加代码(f'return {ret_val};')

    def visit_If(self, node: ast.If) -> Any:
        test = self.获取值(node.test)
        self.添加代码(f'if ({test})')
        
        with self.代码块上下文:
            for stmt in node.body:
                self.visit(stmt)
                
        if node.orelse:
            self.添加代码('else')
            with self.代码块上下文:
                for stmt in node.orelse:
                    self.visit(stmt)

    def visit_For(self, node: ast.For) -> Any:
        target = self.获取值(node.target)
        if target is None:
            if isinstance(node.target, ast.Name):
                 target = C变量('auto', node.target.id, False)
                 self.添加C变量(target)
            else:
                 self.抛出错误("For loop target must be a name", node)
                 
        iter_node = node.iter
        
        # 处理 range() 循环
        if isinstance(iter_node, ast.Call):
             func = self.获取值(iter_node.func)
             if func is range:
                 args = [self.获取值(arg) for arg in iter_node.args]
                 if len(args) == 1:
                     code = f'for (int64_t {target} = 0; {target} < {args[0]}; ++{target})'
                 elif len(args) == 2:
                     code = f'for (int64_t {target} = {args[0]}; {target} < {args[1]}; ++{target})'
                 elif len(args) == 3:
                     code = f'for (int64_t {target} = {args[0]}; {target} < {args[1]}; {target} += {args[2]})'
                 else:
                     self.抛出错误("Invalid range arguments", node)
             else:
                 # 泛型迭代器
                 call_code = self.处理调用(iter_node)
                 code = f'for (auto {target} : {call_code})'
        # 处理列表/元组字面量循环
        elif isinstance(iter_node, (ast.List, ast.Tuple)):
             l = [self.获取值(e) for e in iter_node.elts]
             init_list = 从列表构建初始化列表(l)
             code = f'for (auto {target} : {init_list})'
        else:
             # 处理可迭代对象循环
             iter_obj = self.获取值(iter_node)
             code = f'for (auto {target} : {iter_obj})'
             
        self.添加代码(code)
        with self.代码块上下文:
            for stmt in node.body:
                self.visit(stmt)

    def visit_Break(self, node: ast.Break):
        self.添加代码('break;')

    def visit_Continue(self, node: ast.Continue):
        self.添加代码('continue;')

    def visit_While(self, node: ast.While):
        test = self.获取值(node.test)
        self.添加代码(f'while ({test})')
        with self.代码块上下文:
            for stmt in node.body:
                self.visit(stmt)

    def visit_Assign(self, node: ast.Assign):
        value = self.获取值(node.value)
        for target in node.targets:
            self._assign(target, value, node)

    def visit_AugAssign(self, node: ast.AugAssign):
        value = self.计算二元运算(node)
        self._assign(node.target, value, node)
        
    def visit_AnnAssign(self, node: ast.AnnAssign):
        value = self.获取值(node.value)
        target_py_type = self.获取值(node.annotation)
        c_type = Python类型转C类型(target_py_type)
        self._assign(node.target, value, node, str(c_type))

    def visit_Expr(self, node: ast.Expr):
        # 处理独立表达式，如函数调用语句
        if isinstance(node.value, ast.Call):
            code = self.处理调用(node.value)
            self.添加代码(f'{code};')

    def _assign(self, target_node, value, context_node, cast_type: str = None):
         target_var = self.获取值(target_node)
         
         # 处理 Python 变量的直接赋值 (仅在 正在直接调用 模式下)
         if self.正在直接调用:
              if isinstance(target_node, ast.Name):
                   self.本地变量[target_node.id] = value
              else:
                   self.抛出错误("Direct assignment only supports simple names", context_node)
              self.正在直接调用 = False
              return

         if target_var is None:
              # 新变量声明
              if isinstance(target_node, ast.Name):
                   if isinstance(value, 字典初始化列表):
                        target_var = 标准无序映射(value, target_node.id, False)
                        self.包含头文件.add('<unordered_map>')
                   elif isinstance(value, 列表初始化列表):
                        target_var = 标准列表(value, target_node.id, False)
                        if value.类型名 == Cpp类型.任意:
                             self.包含头文件.add('<any>')
                   else:
                        target_var = C变量('auto', target_node.id, False)
                   
                   self.添加代码(target_var.初始化代码(value, cast_type))
                   self.添加C变量(target_var)
              else:
                   self.抛出错误("Assignment target must be a name", context_node)
         else:
              # 现有变量赋值
              if cast_type:
                   self.添加代码(f'{target_var} = ({cast_type})({value});')
              else:
                   self.添加代码(f'{target_var} = {value};')


    # 文件管理器辅助函数
    def 获取文件前缀(self):
         return self.文件前缀
    
    def 获取无扩展名文件名(self):
        return f'{self.文件前缀}{self.代码哈希}'

    def 获取头文件名(self):
        return f'{self.获取无扩展名文件名()}.h'

    def 获取cpp文件名(self):
        return f'{self.获取无扩展名文件名()}.cpp'

    def 获取库文件名(self):
        if self.可执行文件名:
            return self.可执行文件名
        return f'{self.获取无扩展名文件名()}.so'

    def _构建当前参数列表字符串(self):
        params = []
        for name, var in self.参数变量.items():
            if name == 'self': continue # Skip self if present
            
            if name in self.列表参数映射:
                ptr_var, len_var = self.列表参数映射[name]
                params.append(f'{ptr_var.类型名} {ptr_var.C名称}')
                params.append(f'{len_var.类型名} {len_var.C名称}')
            elif isinstance(var, C变量):
                params.append(f'{var.类型名} {var.C名称}')
        return ', '.join(params)

    def 生成定义(self):
        """生成 C 函数定义/声明，或 C++ 类定义"""
        if self.是否为类:
             # 生成类定义 struct Name { ... };
             fields = []
             for name, type_ in self.类成员变量.items():
                  fields.append(f'    {type_} {name};')
             
             method_decls = []
             for m in self.类方法列表:
                 if m['is_init']:
                     method_decls.append(f"    {m['name']}({m['params']});")
                 else:
                     method_decls.append(f"    {m['ret_type']} {m['name']}({m['params']});")

             struct_body = '\n'.join(fields + [''] + method_decls)
             return f'struct {self.C函数名} {{\n{struct_body}\n}};'
        
        params = []
        for name, var in self.参数变量.items():
            if name in self.列表参数映射:
                ptr_var, len_var = self.列表参数映射[name]
                params.append(f'{ptr_var.类型名} {ptr_var.C名称}')
                params.append(f'{len_var.类型名} {len_var.C名称}')
            elif isinstance(var, C变量):
                params.append(f'{var.类型名} {var.C名称}')
        
        param_str = ', '.join(params)
        return f'extern "C" {self.返回类型} {self.C函数名} ({param_str})'

    def 获取包含代码(self):
        return '\n'.join([f'#include {d}' for d in sorted(self.包含头文件)])

    def 获取头文件代码(self):
        return f'#pragma once\n{self.获取包含代码()}\n{self.生成定义()};'

    def 获取cpp代码(self):
        if self.是否为类:
            # 生成类实现代码
            # struct 定义在头文件中 (获取头文件代码 -> 生成定义)
            # 这里生成方法实现
            impls = []
            for m in self.类方法列表:
                full_name = f"{self.C函数名}::{m['name']}"
                if m['is_init']:
                    head = f"{full_name}({m['params']})"
                else:
                    head = f"{m['ret_type']} {full_name}({m['params']})"
                
                body_lines = [str(line) for line in m['body']]
                body_str = '\n'.join(body_lines)
                impls.append(f'{head}\n{body_str}')
            
            return f'#include "{self.获取头文件名()}"\n' + '\n\n'.join(impls)

        body_code = [str(c) for c in self.代码序列]
        return f'#include "{self.获取头文件名()}"\n{self.生成定义()}\n' + '\n'.join(body_code)

    def 保存代码到文件(self):
        # 清理旧文件
        if os.path.exists(全局上下文.工作目录):
            for fname in os.listdir(全局上下文.工作目录):
                if fname.startswith(self.文件前缀):
                    os.remove(os.path.join(全局上下文.工作目录, fname))
                    
        确保目录存在(全局上下文.工作目录)
        
        with open(f'{全局上下文.工作目录}/{self.获取头文件名()}', 'w') as f:
            f.write(self.获取头文件代码())
            
        with open(f'{全局上下文.工作目录}/{self.获取cpp文件名()}', 'w') as f:
            f.write(self.获取cpp代码())

    def 加载库(self):
        """加载编译好的动态库"""
        if self.可执行文件名:
            return
        
        lib_path = f'{全局上下文.工作目录}/{self.获取库文件名()}'
        self.目标库 = ctypes.CDLL(lib_path)
        self.cpp函数 = self.目标库[self.C函数名]
        self.cpp函数.argtypes = self.ctypes参数类型
        self.cpp函数.restype = self.ctypes返回类型

    def __call__(self, *args, **kwargs):
        if self.可执行文件名:
             raise RuntimeError(f"Cannot call executable directly. Run {全局上下文.工作目录}/{self.可执行文件名}")
        
        if self.列表参数映射:
             new_args = []
             keep_alive = []
             # 遍历预期参数 (按名称)
             # 假设 args 根据参数定义顺序传递
             # self.参数变量 保持插入顺序
             param_names = list(self.参数变量.keys())
             
             arg_idx = 0 # self.ctypes参数类型 中的索引
             
             for i, arg in enumerate(args):
                 if i >= len(param_names):
                      break 
                      
                 param_name = param_names[i]
                 
                 if param_name in self.列表参数映射:
                      if not isinstance(arg, (list, tuple)):
                           raise TypeError(f"Argument '{param_name}' expected list, got {type(arg)}")
                      
                      # ctypes参数类型[arg_idx] 是对应的指针类型
                      pointer_type = self.ctypes参数类型[arg_idx]
                      length = len(arg)
                      
                      # 构造数组
                      array_type = pointer_type._type_ * length
                      c_array = array_type(*arg)
                      keep_alive.append(c_array) # 保持引用，防止 GC 回收
                      
                      new_args.append(c_array)
                      new_args.append(length)
                      
                      arg_idx += 2
                 else:
                      new_args.append(arg)
                      arg_idx += 1
                      
             return self.cpp函数(*new_args)
        
        return self.cpp函数(*args)
