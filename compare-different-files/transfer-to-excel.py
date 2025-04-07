import pandas as pd
import sys

def process_files(inf_file):
    # 提取文件A中的INF文件和源文件列表
    inf_files = {}
    with open(inf_file, 'r') as file_a:
        current_inf = None
        for line in file_a:
            line = line.strip()
            if line.startswith('INF FILE:'):
                current_inf = line[len('INF FILE:'):].strip()
                inf_files[current_inf] = []
            elif current_inf and line:
                inf_files[current_inf].append(line)
    
    # 计算最大列数，填充每列
    max_len = max(len(v) for v in inf_files.values())
    
    # 对每个列表进行填充，使其长度一致
    for key, values in inf_files.items():
        # 用NaN填充列表
        values.extend([None] * (max_len - len(values)))
    
    # 将字典转换为DataFrame
    df = pd.DataFrame(inf_files)
    
    # 将DataFrame保存为Excel文件
    df.to_excel('pi.xlsx', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <inf_file>")
        sys.exit(1)
    process_files(sys.argv[1])
