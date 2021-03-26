import random
import shutil
import string
from pathlib import Path

import pytest
from quick_zip.core.settings import settings
from quick_zip.schema.backup_job import BackupJob
from typer.testing import CliRunner

CWD = Path(__file__).parent
RESOURCES = CWD.joinpath("resources")
DEST = RESOURCES.joinpath("dest")
TEST_CONFIG = RESOURCES.joinpath("config.toml")

# Assign Testing Defaults
settings.update_settings(TEST_CONFIG)


@pytest.fixture
def test_app(monkeypatch):
    monkeypatch.setenv("QUICKZIP_CONFIG", str(TEST_CONFIG))

    return CliRunner()


@pytest.fixture
def job_store():
    return BackupJob.get_job_store(settings.config_file)


@pytest.fixture
def test_config():
    return TEST_CONFIG


@pytest.fixture
def resource_dir():
    return RESOURCES


@pytest.fixture
def dest_dir():
    yield DEST
    [x.unlink() for x in DEST.glob("*.zip")]


@pytest.fixture()
def temp_dir():
    temp_dir = RESOURCES.joinpath(".temp")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture()
def test_files():
    files = []
    letters = string.ascii_lowercase

    for x in range(5):
        result_str = "".join(random.choice(letters) for i in range(1000))
        RESOURCES.joinpath("sort").mkdir(exist_ok=True)
        file = RESOURCES.joinpath("sort", f"file_{x}.txt")

        with open(file, "w") as f:
            f.write(result_str)

        files.append(file)

    return files


@pytest.fixture()
def file_with_content():
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(1000))

    file = RESOURCES.joinpath("src", "temp_file.txt")

    with open(file, "w") as f:
        f.write(result_str)

    yield file
    file.unlink()
