import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1> <files_to_check>")
        sys.exit(1)

    file1 = sys.argv[1]
    files_to_check_file = sys.argv[2]
    result = []

    # 输出结果
    # print(f"{'File to check':<26} | {'In File 1':<10} | {'Path'}")
    # print("-" * 60)

    # 读取要检查的文件列表
    with open(files_to_check_file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    with open(file1, "r") as f:
        paths = f.read().split()
    for l in lines:
        flag = False
        for p in paths:
            if l in p:
                print(f"      {l:<26} | {'YES':<10} | {p}")
                flag = True
                break
        if not flag:
            print(f"      {l:<26} | {'NO':<10} | NULL")
