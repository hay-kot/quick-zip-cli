from pathlib import Path
from time import sleep
from typing import Optional

import typer
from rich.console import Console
from rich.progress import track

from core.config import CONFIG_FILE, config
from schema.backup_job import BackupJob
from schema.config import AppConfig
from services.backups import clean_up_dest, run_job
from utils.backup import post_file_data
from utils.custom_logger import logger

console = Console()

app = typer.Typer()


def pre_work():
    logger.info("-------- START UP --------")

    pass


def clean_up():
    logger.info("-------- FINISHED --------")

    pass


@app.command()
def test():
    print("Test")


@app.command()
def run(cli_config: str = typer.Argument(config)):
    if cli_config:
        print(cli_config)
    else:
        print(config)
    pre_work()
    all_jobs = BackupJob.get_job_store(CONFIG_FILE)

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


if __name__ == "__main__":
    config = config
    app()
    # main(config)
