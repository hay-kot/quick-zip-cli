import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.syntax import Syntax

from quick_zip.core.config import CONFIG_FILE
from quick_zip.schema.backup_job import BackupJob
from quick_zip.schema.config import AppConfig
from quick_zip.services.backups import clean_up_dest, run_job
from quick_zip.utils.backup import post_file_data
from quick_zip.utils.custom_logger import logger

console = Console()

app = typer.Typer()


def pre_work():
    logger.info("-------- START UP --------")

    pass


def clean_up():
    logger.info("-------- FINISHED --------")

    pass


@app.command()
def config(
    config_file: Optional[str] = typer.Argument(CONFIG_FILE),
    filter: Optional[str] = typer.Option(None, "-f"),
):
    if isinstance(config_file, str):
        config_file = Path(config_file)

    # config: AppConfig = AppConfig.from_file(config_file)
    # all_jobs = BackupJob.get_job_store(config_file)

    with open(config_file, "r") as f:
        content = f.read()

    if filter:
        temp_dict = json.loads(content).get(filter)
        content = json.dumps(temp_dict, indent=4)

    syntax = Syntax(content, "json", theme="material", line_numbers=True)
    console.print(syntax)


@app.command()
def run(config_file: str = typer.Argument(CONFIG_FILE)):
    pre_work()

    if isinstance(config_file, str):
        config_file = Path(config_file)

    config: AppConfig = AppConfig.from_file(config_file)
    all_jobs = BackupJob.get_job_store(config_file)

    reports = []
    with console.status("[bold green]Generating ZipFile...") as _status:
        for job in all_jobs:
            console.log(f"Running Job {job.name}")
            report = run_job(job)

            if job.clean_up:
                clean_up_dest(job.destination, job.keep, job.name)

            if job.clean_up_source:
                clean_up_dest(job.source, job.keep, job.name)
            reports.append(report)

            if config.enable_webhooks:
                post_file_data(config.webhook_address, reports)

    clean_up()


@app.command()
def other(name):
    console.print("Hello", f"{name}", style="bold red")


def main():
    app()


if __name__ == "__main__":
    main()
