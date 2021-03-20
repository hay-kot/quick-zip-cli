import os
from datetime import datetime
from pathlib import Path


def sizeof_fmt(size, decimal_places=2):
    for unit in ["B", "kB", "MB", "GB", "TB", "PB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%b %d, %Y")


def get_days_old(path: Path) -> int:
    time_create = datetime.fromtimestamp(int(os.stat(path).st_birthtime))
    time_now = datetime.now()
    difference = time_now - time_create
    duration_in_s = difference.total_seconds() // 86400  # Second in a Day
    return int(duration_in_s)


def get_stats(file_folder: Path) -> dict:
    raw_stats = file_folder.stat()

    pretty_stats = {
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
    return pretty_stats
