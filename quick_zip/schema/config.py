import json
from pathlib import Path

from pydantic import BaseModel


class AppConfig(BaseModel):
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
