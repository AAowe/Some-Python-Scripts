import os
import re
from collections import defaultdict
import sys

def find_inf_file(path):
    """
    在指定路径及其上级目录中查找扩展名为.inf的文件。
    """
    while True:
        inf_files = [f for f in os.listdir(path) if f.endswith('.inf')]
        if inf_files:
            return os.path.join(path, inf_files[0])
        parent_path = os.path.dirname(path)
        if parent_path == path:
            break
        path = parent_path
    return None

def process_lines_list(lines_list):
    """
    处理文件列表，提取路径并查找对应的.inf文件。
    """
    inf_to_c_files = defaultdict(list)
    '''
    considering .c/.nasm in x86, or .c/.s/in arm
    '''
    pattern = re.compile(r'(\S+\.(c|nasm|s))', re.IGNORECASE)

    for line in lines_list:
        match = pattern.search(line)
        if match:
            file_path = match.group(1)
            dir_path = os.path.dirname(file_path)
            inf_file = find_inf_file(dir_path)
            if inf_file:
                inf_to_c_files[inf_file].append(file_path)

    # 按字典序排序
    sorted_inf_files = sorted(inf_to_c_files.items(), key=lambda x: x[0])

    # 输出结果
    for inf_file, c_files in sorted_inf_files:
        print(f"INF File: {inf_file}")
        for c_file in sorted(c_files):
            print(f"  Corresponding C/NASM File: {c_file}")
        print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <file>")
        sys.exit(1)
    
    file = sys.argv[1]

    # get every line in input file
    with open(file, 'r') as f:
        lines_list = [line.strip() for line in f.readlines()]

    process_lines_list(lines_list)