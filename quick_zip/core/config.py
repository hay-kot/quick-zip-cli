import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic.main import BaseModel
from quick_zip.schema.config import AppConfig
from rich.console import Console
from rich.traceback import install

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
install()


BASE_DIR = Path(__file__).parent.parent
APP_VERSION = "v0.1.0"
ZIP_TYPES = [".tar.gz", ".bz2", ".zip"]

AppConfig: BaseModel
console = Console()


def determine_config_file():
    default_config = BASE_DIR.joinpath("config.json")
    config_file = os.getenv("QUICKZIP_CONFIG", default_config)
    return Path(config_file)


def generate_config(config_file):
    return AppConfig.from_file(config_file)


CONFIG_FILE = determine_config_file()
