import json
from pathlib import Path
from typing import Optional

import typer
from quick_zip.core.config import CONFIG_FILE, console
from quick_zip.schema.backup_job import BackupJob, PostData
from quick_zip.schema.config import AppConfig
from quick_zip.services import auditer, ui, web, zipper
from rich.columns import Columns
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    config_file: str = typer.Argument(CONFIG_FILE),
    verbose: bool = typer.Option(False, "-v"),
):
    if isinstance(config_file, str):
        config_file = Path(config_file)
    # config: AppCnfig = AppConfig.from_file(config_file)

    all_jobs = BackupJob.get_job_store(config_file)

    if verbose:
        all_cards = [ui.job_card(x) for x in all_jobs]
        content = Columns(all_cards, equal=False, expand=True)
        console.print(content)

    else:
        console.print("\n")
        table = Table(show_header=True, header_style="bold", title="Job Summary")
        table.add_column("Name", style="bold green", width=12)
        table.add_column("Source")
        table.add_column("Destination")
        table.add_column("All Files", justify="center")
        table.add_column("Clean up Dst", justify="center")
        table.add_column("Clean up Src", justify="center")
        table.add_column("Keep", justify="center")
        table.add_column("Audit", justify="center")
        table.add_column("Oldest", justify="center")

        for job in all_jobs:
            table.add_row(
                job.name,
                job.source.name,
                job.destination.name,
                str(job.all_files),
                str(job.clean_up),
                str(job.clean_up_source),
                f"{job.keep} backups",
                str(job.audit),
                f"{job.oldest} Days",
            )

        console.print(table)
