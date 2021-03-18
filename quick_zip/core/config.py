import json
from pathlib import Path

from pydantic.main import BaseModel
from schema.backup_job import BackupJob
from schema.config import AppConfig

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR.joinpath("config.json")
APP_VERSION = "v0.1.0"
ZIP_TYPES = [".tar.gz", ".bz2", ".zip"]

AppConfig: BaseModel


def generate_config(config_file):

    return AppConfig.from_file(config_file)


def generate_defaults(config_file):
    return BackupJob.get_defaults(config_file)


defaults = generate_defaults(CONFIG_FILE)
config = generate_config(CONFIG_FILE)
