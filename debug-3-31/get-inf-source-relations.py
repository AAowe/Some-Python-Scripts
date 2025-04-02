import re
import sys

def extract_files(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # 匹配 Building 行中的 .inf 文件路径
    building_pattern = r'Building\s+\.\.\.\s+(.+\.inf)'
    building_matches = re.findall(building_pattern, content)

    # 匹配 .c、.nasm、.s 文件路径
    source_pattern = r'(/\S+\.(?:c|h|nasm|s|nasmb)\b)'
    source_matches = re.findall(source_pattern, content, re.IGNORECASE)

    # 处理匹配结果
    result = []
    current_inf = None

    for line in content.split('\n'):
        # 检查是否是 Building 行
        if 'Building ...' in line:
            # 提取 .inf 文件路径
            match = re.search(building_pattern, line)
            if match:
                current_inf = remove_absolute_path(match.group(1))
                result.append(f"INF FILE: {current_inf}")
        else:
            # 提取 .c、.nasm、.s 文件路径
            match = re.search(source_pattern, line, re.IGNORECASE)
            if match and current_inf is not None and '/Build/' not in match.group(1):
                source_file = remove_absolute_path(match.group(1))
                # avoid repeated .nasm/.S files
                if result[-1] == source_file:
                    continue
                result.append(source_file)

    # 将结果按要求格式化
    formatted_result = []
    current_inf_entry = None

    for entry in result:
        if entry.startswith('INF'):
            if current_inf_entry is not None:
                formatted_result.append(current_inf_entry)
            current_inf_entry = entry
        else:
            if current_inf_entry is not None:
                current_inf_entry += f"\n\t{entry}"

    if current_inf_entry is not None:
        formatted_result.append(current_inf_entry)

    return formatted_result

'''
    get relative path
'''
def remove_absolute_path(input_string:str):
    prefixes = ['edk2', 'edk2-platforms', 'edk2-non-osi']
    # 使用正则表达式检查并获取匹配的前缀后面的部分
    for prefix in prefixes:
        if prefix in input_string:
            start_index = input_string.find(prefix)  # 查找该前缀的起始位置
            result = input_string[start_index:]  # 获取从该位置开始到字符串末尾的部分
            break
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    result = extract_files(input_file)
    for entry in result:
        print(entry)
        print()