import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic.main import BaseModel
from rich.console import Console
from rich.traceback import install

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
install()

BASE_DIR = Path(__file__).parent.parent
APP_VERSION = "v0.1.0"
console = Console()


def determine_config_file():
    default_config = BASE_DIR.joinpath("config.json")
    config_file = os.getenv("QUICKZIP_CONFIG", default_config)
    return Path(config_file)


class AppSettings(BaseModel):
    """
    The App configuration object. This is read from the config.json file and used for various
    App wide settings.

    Attributes:
        enable_webhooks: bool
        webhook_address: str
        relative_path: Path
    """

    enable_webhooks: bool
    webhook_address: str
    zip_types: list
    verbose: bool = False

    def set_verbose(self, value=True):
        self.verbose = value

    @classmethod
    def from_file(cls, file: Path):
        """Helper function to pull the "config" key out of a
        config.json file, or whatever file is passed as the argument

        Args:
            file (Path): Path to config.json

        Returns:
            [AppConfig]: Returns an Instance of AppConfig
        """
        with open(file, "r") as f:
            config_json = json.loads(f.read())

        return cls(**config_json.get("config"))


CONFIG_FILE = determine_config_file()
settings = AppSettings.from_file(CONFIG_FILE)
