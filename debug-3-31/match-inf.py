import sys

def process_files(inf_file, components_file):
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

    # 处理文件B并插入源文件
    output_lines = []
    output = []
    with open(components_file, 'r') as file_b:
        current_inf = None
        for line in file_b:
            line = line.strip()
            # remove empty line which made of tabs or blankspaces
            if line == '':
                continue
            #output_lines.append(line)
            # for Phaze, MACRO, Comments, <attribute> and },  just copy them.
            if line.startswith(('[', '!', '#', '<', '}')):
                output.append(line)
            else:
                # eg: NULL|OvmfPkg/Library/SmbiosVersionLib/DetectSmbiosVersionLib.inf
                if '|' in line:
                    current_inf = line.split('|', 1)[1]
                else:
                    current_inf = line.rstrip(' {')
                in_inf_file = False
                for inf_line in inf_files:
                    if current_inf in inf_line:
                        in_inf_file = True
                        if line.endswith('{'):
                            output.append(line)
                            output.append('<Sources>')
                            for source in inf_files[inf_line]:
                                output.append(source)
                        else:
                            output.append(current_inf + ' {')
                            output.append('<Sources>')
                            for source in inf_files[inf_line]:
                                output.append(source)
                            output.append('}')
                if not in_inf_file:
                    output.append(line)

        for line in output:
            print(line)

# 调用函数
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <inf_file> <components_file>")
        sys.exit(1)

    inf_file = sys.argv[1]
    components_file = sys.argv[2]
    process_files(inf_file, components_file)