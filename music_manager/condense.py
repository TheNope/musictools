import os
import shutil
from logging import Logger
from music_manager import get_logger
from music_manager.config import get_config
from music_manager.value_objects import Playlist
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


def remove_titles(
    playlists: list[Playlist]
) -> int:
    library_config = get_config().library
    count_removed = 0

    current_titles = list_titles(Path(library_config.condensed_location))
    all_titles: list[Path] = []
    for playlist in playlists:
        all_titles += playlist.absolute_content(library_config.condensed_location)

    for title in current_titles:
        if title not in all_titles and not str(title).endswith('.m3u'):
            os.remove(title)
            count_removed += 1
            print(str(title) + ' removed.')

    return count_removed


def get_playlists() -> list[Playlist]:
    library_config = get_config().library
    item_list = os.listdir(library_config.location)
    ret_list: list[Playlist] = []
    for item in item_list:
        if item.endswith('.m3u'):
            ret_list.append(Playlist.from_file(Path(f'{library_config.location}/{item}')))
    for playlist in ret_list:
        playlist.remove_duplicates()
    return ret_list


def copy_titles(
    playlists: list[Playlist],
    logger: Logger,
) -> tuple[int, int, int]:
    library_config = get_config().library
    all_titles: list[Path] = []
    for playlist in playlists:
        all_titles += playlist.absolute_content(Path(library_config.location))
    count = 0
    count_successfull = 0
    count_existing = 0
    count_not_found = 0
    num_titles = len(all_titles)

    if not os.path.exists(library_config.condensed_location):
        os.mkdir(library_config.condensed_location)

    for title in all_titles:
        count += 1

        condensed_path = Path(title.as_posix().replace(Path(library_config.location).as_posix(), Path(library_config.condensed_location).as_posix()))
        if condensed_path.exists():
            log_str = f'{str(count)}/{str(num_titles)}: {condensed_path.as_posix()} already exists!'
            count_existing += 1
        else:
            try:
                condensed_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                shutil.copy(str(title), str(condensed_path))
                log_str = f'{str(count)}/{str(num_titles)}: {condensed_path.as_posix()} added.'
                count_successfull += 1
            except FileNotFoundError as e:
                count_not_found += 1
                log_str = f'{str(count)}/{str(num_titles)}: {str(title)} does not exist!'

        logger.info(log_str)

    return (count_successfull, count_existing, count_not_found)


def copy_playlists(playlists: list[Playlist]):
    library_config = get_config().library
    for playlist in playlists:
        condensed_playlist_path = Path(playlist.path.as_posix().replace(Path(library_config.location).as_posix(), Path(library_config.condensed_location).as_posix()))
        playlist.save(Path(condensed_playlist_path))


def condense():
    logger = get_logger()
    playlists = get_playlists()
    count_successfull, count_existing, count_not_found = copy_titles(
        playlists=playlists,
        logger=logger,
    )
    count_removed = remove_titles(playlists)
    copy_playlists(playlists)

    logger.info('-----------------------------------------------------------------------------------------------------------')
    logger.info(f'{str(count_removed)} title(s) removed')
    logger.info(f'{str(count_successfull)} title(s) added')
    logger.info(f'{str(count_existing)} title(s) already exist')
    logger.info(f'{str(count_not_found)} title(s) not found')
    logger.info('-----------------------------------------------------------------------------------------------------------')

if __name__ == '__main__':
    condense()