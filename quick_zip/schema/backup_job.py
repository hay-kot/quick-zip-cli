from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from schema.file_system import FileStat


class BackupJob(BaseModel):
    name: str
    source: Path
    destination: Path
    all_files: bool = False
    clean_up: bool = False
    keep: int = 4

    def __repr__(self) -> str:
        return f"""
Name: {self.name} 
Source: {self.source} 
Destination: {self.destination} 
Include All Files: {self.all_files} 
Cleanup: {self.clean_up} 
keep: {self.keep} 
        """

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
            content: list[dict] = json.loads(f.read()).get("jobs")

        return [BackupJob(**job) for job in content]


class BackupResults(BaseModel):
    name: str
    file: Path
    stats: FileStat
