from typing import *
import os
import json


def is_facade_path(name: str) -> bool:
    path = os.path.join("NNStructure", name)

    if os.path.isdir(path):
        subfiles = os.listdir(path)
        return "facade.py" in subfiles
    return False


def find_facades() -> List[str]:
    items = os.listdir("NNStructure")
    return list(filter(is_facade_path, items))


# map player names to paths to config files
def find_players() -> Dict[str, str]:
    result = {}
    for folder in os.listdir("Models"):
        if os.path.isdir(folder):
            try:
                config = open(os.path.join(os.path.join("Models", folder), "config.json"), 'r')
                data = ''.join(config.readlines())
                config.close()
                data = json.loads(data)
                name = data['name']
                if not name:
                    continue

                result[name] = os.path.join("Models", folder)
            except:
                continue
        return result


