import requests
import html
import re
from pathlib import Path
from logging import Logger

from musictools.config import get_config
from musictools.value_objects import MusicFile

class KHIScraper:
    header = {'user-agent': 'KHIScraper'}
    title_urls = [tuple[str, str]]
    album_name: str
    album_url: str
    year: str

    def __init__(
        self,
        album_url: str,
        logger: Logger,
    ):
        self.logger=logger
        page = self._get_html(album_url)
        self.title_urls = re.findall(
            pattern=r'<td class="clickable-row"><a href="(.*)">(.*)</a></td>',
            string=page,
        )
        self.album_name, self.year = re.findall(
            pattern=r'<title>(.*) \(([0-9]*)\) MP3',
            string=page,
        )[0]
        self.album_url = album_url

    def _get_html(
            self,
            url: str,
        ) -> str:
        page = requests.get(
            url=url,
            headers=self.header
        )
        page.encoding = page.apparent_encoding
        return html.unescape(page.text)

    def download(self):
        download_config = get_config().download
        download_path = Path(download_config.location) / Path(re.sub(r'(\\|\/|\:|\*|\?|\"|\<|\>|\|)', '', self.album_name))
        if not download_path.exists() and not download_path.is_dir():
            download_path.mkdir()

        num_titles = len(self.title_urls)
        i = 0

        for url, title in self.title_urls:
            i += 1
            url = 'https://downloads.khinsider.com' + url

            title_page = self._get_html(url)
            mp3_match = re.findall(
                pattern=r'<a href="(.*).mp3"><span class="songDownloadLink"><i class="material-icons">',
                string=title_page,
            )
            if mp3_match:
                mp3_url = mp3_match[0] + '.mp3'
            flac_match = re.findall(
                pattern=r'<a href="(.*).flac"><span class="songDownloadLink"><i class="material-icons">',
                string=title_page,
            )
            if flac_match:
                flac_url = flac_match[0] + '.flac'
            if download_config.preferred_format == 'lossless' and flac_match:
                file_type = '.flac'
                file_url = flac_url
            else:
                file_type = '.mp3'
                file_url = mp3_url
            file_name = str(i) + file_type
            file_path = download_path / file_name
            if file_path.exists():
                self.logger.info(f'[{str('{:3}'.format(i))}/{str(num_titles)}] Found existing file "{file_name}" skipping...')
                continue
            title_file = requests.get(
                url=file_url,
                headers = self.header
            )
            with open(file_path, 'wb') as file:
                file.write(title_file.content)
            self.logger.info(f'[{str('{:3}'.format(i))}/{str(num_titles)}] Downloaded "{file_name}"')

            # if file_type == '.mp3':
            #     mp3_file = MusicFile(
            #         file_name=str(file_path),
            #         title=title,
            #         album=self.album_name,
            #         artist=None,
            #         year=self.year,
            #         track_number=str(i)
            #     )
            #     mp3_file.write_tags()            
