import shutil
from pathlib import Path

import pytest
from quick_zip.schema.backup_job import BackupJob, BackupResults
from quick_zip.services.zipper import get_deletes, run


def test_get_job_store(resource_dir):
    jobs = BackupJob.get_job_store(resource_dir.joinpath("config.toml"))
    assert all([isinstance(x, BackupJob) for x in jobs])


def test_validate_job_store(job_store, resource_dir, dest_dir):
    for job in job_store:
        pass


def test_replace_variables(test_config: Path):
    VAR_1 = "var_1_value"
    VAR_2 = "var_2_value"
    job_store = BackupJob.get_job_store(test_config)

    job = job_store[0]

    assert job.name == f"{VAR_1}"
    assert job.source == [Path(f"/{VAR_2}/entry_1/{VAR_2}")]
    assert job.destination == Path(f"/home/entry_1/{VAR_2}")


def test_content_validation(job_store, temp_dir, dest_dir, file_with_content: Path, resource_dir):
    job_to_run = job_store[2]
    job_to_run: BackupJob
    job_to_run.source = [resource_dir.joinpath("src")]
    job_to_run.destination = dest_dir

    with open(file_with_content, "r") as f:
        valid_content = f.read()

    data: BackupResults = run(job_to_run)
    assert data

    temp_dir.mkdir(parents=True, exist_ok=True)
    shutil.unpack_archive(data.file, temp_dir)

    with open(temp_dir.joinpath(file_with_content.name), "r") as f:
        content = f.read()

    assert content == valid_content


@pytest.mark.parametrize("x", [1, 2, 3, 4])
def test_keep_sort(resource_dir, x):
    """ 1 is the oldest, 5 is the newest"""
    test_dir = resource_dir.joinpath("sort")
    one = test_dir.joinpath("1.txt")
    two = test_dir.joinpath("2.txt")
    three = test_dir.joinpath("3.txt")
    four = test_dir.joinpath("4.txt")
    five = test_dir.joinpath("5.txt")

    all_files = [one, two, three, four, five]

    deletes = get_deletes(test_dir, x)
    expected = all_files[:-x]
    assert set(deletes) == set(expected)
