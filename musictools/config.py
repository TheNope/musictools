import json
from dataclasses import dataclass
from typing import Any


def get_config(filename: str | None = "config.json") -> "ProgramConfig":
    return ProgramConfig.load(filename)


class ConfigError(Exception): ...


@dataclass
class Config:
    @staticmethod
    def _validate_field(
        name: str,
        config_dict: dict[str, Any],
        content_type: type,
        options: list[Any] | None = None,
    ):
        content = config_dict.get(name)
        if content is None:
            raise ConfigError(f'Config field "{name}" is missing')
        if not isinstance(content, content_type):
            raise ConfigError(
                f'Config field "{name}" has type {type(content).__name__} but should be of type {content_type.__name__}'
            )
        if options:
            if content not in options:
                raise ConfigError(
                    f'Value of config field "{name}" is "{content}" but should be one of {options}'
                )
        return

    @classmethod
    def validate(
        cls,
        config_dict: dict[str, Any],
    ):
        return

    @classmethod
    def load(
        cls,
        config_dict: dict[str, Any],
    ) -> "Config":
        cls.validate(config_dict)
        return cls(**config_dict)


@dataclass
class LibraryConfig(Config):
    location: str = ""
    condensed_location: str = ""

    @classmethod
    def validate(
        cls,
        config_dict: dict[str, Any],
    ):
        cls._validate_field(
            name="location",
            config_dict=config_dict,
            content_type=type(cls.location),
        )
        cls._validate_field(
            name="condensed_location",
            config_dict=config_dict,
            content_type=type(cls.condensed_location),
        )


@dataclass
class CondenseConfig(Config):
    compress: bool = False
    compression_quality: int = 10
    variable_bitrate: bool = True

    @classmethod
    def validate(
        cls,
        config_dict: dict[str, Any],
    ):
        cls._validate_field(
            name="compress",
            config_dict=config_dict,
            content_type=type(cls.compress),
        )
        cls._validate_field(
            name="compression_quality",
            config_dict=config_dict,
            content_type=type(cls.compression_quality),
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )
        cls._validate_field(
            name="variable_bitrate",
            config_dict=config_dict,
            content_type=type(cls.variable_bitrate),
        )


@dataclass
class DownloadConfig(Config):
    location: str = ""
    preferred_format: str = "lossless"

    @classmethod
    def validate(
        cls,
        config_dict: dict[str, Any],
    ):
        cls._validate_field(
            name="preferred_format",
            config_dict=config_dict,
            content_type=type(cls.preferred_format),
            options=["lossless", "lossy"],
        )
        cls._validate_field(
            name="location",
            config_dict=config_dict,
            content_type=type(cls.location),
        )


@dataclass
class ExportConfig(Config):
    location: str = ""

    @classmethod
    def validate(
        cls,
        config_dict: dict[str, Any],
    ):
        cls._validate_field(
            name="location",
            config_dict=config_dict,
            content_type=type(cls.location),
        )


@dataclass
class ProgramConfig(Config):
    library: LibraryConfig
    condense: CondenseConfig
    download: DownloadConfig
    export: ExportConfig

    @classmethod
    def load(
        cls,
        filename: str,
    ) -> "Config":
        with open(filename, "rt") as config_file:
            config_dict = json.loads(config_file.read())
        return cls(
            library=LibraryConfig.load(config_dict.get("library")),
            condense=CondenseConfig.load(config_dict.get("condense")),
            download=DownloadConfig.load(config_dict.get("download")),
            export=ExportConfig.load(config_dict.get("export")),
        )
