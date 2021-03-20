from pathlib import Path

from quick_zip.services.file_stats import sizeof_fmt
from rich.layout import Panel


def file_card(my_path: Path, title=None, title_color=None, append_text=None):
    title = title if title else my_path.name
    if title_color:
        title = f"[b {title_color}]{title}[/]"

    emoji = "📁" if my_path.is_dir() else "📄"

    # File Stats
    try:
        raw_stats = my_path.stat()
        size = sizeof_fmt(raw_stats.st_size)
    except FileNotFoundError:
        size = "[red]Deleted[/]"

    content = f"""{emoji} {size}
Parent: {my_path.parent.name}
"""
    if append_text:
        content += append_text
    content = Panel(content, title=title)

    return content
