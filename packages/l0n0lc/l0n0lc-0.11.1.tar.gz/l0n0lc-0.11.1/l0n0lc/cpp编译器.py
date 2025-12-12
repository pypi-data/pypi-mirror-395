
from typing import Union, List
import subprocess
import os
import shutil


class Cpp编译器:
    """
    C++ 编译器包装类，负责检测编译器、设置参数并执行编译命令。
    """
    def __init__(self) -> None:
        self.编译器 = self._检测编译器()
        self.包含目录: List[str] = []
        self.库目录: List[str] = []
        self.库: List[str] = []
        self.编译选项: List[str] = []
        self.详细模式 = False

    def _检测编译器(self) -> str:
        """
        自动检测可用的 C++ 编译器。
        优先检查 'CXX' 环境变量，然后检查常见的编译器命令。
        """
        # 1. 检查环境变量
        cxx = os.environ.get('CXX')
        if cxx:
            return cxx
        
        # 2. 检查系统路径中的标准编译器
        for compiler in ['c++', 'g++', 'clang++']:
            if shutil.which(compiler):
                return compiler
        
        # 3. 后备默认值
        return '/bin/c++'

    def 设置编译器(self, compiler_path: str):
        """手动设置编译器路径"""
        self.编译器 = compiler_path

    def 添加头文件目录(self, directory: Union[str, List[str]]):
        """添加头文件搜索目录 (-I)"""
        if isinstance(directory, str):
            self.包含目录.append(directory)
            return
        self.包含目录.extend(directory)

    def 添加库目录(self, directory: Union[str, List[str]]):
        """添加库文件搜索目录 (-L)"""
        if isinstance(directory, str):
            self.库目录.append(directory)
            return
        self.库目录.extend(directory)

    def 添加库(self, library_name: Union[str, List[str]]):
        """添加需要链接的库 (-l)"""
        if isinstance(library_name, str):
            self.库.append(library_name)
            return
        self.库.extend(library_name)

    def 添加编译选项(self, option: Union[str, List[str]]):
        """添加其他编译选项"""
        if isinstance(option, str):
            self.编译选项.append(option)
            return
        self.编译选项.extend(option)

    def 编译文件(self, file_path: Union[str, List[str]], output_path: str):
        """
        编译源文件到指定输出路径。
        构建并执行完整的编译器命令。
        """
        cmd = [self.编译器]
        
        # 添加头文件目录
        cmd.extend([f'-I{d}' for d in self.包含目录])
        
        # 添加库目录
        cmd.extend([f'-L{d}' for d in self.库目录])
        
        # 添加链接库
        cmd.extend([f'-l{lib}' for lib in self.库])
        
        # 添加编译选项
        cmd.extend(self.编译选项)
        
        # 添加源文件
        if isinstance(file_path, list):
            cmd.extend(file_path)
        else:
            cmd.append(file_path)
            
        # 添加输出路径
        cmd.extend(['-o', output_path])
        
        if self.详细模式:
            print(f"Compiling with command: {' '.join(cmd)}")
            
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Compilation failed with exit code {e.returncode}") from e
        except FileNotFoundError:
             raise RuntimeError(f"Compiler '{self.编译器}' not found. Please install a C++ compiler.")

    def 编译共享库(self, file_path: Union[str, List[str]], output_path: str):
        """
        编译为共享/动态库 (.so)。
        自动添加 -fPIC 和 --shared 选项。
        """
        self.添加编译选项('-fPIC')
        self.添加编译选项('--shared')
        # 默认使用 -O2 优化
        self.添加编译选项('-O2')
        self.编译文件(file_path, output_path)
