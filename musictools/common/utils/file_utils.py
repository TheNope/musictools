import os
from pathlib import Path

def list_titles(path: Path) -> list[Path]:
    if not os.path.isdir(path):
        return [path]
    else:
        ret_list: list[Path] = []
        for item in path.iterdir():
            item_list = list_titles(path / item)
            ret_list += item_list

        return ret_list
