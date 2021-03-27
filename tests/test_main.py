from quick_zip.core.settings import APP_VERSION
from quick_zip.core import settings


def test_version():
    assert APP_VERSION == "v0.1.9"


def test_env_setup(test_app, test_config):
    assert test_config == settings.determine_config_file()

    assert settings.settings.config_file == test_config
