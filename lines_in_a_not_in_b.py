import sys

def find_lines_in_a_not_in_b(file_a, file_b):
    # 读取文件 A 的行
    with open(file_a, 'r') as f_a:
        lines_a = f_a.readlines()
        lines_a_set = set(lines_a)
    
    # 读取文件 B 的行
    with open(file_b, 'r') as f_b:
        lines_b = f_b.readlines()
        lines_b_set = set(lines_b)
    
    # 找出在文件 A 中但不在文件 B 中的行
    lines_in_a_not_in_b = list(lines_a_set - lines_b_set)
    lines_in_a_not_in_b.sort(key = lines_a.index)
    
    # 输出结果
    print("Lines in {} but not in {}:".format(file_a, file_b))
    for line in lines_in_a_not_in_b:
        print(line, end='')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <file_a> <file_b>")
        sys.exit(1)
    
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    
    find_lines_in_a_not_in_b(file_a, file_b)