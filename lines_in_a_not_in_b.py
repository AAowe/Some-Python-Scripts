import sys

def find_lines_in_a_not_in_b(file_a, file_b):
    # 读取文件 A 的行
    with open(file_a, 'r') as f_a:
        lines_a = set(f_a.readlines())
    
    # 读取文件 B 的行
    with open(file_b, 'r') as f_b:
        lines_b = set(f_b.readlines())
    
    # 找出在文件 A 中但不在文件 B 中的行
    lines_in_a_not_in_b = lines_a - lines_b
    
    # 输出结果
    print("Lines in {} but not in {}:".format(file_a, file_b))
    for line in lines_in_a_not_in_b:
        print(line, end='')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_a> <file_b>")
        sys.exit(1)
    
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    
    find_lines_in_a_not_in_b(file_a, file_b)