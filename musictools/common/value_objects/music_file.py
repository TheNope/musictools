from abc import ABC, abstractmethod
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MusicFile(ABC):
    path: Path

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
    def artist(self) -> list[str]:
        return []

    @property
    @abstractmethod
    def album(self) -> str:
        return ""

    @property
    @abstractmethod
    def title(self) -> str:
        return ""

    @property
    @abstractmethod
    def track(self) -> str:
        return ""

    @property
    @abstractmethod
    def genre(self) -> str:
        return []

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
        return MP3File(path=file_path, mp3=mp3, id3=mp3.tags or ID3())

    def _texts(self, frame_id: str) -> list[str]:
        texts: list[str] = []
        for frame in self.id3.getall(frame_id):
            texts.extend(frame.text)
        return texts

    @property
    def artist(self) -> list[str]:
        return self._texts("TPE1")

    @property
    def album(self) -> str:
        return (self._texts("TALB") or [""])[0]

    @property
    def title(self) -> str:
        return (self._texts("TIT2") or [""])[0]

    @property
    def track(self) -> str:
        return (self._texts("TRCK") or [""])[0]

    @property
    def genre(self) -> list[str]:
        return self._texts("TCON")

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
        return FLACFile(path=file_path, flac=FLAC(file_path))

    @property
    def artist(self) -> list[str]:
        return self.flac.get("artist", [])

    @property
    def album(self) -> str:
            return self.flac.get("album", [""])[0]

    @property
    def title(self) -> str:
        return self.flac.get("title", [""])[0]

    @property
    def track(self) -> str:
        return self.flac.get("track", [""])[0]

    @property
    def genre(self) -> list[str]:
        return self.flac.get("genre", [])

    @property
    def bitrate(self) -> float:
        return 9999

    @property
    def quality(self) -> float:
        return self.bitrate / 32
