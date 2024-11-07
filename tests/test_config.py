from music_manager.config import get_config, ConfigError
import pytest

def test_config():
    config = get_config('tests/data/config.json')
    assert config.library.location == 'Library'
    assert config.library.condensed_location == 'Condensed'
    assert config.download.location == '.'
    assert config.download.preferred_format == 'lossless'


def test_config_validation():
    with pytest.raises(ConfigError) as config_error:
        get_config('tests/data/config_missing_field.json')
        assert config_error.value == 'Config field "condensed_location" is missing'
    with pytest.raises(ConfigError) as config_error:
        get_config('tests/data/config_incorrect_type.json')
        assert config_error.value == 'Config field "location" has type bool but should be of type str'
    with pytest.raises(ConfigError) as config_error:
        get_config('tests/data/config_invalid_option.json')
        assert config_error.value == 'Value of config field "preferred_format" is "abc" but should be one of [\'lossless\', \'lossy\']'