import logging

LOSSLESS_FORMATS = ["flac"]
LOSSY_FORMATS = ["mp3"]
SUPPORTED_FORMATS = LOSSLESS_FORMATS + LOSSY_FORMATS


def get_logger() -> logging.Logger:
    logger = logging.Logger(
        name="music-manager-logger",
        level=logging.INFO,
    )
    logger.addHandler(logging.StreamHandler())
    return logger
