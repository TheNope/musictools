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
    ) -> "Playlist":
        playlist = cls(
            path=path,
            content=[],
        )
        with open(path, "rt") as playlist_file:
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
        with open(path, "wt") as playlist_file:
            for title in self.content:
                playlist_file.write(title + "\n")

    def absolute_content(
        self,
        prefix_path: Path,
    ) -> list[Path]:
        absolute_content: list[Path] = []
        for title in self.content:
            absolute_path = prefix_path / Path(title)
            absolute_content.append(absolute_path)
        return absolute_content

    def remove_duplicates(self):
        for title in self.content:
            while self.content.count(title) > 1:
                self.content.remove(title)
                print(f"Removed duplicate title {title} from playlist {self.path}")
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
