import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class FileOperation(BaseModel):
    source: str
    destination: Optional[Path]


class FileStat(BaseModel):
    uid: int
    gid: int
    create_time: datetime.datetime
    modified_time: datetime.datetime
    access_time: datetime.datetime
    size: str
