from re import sub
import os
from typing import Tuple


def exist_folder(folder: str, path: str) -> bool:
    return os.path.isdir(os.path.join(path, folder))


def join_path(path: str, directory):
    return os.path.join(path, directory)


def if_exist_move(path: str, folder: str) -> Tuple[bool, str]:
    move = exist_folder(folder, path)
    if move:
        current_directory = join_path(path, folder)
        os.chdir(current_directory)
        return True, current_directory
    return False, path


def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s


def camel_case(s):
    if is_camel_case(s):
        return s
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].title(), s[1:]])
