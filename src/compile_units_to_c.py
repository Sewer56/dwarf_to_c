import sys
import subprocess
import os

def process_files(input_list_path, elf_file_path):
    # Reads a file generated with 
    # python3 compile_units_to_c.py units.txt --name-only --filter "PREFIX_FROM_DW_AT_COMP_DIR"

    # Read the list of files
    with open(input_list_path, 'r') as file:
        file_list = [line.strip() for line in file if line.strip()]

    # Create a directory for output files
    output_dir = "dwarf_to_c_output"
    os.makedirs(output_dir, exist_ok=True)

    # Process each file
    for file_path in file_list:
        # Construct the output file name
        output_file = os.path.join(output_dir, file_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Construct the command
        command = f"python2 dwarf_to_c.py {elf_file_path} {file_path}"

        print(f"Processing: {file_path}")
        print(f"Output: {output_file}")
        
        try:
            # Run the command and capture the output
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Write the output to a file
            with open(output_file, 'w') as out_file:
                out_file.write(result.stdout)
            
            print(f"Output written to: {output_file}")

        except subprocess.CalledProcessError as e:
            print(f"Error processing {file_path}: {e}")
            print(f"STDERR: {e.stderr}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_file_list> <path_to_elf_file>")
        sys.exit(1)

    input_list_path = sys.argv[1]
    elf_file_path = sys.argv[2]

    process_files(input_list_path, elf_file_path)