# Created by Noé Cruz | Zurckz 22 at 20/03/2022
# See https://www.linkedin.com/in/zurckz

import json
import os
import sys
from pathlib import Path
from typing import Callable, List


def read_event(name: str = None, event_file_path: str = None):
    event_path = f"{os.getcwd()}\\events\\{name}" if name else event_file_path
    if not event_path:
        raise ValueError("Path file or name is required...")
    with open(event_path, 'r') as sm:
        return json.loads(sm.read())


def add_source_to_path(src_dir: str = None, replacement: str = None):
    current_dir = src_dir
    if not current_dir:
        current_dir = os.getcwd()
        current_dir = current_dir.replace('\\tests' if not replacement else replacement, '\\src')
    sys.path.append(current_dir)
    path = Path(current_dir)
    sys.path.append(str(path.parent.absolute()))


def get_files_in(directory: str, ext, absolute=False) -> List[str]:
    path_files = []
    parent = os.getcwd()
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(ext):
                if absolute:
                    path_files.append(os.path.join(parent, root, filename))
                else:
                    path_files.append(os.path.join(root, filename))
    return path_files


def file_content_updater(
        file_path: str,
        mutator: Callable[[str], str] = None,
        find: str = None,
        replaced: str = None,
) -> None:
    """
    Content File Updater
    @param file_path:
    @param mutator:
    @param find:
    @param replaced:
    @return:
    """
    with open(file_path, "r+b") as f:
        content = f.readlines()
        for i, line in enumerate(content):
            line = line.decode("utf-8")
            if mutator:
                new: str = mutator(line)
                content[i] = new.encode("utf-8")
            else:
                if line and find in line:
                    print(f"Found in {file_path} line: {i}... Removed...")
                    content[i] = line.replace(find, replaced).encode("utf-8")
        f.seek(0)
        f.truncate()
        f.writelines(content)
