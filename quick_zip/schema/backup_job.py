from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import BaseModel
from quick_zip.schema.file_system import FileStat


class BackupJob(BaseModel):
    """Main configuration objcect for jobs.

    Attributes:
        name: str
        source: Path
        destination: Path
        all_files: bool = False
        clean_up: bool = False
        clean_up_source: bool = False
        keep: int = 4

    """

    name: str
    source: Path
    destination: Path
    all_files: bool = False
    clean_up: bool = False
    clean_up_source: bool = False
    keep: int = 4
    audit: bool = False,
    results: str = "not set"
    oldest: int = 7

    def __repr__(self) -> str:
        return f"""

        Name: {self.name} 
        Source: {self.source} 
        Destination: {self.destination} 
        Include All Files: {self.all_files} 
        Cleanup: {self.clean_up} 
        keep: {self.keep} 
        
        """

    @property
    def final_dest(self):
        dir = self.destination.joinpath(self.name)
        dir.mkdir(parents=True, exist_ok=True)
        return dir

    @classmethod
    def get_defaults(cls, file: Path) -> BackupJob:
        """Helper function to pull the "default" key out of a
        config.json file, or whatever file is passed as the argument

        Args:
            file (Path): Path to config.json

        Returns:
            [BackupJob]: Returns an Instance of BackupJob
        """
        with open(file, "r") as f:
            config_json = json.loads(f.read())

        if defaults := config_json.get("defaults"):
            return cls(**defaults)
        else:
            raise Exception("No Default Arguments")

    @staticmethod
    def _find_replace_vars(content: str, vars: dict):
        for key, value in vars.items():
            match_str = r"\$\{" + key + r"\}"
            content = re.sub(match_str, value, content)

        match_str = r"\$\{.*\}"

        if match := re.search(match_str, content):
            raise Exception(
                f"Undefined Variable Detected in the configuration file `{match.group()}`"
            )

        return content

    @staticmethod
    def get_job_store(config: Path) -> list[BackupJob]:
        """A Helper function to read the "jobs" key of the configuration
        file and return a list of BackupJob Objects.

        Args:
            config (Path): The Path object for the configuration file

        Returns:
            list[BackupJob]:
        """

        with open(config, "r") as f:
            raw_content = f.read()

        vars: dict = json.loads(raw_content).get("vars", False)
        if vars:
            content = BackupJob._find_replace_vars(raw_content, vars)
            content = json.loads(content).get("jobs")
        else:
            content: list[dict] = json.loads(raw_content).get("jobs")

        return [BackupJob(**job) for job in content]


class BackupResults(BaseModel):
    """Results returned for each job ccompleted

    Attributes:
        name: str
        file: Path
        stats: FileStat

    """

    name: str
    file: Path
    stats: FileStat


class PostData(BaseModel):
    data: list[BackupResults]
