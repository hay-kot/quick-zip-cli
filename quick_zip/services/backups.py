import os
import shutil
import time
from pathlib import Path

from quick_zip.core.config import ZIP_TYPES, console
from quick_zip.schema.backup_job import BackupJob, BackupResults
from quick_zip.services import auditer
from quick_zip.services.file_stats import get_stats
from quick_zip.utils import cards
from rich.columns import Columns
from rich.layout import Panel


def run(job: BackupJob) -> dict:

    if job.source.is_dir():
        backup_name = get_backup_name(job.name, job.final_dest)
        shutil.make_archive(job.final_dest.joinpath(backup_name), "zip", job.source)
        dest = job.final_dest.joinpath(backup_name + ".zip")

    elif job.source.is_file() and job.source.suffix.lower() in ZIP_TYPES:
        dest = get_backup_name(job.name, job.final_dest, job.source.suffix)

        console.print(f"Copying Archive {job.source}")
        dest = Path(shutil.copy(job.source, dest))

    elif job.source.is_file():
        backup_name = get_backup_name(job.name, job.final_dest, job.source.suffix)
        dest = Path(shutil.copy(job.source, backup_name))

    else:
        raise Exception(
            f"Fatal Error: {job.source} is not file or folder... What is it?"
        )

    if job.clean_up:
        _backups, dest_clean = clean_up_dest(job.final_dest, job.keep)

    if job.clean_up_source:
        _backups, src_clean = clean_up_dest(job.source, job.keep)

    audit_report = None
    if job.audit:
        audit_report = auditer.audit(job.final_dest, job.oldest)

    clean_up_cards = [
        cards.file_card(x, title_color="red", append_text="[i]From Source")
        for x in dest_clean
    ]

    for file in src_clean:
        clean_up_cards.append(
            cards.file_card(file, title_color="red", append_text="[i]From Destionation")
        )

    console.print(f"\n[b]🗑  Cleanup '{job.destination}'", justify="center")
    content = Columns(clean_up_cards, equal=True, expand=False)
    console.print(content)

    return BackupResults(
        name=job.name,
        job=job,
        file=dest,
        stats=get_stats(dest).get("stats"),
        audit=audit_report,
    )


def get_all_stats(path: Path) -> dict:
    my_stats = {"name": path.name}
    my_stats.update(get_stats(path))
    return


def get_deletes(directory: Path, keep: int) -> list[Path]:
    clean_list = sorted(directory.iterdir(), key=os.path.getmtime, reverse=True)
    deletes = [x for x in clean_list if x.is_file()]
    return deletes[keep:]


def clean_up_dest(directory: Path, keep: int) -> list[Path]:
    clean_list = get_deletes(directory, keep)

    for file in clean_list:
        file.unlink()

    backups = [get_all_stats(x) for x in directory.iterdir()]

    return backups, clean_list


def cleanup_card(src_list: list[Path], dest_list: list[Path], title):
    content = ""
    src_content = "[b red]Source Directory[/]\n"
    for p in src_list:
        src_content += p.name + "\n"

    dest_content = "[b red]Destionation Directory[/]\n"
    for p in dest_list:
        dest_content += p.name + "\n"

    content += src_content if len(src_list) > 0 else ""
    content += dest_content if len(dest_list) > 0 else ""

    return Panel(content, title=title, expand=False)


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

    console.print(f"Creating: {final_name}")
    return final_name
