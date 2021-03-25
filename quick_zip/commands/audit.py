from pathlib import Path
from typing import Optional

import typer
from quick_zip.core.settings import AppSettings, settings
from quick_zip.schema.backup_job import BackupJob
from quick_zip.services import checker

app = typer.Typer()


@app.callback()
def verbose(verbose: bool = False):
    settings.verbose = verbose


@app.callback(invoke_without_command=True)
def audit(
    config_file: str = typer.Argument(settings.config_file),
    job: Optional[list[str]] = typer.Option(None, "-j"),
):
    """🧐 Performs ONLY the audits for configured jobs"""
    if isinstance(config_file, str):
        config_file = Path(config_file)
        config: AppSettings = AppSettings.from_file(config_file)

    all_jobs = BackupJob.get_job_store(config_file)

    if job:
        all_jobs = [x for x in all_jobs if x.name in job]

    for my_job in all_jobs:
        my_job: BackupJob
        audit_report = checker.audit(my_job.final_dest, my_job.oldest)
