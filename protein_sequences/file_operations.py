import os
from typing import List

def read_file(file_path: str) -> List[str]:
    with open(file_path) as file:
        return file.readlines()

def write_to_file(file_path: str, content: str) -> None:
    with open(file_path, 'a+') as file:
        file.write(content)

def get_all_files(directory_path: str) -> List[str]:
    return os.listdir(directory_path)