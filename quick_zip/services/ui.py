from pathlib import Path

from quick_zip.schema.backup_job import BackupJob
from quick_zip.utils import fstats
from rich.layout import Panel


def file_card(my_path: Path, title=None, title_color=None, append_text=None):
    title = title if title else my_path.name
    if title_color:
        title = f"[b {title_color}]{title}[/]"

    emoji = "📁" if my_path.is_dir() else "📄"

    # File Stats
    try:
        raw_stats = my_path.stat()
        size = fstats.sizeof_fmt(raw_stats.st_size)
    except FileNotFoundError:
        size = "[red]Deleted[/]"

    content = f"""\
{emoji} {size}
Parent: {my_path.parent.name}
"""
    if append_text:
        content += append_text
    content = Panel(content, title=title)

    return content


def job_card(job_obj: BackupJob):
    title = f"💼 [b]{job_obj.name}[/]"

    # File Stats

    content = f"""\
[b blue]Source[/]       = [i red]{job_obj.source}[/]
[b blue]Destination[/]  = [i red]{job_obj.destination}[/]
[b blue]All Files[/]    = [i red]{job_obj.all_files}[/]
[b blue]Audit[/]        = [i red]{job_obj.audit}[/]
[b blue]Keep[/]         = [i red]{job_obj.keep}[/]
[b blue]Clean Up Dst[/] = [i red]{job_obj.clean_up}[/]
[b blue]Clean Up Src[/] = [i red]{job_obj.clean_up_source}[/]
[b blue]Oldest[/]       = [i red]{job_obj.oldest}[/]"""
    return Panel(content, title=title)
