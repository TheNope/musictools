from abc import ABC, abstractmethod
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from dataclasses import dataclass
from pathlib import Path
from musictools import SUPPORTED_FORMATS


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

    def compress(
            self,
            format: str,
        ):
        for title in self.content:
            original_title = title
            title_path = Path(title)
            title = title.replace(title_path.suffix, format)
            title_index = self.content.index(original_title)
            self.content[title_index] = title


@dataclass
class MusicFile(ABC):
    # title: str | None
    # album: str | None
    # artist: str | None
    # year: str | None
    # track_number: int | None

    @staticmethod
    def from_file(file_path: Path) -> 'MusicFile':
        if file_path.suffix == '.mp3':
            return MP3File.from_file(file_path)
        elif file_path.suffix == '.flac':
            return FLACFile.from_file(file_path)
        else:
            raise ValueError('This file type is currently not suported.')
        
    @property
    @abstractmethod
    def bitrate(self) -> float:
        pass

    @property
    @abstractmethod
    def quality(self) -> float:
        pass

    # def write_tags(self):
    #     if self.title: self.file['title'] = self.title
    #     if self.album: self.file['album'] = self.album
    #     if self.artist: self.file['artist'] = self.artist
    #     if self.year: self.file['date'] = self.year
    #     if self.track_number: self.file['tracknumber'] = self.track_number

    #     self.file.save()

@dataclass
class MP3File(MusicFile):
    mp3: MP3
    id3: ID3

    @staticmethod
    def from_file(file_path: Path) -> 'MP3File':
        mp3 = MP3(file_path)
        return MP3File(
            mp3=mp3,
            id3 = mp3.tags or ID3()
        )
    
    @property
    def bitrate(self) -> float:
        return self.mp3.info.bitrate / 1000
    
    @property
    def quality(self) -> float:
        return self.bitrate / 32


@dataclass
class FLACFile(MusicFile):
    flac: FLAC

    @staticmethod
    def from_file(file_path: Path) -> 'FLACFile':
        return FLACFile(
            flac=FLAC(file_path)
        )
    
    @property
    def bitrate(self) -> float:
        return 9999

    @property
    def quality(self) -> float:
        return self.bitrate / 32