import json
from pathlib import Path
from typing import Optional

import typer
from rich.columns import Columns
from rich.syntax import Syntax

from quick_zip.commands import jobs
from quick_zip.core.config import CONFIG_FILE, console
from quick_zip.schema.backup_job import BackupJob, PostData
from quick_zip.schema.config import AppConfig
from quick_zip.services import auditer, ui, web, zipper

app = typer.Typer()
app.add_typer(jobs.app, name="jobs")


@app.command()
def docs():
    """💬 Opens quickZip documentation in browser"""
    typer.launch("http://localhost:8000")  #! Place Holder


@app.command()
def config(
    config_file: Optional[str] = typer.Argument(CONFIG_FILE),
    filter: Optional[str] = typer.Option(None, "-f"),
):
    """📄 displays the configuration file"""
    print(CONFIG_FILE)

    if isinstance(config_file, str):
        config_file = Path(config_file)

    with open(config_file, "r") as f:
        content = f.read()

    if filter:
        temp_dict = json.loads(content).get(filter)

        if temp_dict == None:
            console.print(
                f"Error! Could not find key '{filter}' in {config_file}",
                style="red",
            )

            raise typer.Exit()

        content = json.dumps(temp_dict, indent=4)

    syntax = Syntax(content, "json", theme="material", line_numbers=True)
    console.print(syntax)


@app.command()
def audit(
    config_file: str = typer.Argument(CONFIG_FILE),
    job: Optional[list[str]] = typer.Option(None, "-j"),
    verbose: Optional[bool] = typer.Argument("-v"),
):
    """🧐 Performs ONLY the audits for configured jobs"""
    if isinstance(config_file, str):
        config_file = Path(config_file)
        config: AppConfig = AppConfig.from_file(config_file)

    all_jobs = BackupJob.get_job_store(config_file)

    if job:
        all_jobs = [x for x in all_jobs if x.name in job]

    if verbose:
        for my_job in all_jobs:
            my_job: BackupJob
            audit_report = auditer.audit(my_job.final_dest, my_job.oldest)


@app.command()
def run(
    config_file: str = typer.Argument(CONFIG_FILE),
    job: Optional[list[str]] = typer.Option(None, "-j"),
):
    """✨ The main entrypoint for the application. By default will run"""

    if isinstance(config_file, str):
        config_file = Path(config_file)
    config: AppConfig = AppConfig.from_file(config_file)

    all_jobs = BackupJob.get_job_store(config_file)

    if job:
        all_jobs = [x for x in all_jobs if x.name in job]

    reports = []

    with console.status("[bold green]Generating ZipFile...") as _status:
        for job in all_jobs:
            job: BackupJob
            console.rule(f"QuickZip: '{job.name}'")
            report = zipper.run(job)

            reports.append(report)

    if config.enable_webhooks:
        web.post_file_data(config.webhook_address, body=PostData(data=reports))


def main():
    app()


if __name__ == "__main__":
    main()
