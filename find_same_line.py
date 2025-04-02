import sys

def find_common_lines(file1, file2, file3):
    # 读取每个文件的行
    with open(file1, 'r') as f1:
        lines1 = f1.readlines()
        lines1_set = set(lines1)
    with open(file2, 'r') as f2:
        lines2 = f2.readlines()
        lines2_set = set(lines2)
    with open(file3, 'r') as f3:
        lines3 = f3.readlines()
        lines3_set = set(lines3)
    
    # 找出三个文件中的共同行
    common_lines = list(lines1_set.intersection(lines2_set).intersection(lines3_set))

    # ordered as lines1
    order = 1
    match order:
        case 2:
            common_lines.sort(key = lines2.index)
        case 3:
            common_lines.sort(key = lines3.index)
        case _:
            common_lines.sort(key = lines1.index)
    # 输出结果
    print("Common lines in all three files:")
    for line in common_lines:
        print(line, end='')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <file1> <file2> <file3>")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]
    find_common_lines(file1, file2, file3)