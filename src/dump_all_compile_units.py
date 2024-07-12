import re
import sys
from io import open as io_open
import argparse

def extract_compile_unit_info(file_path):
    try:
        with io_open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except IOError as e:
        print(f"Error opening file: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

    compile_unit_pattern = r'Abbrev Number: 1 \(DW_TAG_compile_unit\)(.*?)(?=\n\s*<1>|\Z)'
    compile_unit_matches = re.findall(compile_unit_pattern, content, re.DOTALL)

    compile_unit_info = []
    for match in compile_unit_matches:
        name_pattern = r'DW_AT_name\s+:\s+(.*)'
        name_match = re.search(name_pattern, match)
        
        comp_dir_pattern = r'DW_AT_comp_dir\s+:\s+(.*)'
        comp_dir_match = re.search(comp_dir_pattern, match)
        
        name = name_match.group(1).strip() if name_match else "N/A"
        comp_dir = comp_dir_match.group(1).strip() if comp_dir_match else "N/A"
        
        compile_unit_info.append((name, comp_dir))

    return compile_unit_info

def main():
    # Parses the content of `readelf --debug-dump=info ramboD.elf > out.txt`.
    # Extracting the compilation units.
    # python3 dump_all_compile_units.py out.txt --name-only --filter /home/disk3/am1lind/NNOpenGL > units.txt
    parser = argparse.ArgumentParser(description='Extract compile unit info from DWARF output.')
    parser.add_argument('file_path', help='Path to the input file')
    parser.add_argument('--name-only', action='store_true', help='Print only DW_AT_name')
    parser.add_argument('--filter', help='Filter DW_AT_comp_dir to start with this prefix')
    
    args = parser.parse_args()
    
    info_list = extract_compile_unit_info(args.file_path)
    if info_list:
        for name, comp_dir in info_list:
            if args.filter and not comp_dir.startswith(args.filter):
                continue
            if args.name_only:
                print(name)
            else:
                print(f"DW_AT_name: {name}")
                print(f"DW_AT_comp_dir: {comp_dir}")
                print("-" * 40)
    else:
        print("No compile unit information found or error occurred.")

if __name__ == "__main__":
    main()