from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer

from quick_zip.commands import audit, config, jobs
from quick_zip.core.settings import APP_VERSION, console, settings
from quick_zip.schema.backup_job import BackupJob
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


@app.callback()
def version_callback(v):
    if v:
        console.print(f"Quick Zip CLI Version: {APP_VERSION}")
    return


@app.command()
def run(
    config_file: Path = typer.Argument(settings.config_file),
    job: Optional[List[str]] = typer.Option(None, "-j"),
    verbose: bool = typer.Option(False, "-v"),
):
    """✨ The main entrypoint for the application. By default will run"""

    if isinstance(config_file, Path):
        settings.update_settings(config_file)

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

    if settings.enable_webhooks:
        web.post_file_data(settings.webhook_address, body=reports)


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    version: Optional[bool] = typer.Option(None, "--version", callback=version_callback),
):
    typer.Exit()


if __name__ == "__main__":
    typer.run(main)
