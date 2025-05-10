import os
from pathlib import Path

from musictools import SUPPORTED_FORMATS
from musictools.common.value_objects.playlist import Playlist


def list_titles(path: Path) -> list[Path]:
    if not os.path.isdir(path):
        if path.suffix.replace(".", "") in SUPPORTED_FORMATS:
            return [path]
        else:
            return []
    else:
        ret_list: list[Path] = []
        for item in path.iterdir():
            item_list = list_titles(path / item)
            ret_list += item_list

        return ret_list


def get_playlists(path: Path) -> list[Playlist]:
    item_list = os.listdir(path)
    ret_list: list[Playlist] = []
    for item in item_list:
        if item.endswith(".m3u"):
            ret_list.append(
                Playlist.from_file(
                    title_prefix_path=Path(path),
                    path=path / item,
                )
            )
    return ret_list
