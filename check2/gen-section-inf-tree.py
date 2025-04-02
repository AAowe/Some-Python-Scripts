import os
import re
from pathlib import Path
from collections import defaultdict

class EDK2Parser:
    def __init__(self, arch, file_a_path, file_d_path, root_dir):
        self.arch = arch.upper()
        self.root_dir = Path(root_dir).resolve()
        self.file_a = Path(file_a_path)
        self.file_d = Path(file_d_path)
        
        # 初始化 processed_files 为空集合
        self.processed_files = set()  # 这里初始化为空集合

        # 初始化时处理文件D
        self.library_classes = self.parse_library_classes()
        
        self.file_tree = defaultdict(list)

    def parse_library_classes(self):
        """解析文件D的库类信息（包含处理!include）"""
        lib_classes = defaultdict(dict)
        sections = self.resolve_include(self.file_d, self.file_d.parent)
        
        for section, lines in sections.items():
            for line in lines:
                if '|' in line:
                    lib, path = line.split('|', 1)
                    lib_classes[section][lib.strip()] = self.normalize_path(path.strip())
        
        return lib_classes

    def normalize_path(self, rel_path):
        """将EDK2风格路径转换为绝对路径"""
        if rel_path.startswith('"'):
            rel_path = rel_path.strip('"')
        return str(self.root_dir / rel_path)

    def _preprocess_line(self, lines):
        """预处理行：去除注释、处理续行"""
        buffer = ''
        for line in lines:
            line = line.split('#')[0].strip()
            if not line:
                continue
            
            # 处理续行
            if line.endswith('\\\\\\'):
                buffer += line[:-1]
                continue
            
            if buffer:
                line = buffer + line
                buffer = ''
            
            yield line

    def resolve_include(self, file_path, base_dir):
        """递归处理!include"""
        file_path = Path(file_path).resolve()
        if file_path in self.processed_files:
            return defaultdict(list)
        self.processed_files.add(file_path)  # 标记文件已处理

        sections = defaultdict(list)
        current_section = None
        
        with open(file_path, 'r') as f:
            for line in self._preprocess_line(f):
                if line.startswith('!include'):
                    include_path = line.split(' ', 1)[1].strip().strip('"')
                    abs_path = (base_dir / include_path).resolve()
                    if abs_path.exists():
                        included_sections = self.resolve_include(abs_path, abs_path.parent)
                        for section, content in included_sections.items():
                            sections[section].extend(content)
                    continue
                
                if line.startswith('!'):
                    continue  # 忽略其他!开头的宏
                
                if line.startswith('['):
                    current_section = line.strip().strip('[]')
                    continue
                
                if current_section is not None:
                    sections[current_section].append(line)
        
        return sections

    def process_file_a(self):
        """处理文件A"""
        sections = self.resolve_include(self.file_a, self.file_a.parent)
        
        if 'Sec' in sections:
            print(f"\n处理 [Sec] 字段:")
            self.process_section(sections['Sec'], self.file_a.parent)

        if 'Pei' in sections:
            print(f"\n处理 [Pei] 字段:")
            self.process_section(sections['Pei'], self.file_a.parent)

        if 'Dxe' in sections:
            print(f"\n处理 [Dxe] 字段:")
            self.process_section(sections['Dxe'], self.file_a.parent)

    def process_section(self, section_lines, base_dir):
        """处理具体字段内容"""
        current_inf = None
        for line in section_lines:
            line = line.strip()
            if not line:
                continue
            
            if line.endswith('{'):
                current_inf = line.split('{')[0].strip()
                inf_path = self.root_dir / current_inf
                print(f"处理 INF 文件: {current_inf}")
                self.process_inf(inf_path)
                continue
            
            if line == '}':
                current_inf = None
                continue
            
            if current_inf is None and line.endswith('.inf'):
                inf_path = self.root_dir / line
                print(f"处理 INF 文件: {line}")
                self.process_inf(inf_path)

    def process_inf(self, inf_path):
        """处理INF文件（文件B）"""
        inf_path = Path(inf_path).resolve()
        sections = self.resolve_include(inf_path, inf_path.parent)
        
        # 获取MODULE_TYPE
        module_type = None
        for line in sections.get('Defines', []):
            if line.startswith('MODULE_TYPE'):
                module_type = line.split('=', 1)[1].strip()
                break
        
        # 合并LibraryClasses
        merged_libs = []
        possible_sections = [
            f'LibraryClasses.{self.arch}',
            f'LibraryClasses.common.{self.arch}',
            'LibraryClasses.common',
            'LibraryClasses'
        ]
        
        for section in possible_sections:
            if section in sections:
                merged_libs.extend(sections[section])
        
        # 查找库路径
        for lib_line in merged_libs:
            lib_name = lib_line.split('|')[0].strip() if '|' in lib_line else lib_line.strip()
            lib_path = self.find_library_path(lib_name)
            if lib_path:
                print(f"找到库 {lib_name} => {Path(lib_path).relative_to(self.root_dir)}")
                self.file_tree[str(inf_path)].append(lib_path)

    def find_library_path(self, lib_name):
        """根据文件D查找库路径"""
        search_order = [
            f'LibraryClasses.common.{self.arch}',
            f'LibraryClasses.{self.arch}',
            'LibraryClasses.common',
            'LibraryClasses'
        ]
        
        for section in search_order:
            if lib_name in self.library_classes.get(section, {}):
                return self.library_classes[section][lib_name]
        return None

if __name__ == "__main__":
    # 配置参数
    ARCH = 'X64'
    ROOT_DIR = '/home/ubuntu/raspberry/edk2'  # EDK2根目录
    FILE_A = '/home/ubuntu/raspberry/compile-log-workspace/check2/ovmfx64components.txt'       # 文件A绝对路径
    FILE_D = '/home/ubuntu/raspberry/compile-log-workspace/check2/ovmfx64libraries.txt'       # 文件D绝对路径
    
    # 初始化解析器
    parser = EDK2Parser(
        arch=ARCH,
        file_a_path=FILE_A,
        file_d_path=FILE_D,
        root_dir=ROOT_DIR
    )
    
    # 处理文件A
    print("======== 处理文件A ========")
    parser.process_file_a()
    
    # 打印文件树
    print("\n======== 文件依赖关系 ========")
    for parent, children in parser.file_tree.items():
        print(f"{Path(parent).name}:")
        for child in children:
            print(f"  └─ {Path(child).name}")
