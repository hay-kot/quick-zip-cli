from pathlib import Path
from typing import Optional

import typer

from quick_zip.commands import audit, config, jobs
from quick_zip.core.settings import CONFIG_FILE, AppSettings, console, settings
from quick_zip.schema.backup_job import BackupJob, PostData
from quick_zip.services import web, zipper

app = typer.Typer()
app.add_typer(jobs.app, name="jobs")
app.add_typer(audit.app, name="audit")
app.add_typer(config.app, name="config")


@app.command()
def docs():
    """💬 Opens quickZip documentation in browser"""
    typer.launch("https://hay-kot.github.io/quick-zip-cli/")


@app.callback()
def verbose(verbose: bool = False):
    settings.verbose = verbose


@app.command()
def run(
    config_file: str = typer.Argument(CONFIG_FILE),
    job: Optional[list[str]] = typer.Option(None, "-j"),
    verbose: bool = typer.Option(False, "-v"),
):
    """✨ The main entrypoint for the application. By default will run"""

    if isinstance(config_file, str):
        config_file = Path(config_file)
    config: AppSettings = AppSettings.from_file(config_file)

    all_jobs = BackupJob.get_job_store(config_file)

    if job:
        all_jobs = [x for x in all_jobs if x.name in job]

    reports = []

    for job in all_jobs:
        job: BackupJob
        console.print()
        console.rule(f"QuickZip: '{job.name}'")
        report = zipper.run(job)

        reports.append(report)

    if config.enable_webhooks:
        web.post_file_data(config.webhook_address, body=PostData(data=reports))


def main():
    app()


if __name__ == "__main__":
    main()
