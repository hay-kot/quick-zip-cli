from pathlib import Path

from rich.columns import Columns
from rich.console import Console
from rich.layout import Panel

from quick_zip.utils import fstats


def file_panel(my_path: Path, title=None, title_color=None, append_text=None):
    title = title if title else my_path.name
    if title_color:
        title = f"[b {title_color}]{title}[/]"


    emoji = "📁" if my_path.is_dir() else "📄"

    # File Stats
    raw_stats = my_path.stat()
    size = fstats.sizeof_fmt(raw_stats.st_size)

    content = f"""{emoji} {size}
Parent: {my_path.parent.name}
{append_text if append_text else ""}
    """
    content = Panel(content, title=title)

    return content


console = Console()

this_list = list(Path(__file__).parent.iterdir())

cards = [file_panel(x, title_color="red") for x in this_list]
content = columns = Columns(cards, equal=True, expand=True)

console.print(content)
