import os
import time
import zipfile as zf
from pathlib import Path

from quick_zip.core.settings import console, settings
from quick_zip.schema.backup_job import BackupJob, BackupResults
from quick_zip.services import checker, ui
from quick_zip.utils import fstats
from rich.columns import Columns
from rich.layout import Panel
from rich.progress import Progress


def get_all_source_size(sources: list[Path]):
    total = 0

    for src in sources:
        if src.is_file():
            total += src.stat().st_size
        else:
            total += sum(f.stat().st_size for f in src.glob("**/*") if f.is_file())

    return total


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


def zipdir(path, ziph, progress: Progress, task, top_dir):
    for root, _dirs, files in os.walk(path):

        for file in files:
            progress.update(task, description=f"[red]Zipping...{Path(file).name}")
            in_zip_path = os.path.relpath(os.path.join(root, file), top_dir)
            ziph.write(os.path.join(root, file), in_zip_path)

            if not progress.finished:
                file = Path(root).joinpath(file)
                progress.update(task, advance=file.stat().st_size)


def run(job: BackupJob, verbose=False) -> dict:
    dest = get_backup_name(job.name, job.final_dest, "zip", is_file=True)
    dest = job.final_dest.joinpath(dest)

    to_zip_size = get_all_source_size(job.source)
    with zf.ZipFile(dest.absolute(), mode="a") as f:
        with Progress() as progress:

            task = progress.add_task("[red]Zipping...", total=to_zip_size)

            for src in job.source:
                top_dir = "/"
                progress.update(task, description=f"[red]Zipping... {src.name}")
                if src.is_dir():
                    top_dir = src
                    zipdir(src, f, progress, task, top_dir)
                else:
                    f.write(src, top_dir.joinpath(src.name))

                    if not progress.finished:
                        progress.update(task, advance=dest.stat().st_size)

    compression = compress_dif(to_zip_size, get_all_source_size([dest]))
    console.print(compression)

    clean_up_cards = []
    if job.clean_up:
        _backups, dest_clean = clean_up_dir(job.final_dest, job.keep)
        clean_up_cards = [ui.file_card(x, title_color="red", append_text="[i]From Source") for x in dest_clean]

    # if job.clean_up_source:
    #     _backups, src_clean = clean_up_dir(job.source, job.keep)
    #     for file in src_clean:
    #         clean_up_cards.append(ui.file_card(file, title_color="red", append_text="[i]From Destionation"))

    audit_report = None
    if job.audit:
        audit_report = checker.audit(job.final_dest, job.oldest)

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


def get_all_stats(path: Path) -> dict:
    my_stats = {"name": path.name}
    my_stats.update(fstats.get_stats(path))
    return


def get_deletes(directory: Path, keep: int) -> list[Path]:
    clean_list = sorted(directory.iterdir(), key=os.path.getmtime, reverse=True)
    deletes = [x for x in clean_list if x.is_file()]
    return deletes[keep:]


def clean_up_dir(directory: Path, keep: int) -> list[Path]:
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
        while list(dest.glob(f"{final_name}*")) != []:
            final_name = f"{file_stem}_{add_timestr}.{extension}"
            x += 1
    else:
        final_name = f"{file_stem}"

        x = 1
        while list(dest.glob(f"{final_name}.*")) != []:
            final_name = f"{file_stem}_{add_timestr}"
            x += 1

    console.print(f"Creating: {final_name}")
    return final_name
