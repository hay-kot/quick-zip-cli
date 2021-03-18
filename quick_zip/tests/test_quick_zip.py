import shutil
from pathlib import Path

import pytest
from core.config import APP_VERSION, CONFIG_FILE, generate_config
from schema.backup_job import BackupJob, BackupResults
from schema.config import AppConfig
from services.backups import run_job

CWD = Path(__file__).parent
RESOURCES = CWD.joinpath("resources")
DEST = RESOURCES.joinpath("dest")

shutil.rmtree(DEST, ignore_errors=True)


@pytest.fixture()
def job_store():
    return BackupJob(
        name="Test Job", source=RESOURCES.joinpath("src"), destination=DEST
    )


def test_version():
    assert APP_VERSION == "v0.1.0"


class ConfigTests:
    @staticmethod
    def test_generate_config():
        app_config = generate_config(CONFIG_FILE)

        assert isinstance(app_config, AppConfig)
        test_config = AppConfig(
            enable_webhooks=True,
            webhook_address="https://webhooks.com/webhook",
            relative_path="/my/backup/dir",
        )

        assert app_config.enable_webhooks == test_config.enable_webhooks
        assert app_config.webhook_address == test_config.webhook_address
        assert app_config.relative_path == test_config.relative_path


class BackupJobTests:
    @staticmethod
    def test_default_values(job_store):
        assert isinstance(job_store, BackupJob)

        # Test Default Values
        assert job_store.name == "Test Job"
        assert job_store.source == RESOURCES.joinpath("src")
        assert job_store.destination == DEST
        assert job_store.clean_up == False
        assert job_store.all_files == False
        assert job_store.keep == 4

    @staticmethod
    def test_get_job_store():
        job_store = BackupJob.get_job_store(RESOURCES.joinpath("config.json"))
        assert all([isinstance(x, BackupJob) for x in job_store])

    @staticmethod
    def test_contents(job_store):
        data: BackupResults = run_job(job_store)
        assert data

        out_dir = RESOURCES.joinpath(".temp")
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(data.file, out_dir)

        with open(out_dir.joinpath("my_files.txt"), "r") as f:
            content = f.read()

        assert content == "this is my test file contents"
