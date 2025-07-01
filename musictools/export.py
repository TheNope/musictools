import json
from pathlib import Path
from musictools.common.utils.file_utils import get_playlists, list_titles
from musictools.common.value_objects.music_file import MusicFile
from musictools.config import get_config


def generate_library_dict(library_location: Path) -> dict[str, dict[str, str]]:
    titles = list_titles(library_location)
    library_dict = {}
    i = 0

    for title in titles:
        music_file = MusicFile.from_file(title)
        title_dict = {
            "artist": music_file.artist,
            "album": music_file.album,
            "title": music_file.title,
            "track": music_file.track,
            "genre": music_file.genre,
        }
        library_dict[f"title_{str(i)}"] = title_dict
        i += 1

    return library_dict


def generate_playlists_dict(library_location: Path) -> dict[str, dict[str, str]]:
    playlists = get_playlists(library_location)
    playlists_dict = {}

    for playlist in playlists:
        playlist_dict = {}
        i = 0

        for title in playlist.content:
            title_dict = {
                "artist": title.artist,
                "album": title.album,
                "title": title.title,
                "track": title.track,
                "genre": title.genre,
            }
            playlist_dict[f"title_{str(i)}"] = title_dict
            i += 1

        playlists_dict[playlist.name] = playlist_dict

    return playlists_dict


def export():
    library_config = get_config().library
    export_config = get_config().export

    library_dict = generate_library_dict(Path(library_config.location))
    playlists_dict = generate_playlists_dict(Path(library_config.location))

    with open(
        Path(export_config.location) / Path("library.json"), "wt"
    ) as library_export_file:
        library_export_file.write(
            json.dumps(
                obj=library_dict,
                indent=2,
            )
        )
    with open(
        Path(export_config.location) / Path("playlists.json"), "wt"
    ) as playlists_export_file:
        playlists_export_file.write(
            json.dumps(
                obj=playlists_dict,
                indent=2,
            )
        )


if __name__ == "__main__":
    export()
