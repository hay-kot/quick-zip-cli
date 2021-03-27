from datetime import datetime
from pathlib import Path
from typing import List, Union


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%b %d, %Y")


def sizeof_fmt(size, decimal_places=2):
    for unit in ["B", "kB", "MB", "GB", "TB", "PB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def get_days_old(path: Path) -> int:
    time_create = datetime.fromtimestamp(int(path.stat().st_ctime))
    time_now = datetime.now()
    difference = time_now - time_create
    duration_in_s = difference.total_seconds() // 86400  # Second in a Day
    return int(duration_in_s)


def get_directory_size(sources: Union[List[Path], Path], pretty=False):
    sources = [sources] if isinstance(sources, Path) else sources

    total = 0

    for src in sources:
        if src.is_file():
            total += src.stat().st_size
        else:
            total += sum(f.stat().st_size for f in src.glob("**/*") if f.is_file())

    if pretty:
        return sizeof_fmt(total)

    return total


def get_stats(file_folder: Path) -> dict:
    raw_stats = file_folder.stat()

    return {
        "stats": {
            "uid": raw_stats.st_uid,
            "gid": raw_stats.st_gid,
            "create_time": raw_stats.st_ctime,
            "created_time_text": format_time(raw_stats.st_ctime),
            "modified_time": raw_stats.st_mtime,
            "modified_time_text": format_time(raw_stats.st_mtime),
            "access_time": raw_stats.st_atime,
            "access_time_text": format_time(raw_stats.st_atime),
            "size": sizeof_fmt(raw_stats.st_size),
        }
    }
