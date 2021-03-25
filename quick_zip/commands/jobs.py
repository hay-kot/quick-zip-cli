from pathlib import Path

import typer
from quick_zip.core.settings import settings, console
from quick_zip.schema.backup_job import BackupJob
from quick_zip.services import ui
from rich.columns import Columns
from rich.table import Table
from rich import box

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    config_file: str = typer.Argument(settings.config_file),
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
        table = Table(show_header=True, header_style="bold", title="Job Summary", box=box.SIMPLE)
        table.add_column("Name", style="bold green", width=12)
        table.add_column("Source", justify="center")
        table.add_column("Destination", justify="center")
        table.add_column("All Files", justify="center")

        for job in all_jobs:
            table.add_row(
                job.name,
                job.source.name,
                job.destination.name,
                str(job.all_files),
            )

        console.print(table)
