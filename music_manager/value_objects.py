from mutagen.easyid3 import EasyID3
from typing import Optional
from dataclasses import dataclass
from pathlib import Path
from music_manager import SUPPORTED_FORMATS


@dataclass
class Playlist:
    path: Path
    content: list[str]

    @classmethod
    def from_file(
        cls,
        path: str,
    ) -> 'Playlist':
        playlist = cls(
            path=path,
            content=[],
        )
        with open(path, 'rt') as playlist_file:
            lines = playlist_file.readlines()
        for line in lines:
            line = line.rstrip()
            for format in SUPPORTED_FORMATS:
                if line.endswith(format):
                    playlist.content.append(line)
                    continue
        return playlist
    
    def save(
        self,
        path: Path | None = None,
    ):
        if not path:
            path = self.path
        with open(path, 'wt') as playlist_file:
            for title in self.content:
                playlist_file.write(title + '\n')

    def absolute_content(
        self,
        prefix_path: Path,
    ) -> list[Path] :
        absolute_content: list[Path] = []
        for title in self.content:
            absolute_path = prefix_path / Path(title)
            absolute_content.append(absolute_path)
        return absolute_content
    
    def remove_duplicates(self):
        for title in self.content:
            while self.content.count(title) > 1:
                self.content.remove(title)
                print(f'Removed duplicate title {title} from playlist {self.path}')
        self.save()


class MusicFile:
    file_url: str
    file_name: str
    file: EasyID3
    title: str
    album: str
    artist: str
    year: str
    track_number: int

    def __init__(
        self,
        file_name: str,
        title: Optional[str] = None,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        year: Optional[int] = None,
        track_number: Optional[int] = None
    ):
        """Create a new Mp3File object representing an existing mp3 file on disk."""
        self.file_name = file_name
        self.file = EasyID3(file_name)
        self.title = title
        self.album = album
        self.artist = artist
        self.year = year
        self.track_number = track_number

    def write_tags(self):
        """Write tags to the file on disk."""
        self.file['title'] = self.title
        self.file['album'] = self.album
        if self.artist is not None:
            self.file['artist'] = self.artist
        self.file['date'] = self.year
        self.file['tracknumber'] = self.track_number

        self.file.save()