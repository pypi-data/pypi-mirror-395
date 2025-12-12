import logging
from typing import List, Dict
from .boilerplates import basic
from .placeholders import place_holders
import os

from .ignore import ignore


def scaffolding_dispatcher(in_data: List[Dict[str, str]], verbose=False, click=None):
    basic_project(in_data, verbose)


def basic_project(in_data: List[Dict[str, str]], verbose=False):
    try:
        current_directory = os.getcwd()
        name = in_data[0]["value"]
        only_content = in_data[8]["value"]
        force = True
        # Path
        path = current_directory
        if only_content is False:
            force = False
            path = os.path.join(current_directory, name)
            if os.path.isdir(path) is True:
                print(f"Project {name} already exist!")
                return
                # mode
            mode = 0o666
            os.mkdir(path, mode)
            if verbose is True:
                print("Directory '% s' created" % path)
            os.chdir(path)

        if verbose is True:
            print("Working in '% s'" % path)
        in_data[9] = path
        creator(path, basic, in_data, verbose, force)

        if in_data[7]["value"] is True:
            try:
                os.system(f"code {path}")
            except Exception as ex:
                ...
    except Exception as e:
        print("An critical error occurred while try to generate project...")
        if verbose is True:
            logging.exception(e)


def create_dir_and_move(current_directory, name, verbose, force) -> str:
    path = os.path.join(current_directory, name)
    if os.path.isdir(path) is True:
        print(f"Project {name} already exist!")
        return
    mode = 0o666
    os.mkdir(path, mode)
    if verbose is True:
        print("Directory '% s' created" % path)
    os.chdir(path)
    return path


def creator(c_dir: str, context: dict, info: List, verbose: bool, force: bool):
    for k in context.keys():
        os.chdir(c_dir)
        c_file = context.get(k)
        if c_file["type"] == 'file':
            with open(place_holders(c_file["name"], info), "w+", encoding="utf-8") as f:
                f.write(place_holders(c_file["content"], info))
        elif c_file["type"] == "raw-file":
            with open(place_holders(c_file["name"], info), "w+", encoding="utf-8") as f:
                f.write(ignore)
        elif c_file["type"] == "dir":
            creator(create_dir_and_move(c_dir, place_holders(c_file["name"], info), verbose, force), c_file["child"],
                    info, verbose, force)
