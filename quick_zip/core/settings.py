import os
import shutil
from pathlib import Path
from typing import Optional

import toml
from dotenv import load_dotenv
from pydantic.main import BaseModel
from rich import traceback
from rich.console import Console

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
traceback.install()

BASE_DIR = Path(__file__).parent.parent
DEFAULT_CONFIG = BASE_DIR.joinpath("default.toml")
APP_VERSION = "v0.1.0"
console = Console()


def determine_config_file():
    default_config = BASE_DIR.joinpath("config.toml")
    config_file = Path(os.getenv("QUICKZIP_CONFIG", default_config))

    if config_file.is_file():
        return config_file

    return Path(shutil.copy(DEFAULT_CONFIG, Path.home().joinpath("quick-zip_config.toml")))


class AppSettings(BaseModel):
    """
    The App configuration object. This is read from the config.toml file and used for various
    App wide settings.

    Attributes:
        enable_webhooks: bool
        webhook_address: str
        relative_path: Path
    """

    BASE_DIR: Path = BASE_DIR
    HOME_DIR: Path = Path.home()

    enable_webhooks: bool
    webhook_address: str
    zip_types: list
    verbose: bool = False

    config_file: Optional[Path]

    def set_verbose(self, value=True):
        self.verbose = value

    @classmethod
    def from_file(cls, file: Path):
        """Helper function to pull the "config" key out of a
        config.toml file, or whatever file is passed as the argument

        Args:
            file (Path): Path to config.toml

        Returns:
            [AppConfig]: Returns an Instance of AppConfig
        """
        with open(file, "r") as f:
            config_json = toml.loads(f.read())

        return cls(**config_json.get("config"), config_file=file)

    def update_settings(self, file: Path):
        with open(file, "r") as f:
            config_json = toml.loads(f.read())["config"]

        self.config_file = file
        for key, value in config_json.items():
            if hasattr(self, key):
                setattr(self, key, value)


determined_config = determine_config_file()
settings = AppSettings.from_file(determined_config)
