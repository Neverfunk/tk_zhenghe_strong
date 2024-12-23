import os
def process_erb_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ERB"):
                file_path = os.path.join(root, file)
                modify_file(file_path)

def modify_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()

        modified_lines = []
        for line in lines:
            stripped_line = line.lstrip()
            indent = line[:len(line) - len(stripped_line)]
            if stripped_line.startswith("MONEY") and not stripped_line.startswith("MONEY:"):
                if "+=" in stripped_line or "-=" in stripped_line:
                    # Add ';' at the beginning of the line with original indentation
                    modified_lines.append(f"{indent};{stripped_line}")

                    # Determine the remaining content
                    if "+=" in stripped_line:
                        _, content = stripped_line.split("+=", 1)
                        modified_lines.append(f"{indent}CALL ADD_MONEY(({content.strip()}))\n")
                    elif "-=" in stripped_line:
                        _, content = stripped_line.split("-=", 1)
                        modified_lines.append(f"{indent}CALL ADD_MONEY(-1*({content.strip()}))\n")
                else:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)

        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.writelines(modified_lines)

        print(f"Processed file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

directory = "./ERB/"
process_erb_files(directory)
