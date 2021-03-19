import shutil
from pathlib import Path

from quick_zip.schema.backup_job import BackupJob, BackupResults
from quick_zip.services.backups import get_deletes, run_job


def test_keep_sort(dest_dir):
    """ 1 is the oldest, 5 is the newest"""
    test_dir = dest_dir.joinpath("sort")
    one = test_dir.joinpath("1.txt")
    two = test_dir.joinpath("2.txt")
    three = test_dir.joinpath("3.txt")
    four = test_dir.joinpath("4.txt")
    _five = test_dir.joinpath("5.txt")

    deletes = get_deletes(test_dir, 1)
    expected = [one, two, three, four]
    assert set(deletes) == set(expected)

    deletes = get_deletes(test_dir, 2)
    expected = [one, two, three]
    assert set(deletes) == set(expected)

    deletes = get_deletes(test_dir, 3)
    expected = [one, two]
    assert set(deletes) == set(expected)

    deletes = get_deletes(test_dir, 4)
    expected = [one]
    assert set(deletes) == set(expected)

    deletes = get_deletes(test_dir, 5)
    expected = []
    assert set(deletes) == set(expected)


class BackupJobTests:
    @staticmethod
    def test_default_values(job_store, resource_dir, dest_dir):
        assert isinstance(job_store, BackupJob)

        # Test Default Values
        assert job_store.name == "Test Job"
        assert job_store.source == resource_dir.joinpath("src")
        assert job_store.destination == dest_dir
        assert job_store.clean_up == False
        assert job_store.all_files == False
        assert job_store.keep == 4

    @staticmethod
    def test_replace_variables(config_with_vars: Path):
        VAR_1 = "var_1_value"
        VAR_2 = "var_2_value"
        job_store = BackupJob.get_job_store(config_with_vars)

        job = job_store[0]

        assert job.name == f"{VAR_1}"
        assert job.source == Path(f"/{VAR_2}/entry_1/{VAR_2}")
        assert job.destination == Path(f"/home/entry_1/{VAR_2}")

    @staticmethod
    def test_get_job_store(resource_dir):
        jobs = BackupJob.get_job_store(resource_dir.joinpath("config.json"))
        assert all([isinstance(x, BackupJob) for x in jobs])

    @staticmethod
    def test_contents(job_store, temp_dir):
        data: BackupResults = run_job(job_store)
        assert data

        temp_dir.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(data.file, temp_dir)

        with open(temp_dir.joinpath("my_files.txt"), "r") as f:
            content = f.read()

        assert content == "this is my test file contents"
