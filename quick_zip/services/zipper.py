import os
import time
import zipfile as zf
from pathlib import Path
from typing import List

from quick_zip.core.settings import console, settings
from quick_zip.schema.backup_job import BackupJob, BackupResults
from quick_zip.services import checker, ui
from quick_zip.utils import fstats
from rich.columns import Columns
from rich.progress import Progress


def compress_dif(size_before, size_after):
    pretty_before = fstats.sizeof_fmt(size_before)
    pretty_after = fstats.sizeof_fmt(size_after)

    if size_after == size_before:
        percent = 100.0
    try:
        percent = (abs(size_after - size_before) / size_before) * 100.0
    except ZeroDivisionError:
        percent = 0

    return f"Compression '{pretty_before}' -> '{pretty_after}' | [b]Size Reduced {round(percent)}%"


def create_archive(sources: List[Path], dest: Path, to_zip_size: int):
    def zipdir(path, ziph, top_dir):
        for root, _dirs, files in os.walk(path):

            for file in files:
                progress.update(task, description=f"[red]Zipping...{Path(file).name}")
                in_zip_path = os.path.relpath(os.path.join(root, file), top_dir)
                ziph.write(os.path.join(root, file), in_zip_path)

                if not progress.finished:
                    file = Path(root).joinpath(file)
                    progress.update(task, advance=file.stat().st_size)

    with zf.ZipFile(dest, mode="a") as f:
        with Progress() as progress:

            task = progress.add_task("[red]Zipping...", total=to_zip_size)

            for src in sources:
                top_dir = "/"
                progress.update(task, description=f"[red]Zipping... {src.name}")

                if src.is_dir():
                    top_dir = src
                    zipdir(top_dir, f, top_dir)
                else:
                    f.write(src, top_dir.joinpath(src.name))

                    if not progress.finished:
                        progress.update(task, advance=dest.stat().st_size)


def get_deletes(directory: Path, keep: int) -> List[Path]:
    clean_list = sorted(directory.iterdir(), key=os.path.getmtime, reverse=True)
    deletes = [x for x in clean_list if x.is_file()]
    return deletes[keep:]


def get_backup_name(job_name, dest, extension: str = "", is_file: bool = False) -> str:
    timestr = time.strftime("%Y.%m.%d")
    add_timestr = time.strftime("%H.%M.%S")

    file_stem = f"{job_name}_{timestr}"

    final_name: Path
    x = 1
    if is_file:
        final_name = f"{file_stem}.{extension}"

        while list(dest.glob(f"{final_name}*")) != []:
            final_name = f"{file_stem}_{add_timestr}.{extension}"
            x += 1
    else:
        final_name = f"{file_stem}"

        while list(dest.glob(f"{final_name}.*")) != []:
            final_name = f"{file_stem}_{add_timestr}"
            x += 1

    console.print(f"Creating: {final_name}")
    return final_name


def cleaner(job: BackupJob):
    def clean_up_dir(directory: Path, keep: int) -> List[Path]:
        clean_list = get_deletes(directory, keep)

        for file in clean_list:
            file.unlink()

        # backups = [get_all_stats(x) for x in directory.iterdir()]

        return clean_list

    cards = []
    dest_clean = None
    if job.clean_up:
        dest_clean = clean_up_dir(job.final_dest, job.keep)
        cards += [ui.file_card(x, title_color="red", append_text="[i]From Destination") for x in dest_clean]

    return cards, dest_clean


def run(job: BackupJob) -> BackupResults:
    dest = get_backup_name(job.name, job.final_dest, "zip", is_file=True)
    dest = job.final_dest.joinpath(dest)

    to_zip_size = fstats.get_directory_size(job.source)
    create_archive(job.source, dest, to_zip_size)

    compression = compress_dif(to_zip_size, fstats.get_directory_size(dest))
    console.print(compression)

    clean_up_cards, dest_clean = cleaner(job)

    audit_report = checker.audit(job.final_dest, job.oldest) if job.audit else None

    if settings.verbose and job.clean_up:
        console.print(f"\n[b]🗑  Cleanup '{job.destination}'", justify="center")
        content = Columns(clean_up_cards, equal=True, expand=False)
        console.print(content)
    elif job.clean_up:
        for trash in dest_clean:
            trash: Path
            console.print(f"\n[b]Cleanup '{job.destination}'")

            console.print(f"  🗑  [red]{trash.name}")

    return BackupResults(
        name=job.name,
        job=job,
        file=dest,
        stats=fstats.get_stats(dest).get("stats"),
        audit=audit_report,
    )
