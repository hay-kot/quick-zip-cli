import os
import shutil
import time
from pathlib import Path

from core.config import ZIP_TYPES
from schema.backup_job import BackupJob, BackupResults
from utils.custom_logger import logger

from services.file_stats import get_stats


def get_all_stats(path: Path) -> dict:
    my_stats = {"name": path.name}
    my_stats.update(get_stats(path))
    return


def get_deletes(directory: Path, keep: int) -> list[Path]:
    clean_list = sorted(directory.iterdir(), key=os.path.getmtime, reverse=True)
    deletes = [x for x in clean_list if x.is_file()]
    return deletes[keep:]


def clean_up_dest(directory: Path, keep: int, name: str = "") -> list[Path]:
    logger.info(f"Cleaning Directory: {directory.name}")
    logger.info(f"Keeping... {keep}")
    clean_list = get_deletes(directory, keep)

    for file in clean_list:
        file.unlink()

    backups = [get_all_stats(x) for x in directory.iterdir()]

    logger.debug(backups)

    return backups


def run_job(job: BackupJob) -> dict:
    timestr = time.strftime("%Y.%m.%d")

    dest = job.destination.joinpath(f"{job.source.stem}_{timestr}")

    if job.source.is_dir():
        logger.info(f"Zipping Folder {job.source}")
        shutil.make_archive(dest, "zip", job.source)
        dest = job.destination.joinpath(f"{job.source.stem}_{timestr}.zip")

    elif job.source.is_file() and job.source.suffix.lower() in ZIP_TYPES:
        logger.info(f"Copying Archive {job.source}")
        dest = Path(shutil.copy(job.source, job.destination))

    elif job.source.is_file():
        dest = Path(shutil.copy(job.source, f"{dest}{job.source.suffix}"))

    else:
        raise Exception(
            f"Fatal Error: {job.source} is not file or folder... What is it?"
        )

    all_backups = clean_up_dest(job.destination, job.keep, job.name)

    return BackupResults(name=job.name, file=dest, stats=get_stats(dest).get("stats"))
