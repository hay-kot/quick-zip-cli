import os
import shutil
import time
from pathlib import Path

from core.config import ZIP_TYPES
from rich.console import Console
from schema.backup_job import BackupJob, BackupResults
from utils.custom_logger import logger

from services.file_stats import get_stats

console = Console()


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
        logger.info(f"Dropping... {file.name}")
        file.unlink()

    backups = [get_all_stats(x) for x in directory.iterdir()]

    logger.debug(backups)

    return backups


def get_backup_name(job_name, dest, extension: str = "", is_file: bool = False) -> str:
    timestr = time.strftime("%Y.%m.%d")
    add_timestr = time.strftime("%H.%M.%S")

    file_stem = f"{job_name}_{timestr}"

    final_name: Path
    if is_file:
        final_name = f"{file_stem}.{extension}"

        x = 1
        while list(dest.glob(f"{final_name}.*")) != []:
            final_name = f"{file_stem}.{extension}_{add_timestr}"
            x += 1
    else:
        final_name = f"{file_stem}"

        x = 1
        while list(dest.glob(f"{final_name}.*")) != []:
            final_name = f"{file_stem}_{add_timestr}"
            x += 1

    console.log("\n")  # Keeps Logger on New line
    logger.info(f"Name Determined {final_name}")
    return final_name


def run_job(job: BackupJob) -> dict:

    if job.source.is_dir():
        backup_name = get_backup_name(job.name, job.destination)
        logger.info(f"Zipping Folder {job.source}")
        shutil.make_archive(job.destination.joinpath(backup_name), "zip", job.source)
        dest = job.destination.joinpath(backup_name + ".zip")

    elif job.source.is_file() and job.source.suffix.lower() in ZIP_TYPES:
        dest = get_backup_name(job.name, job.destination, job.source.suffix)

        logger.info(f"Copying Archive {job.source}")
        dest = Path(shutil.copy(job.source, dest))

    elif job.source.is_file():
        backup_name = get_backup_name(job.name, job.destination, job.source.suffix)
        dest = Path(shutil.copy(job.source, backup_name))

    else:
        raise Exception(
            f"Fatal Error: {job.source} is not file or folder... What is it?"
        )

    return BackupResults(name=job.name, file=dest, stats=get_stats(dest).get("stats"))
