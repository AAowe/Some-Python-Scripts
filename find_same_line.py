import sys

def find_common_lines(file1, file2, file3):
    # 读取每个文件的行
    with open(file1, 'r') as f1:
        lines1 = set(f1.readlines())
    with open(file2, 'r') as f2:
        lines2 = set(f2.readlines())
    with open(file3, 'r') as f3:
        lines3 = set(f3.readlines())
    
    # 找出三个文件中的共同行
    common_lines = lines1.intersection(lines2).intersection(lines3)
    
    # 输出结果
    print("Common lines in all three files:")
    for line in common_lines:
        print(line, end='')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <file1> <file2> <file3>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]
    
    find_common_lines(file1, file2, file3)