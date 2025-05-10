from abc import ABC, abstractmethod
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MusicFile(ABC):
    # title: str | None
    # album: str | None
    # artist: str | None
    # year: str | None
    # track_number: int | None

    @staticmethod
    def from_file(file_path: Path) -> "MusicFile":
        if file_path.suffix == ".mp3":
            return MP3File.from_file(file_path)
        elif file_path.suffix == ".flac":
            return FLACFile.from_file(file_path)
        else:
            raise ValueError("This file type is currently not suported.")

    @property
    @abstractmethod
    def bitrate(self) -> float:
        pass

    @property
    @abstractmethod
    def quality(self) -> float:
        pass


@dataclass
class MP3File(MusicFile):
    mp3: MP3
    id3: ID3

    @staticmethod
    def from_file(file_path: Path) -> "MP3File":
        mp3 = MP3(file_path)
        return MP3File(mp3=mp3, id3=mp3.tags or ID3())

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
    def from_file(file_path: Path) -> "FLACFile":
        return FLACFile(flac=FLAC(file_path))

    @property
    def bitrate(self) -> float:
        return 9999

    @property
    def quality(self) -> float:
        return self.bitrate / 32
