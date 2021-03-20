from pathlib import Path

from quick_zip.core.config import console
from quick_zip.schema.backup_job import Audit, BackupFile
from quick_zip.services.file_stats import get_days_old
from quick_zip.utils import cards
from rich.columns import Columns


def audit(destination: Path, oldest_by_days: int) -> Audit:
    console.print(f"\n[b]Audit Report `{destination.name}`", justify="center")

    all_files = []
    for file in destination.iterdir():
        all_files.append(BackupFile(path=file, days_old=get_days_old(file)))

    all_files.sort(key=lambda x: x.days_old)

    newest: BackupFile = all_files[0]
    oldest: BackupFile = all_files[-1]
    health = True if newest.days_old < oldest_by_days else False

    my_cards = []
    for file in all_files:
        file: BackupFile
        health = True if file.days_old < oldest_by_days else False
        color = "green" if health else "red"
        append_text = f"""[b {color}]{file.days_old} Days Old[/]"""
        my_cards.append(
            cards.file_card(file.path, title_color=color, append_text=append_text)
        )

    content = Columns(my_cards, equal=False, expand=True)
    console.print(content)

    return Audit(
        healthy=health,
        newest=newest,
        oldest=oldest,
    )
