from dataclasses import dataclass
from pathlib import Path
from musictools import SUPPORTED_FORMATS
from musictools.common.value_objects.music_file import MusicFile


@dataclass
class Playlist:
    path: Path
    title_prefix_path: Path
    name: str
    content: list[MusicFile]

    @classmethod
    def from_file(
        cls,
        path: Path,
        title_prefix_path: Path,
    ) -> "Playlist":
        playlist = cls(
            path=path,
            title_prefix_path=title_prefix_path,
            name=path.name.replace(path.suffix, ""),
            content=[],
        )
        with open(path, "rt") as playlist_file:
            lines = playlist_file.readlines()
        for line in lines:
            line = line.rstrip()
            line = line.replace("\\", "/")
            for format in SUPPORTED_FORMATS:
                if line.endswith(format):
                    playlist.content.append(
                        MusicFile.from_file(title_prefix_path / Path(line))
                    )
                    continue
        return playlist

    def save(
        self,
        path: Path | None = None,
    ):
        if not path:
            path = self.path
        with open(path, "wt") as playlist_file:
            for title in self.content:
                playlist_file.write(
                    str(title.path.relative_to(self.title_prefix_path)) + "\n"
                )

    def content_paths(self) -> list[Path]:
        absolute_content: list[Path] = []
        for title in self.content:
            absolute_content.append(title.path)
        return absolute_content

    def condense(
        self,
        location: Path,
        condensed_location: Path,
        format: str | None = None,
    ):
        self.title_prefix_path = condensed_location
        for title in self.content:
            title.path = Path(
                title.path.as_posix().replace(
                    location.as_posix(),
                    condensed_location.as_posix(),
                )
            )
            if format:
                title.path = Path(
                    title.path.as_posix().replace(title.path.suffix, format)
                )
