# cpg_islands_preprocessing.py
import os
from typing import List

def read_file(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def reformat_lines(lines: List[str]) -> List[str]:
    joined_lines = "".join(lines)
    return joined_lines.split(".0")

def write_file(output_path: str, lines: List[str]) -> None:
    with open(output_path, 'w') as file:
        for line in lines:
            if line.startswith('>'):
                file.write(line + ".0")
            else:
                file.write('\n' + line + '\n')

def reformat_files(input_dir: str, output_dir: str) -> None:
    files = os.listdir(input_dir)
    for file in files:
        lines = read_file(os.path.join(input_dir, file))
        reformatted_lines = reformat_lines(lines)
        write_file(os.path.join(output_dir, file), reformatted_lines)