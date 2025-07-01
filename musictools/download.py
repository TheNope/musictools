import sys
from musictools.khi_scraper import KHIScraper
from musictools import get_logger


def download():
    url = sys.argv[1]
    logger = get_logger()

    if "khinsider" in url:
        scraper = KHIScraper(
            url,
            logger=logger,
        )
        scraper.download()
    else:
        raise ValueError(f"Could not parse url: {url}")

    print("Download finished!")


if __name__ == "__main__":
    download()
