import sys
import re

def extract_files(input_file):
    c_files = set()
    h_files = set()
    nasm_files = set()
    s_files = set()

    # 正则表达式，用于匹配.c和.h文件
    c_pattern = re.compile(r'(\S+\.c)')
    h_pattern = re.compile(r'(\S+\.h)')
    nasm_pattern = re.compile(r'(\S+\.nasm)', re.IGNORECASE)
    s_pattern = re.compile(r'(\S+\.s)', re.IGNORECASE)


    try:
        with open(input_file, 'r') as file:
            for line in file:
                # 搜索.c文件
                c_matches = c_pattern.findall(line)
                for match in c_matches:
                    c_files.add(match)

                # 搜索.h文件
                h_matches = h_pattern.findall(line)
                for match in h_matches:
                    h_files.add(match)
                
                # 搜索.nasm文件
                nasm_matches = nasm_pattern.findall(line)
                for match in nasm_matches:
                    nasm_files.add(match)

                # 搜索.s文件
                s_matches = s_pattern.findall(line)
                for match in s_matches:
                    s_files.add(match)
            
        # 输出结果
        print("Extracted .c files:")
        for c_file in sorted(c_files):
            print(c_file)

        print("\nExtracted .h files:")
        for h_file in sorted(h_files):
            print(h_file)

        print("\nExtracted .nasm files:")
        for nasm_file in sorted(nasm_files):
            print(nasm_file)

        print("\nExtracted .s files:")
        for s_file in sorted(s_files):
            print(s_file)
        
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    extract_files(input_file)