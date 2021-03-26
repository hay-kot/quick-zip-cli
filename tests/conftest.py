import random
import shutil
import string
from pathlib import Path
from time import sleep

import pytest
from quick_zip.core.settings import settings
from quick_zip.schema.backup_job import BackupJob
from typer.testing import CliRunner

CWD = Path(__file__).parent
RESOURCES = CWD.joinpath("resources")
DEST = RESOURCES.joinpath("dest")
SRC = RESOURCES.joinpath("src")
SORT = RESOURCES.joinpath("sort")

TEST_CONFIG = RESOURCES.joinpath("config.toml")

IMPORTANT_DIRS = [RESOURCES, SORT, SRC]


def setup_tests():
    settings.update_settings(TEST_CONFIG)

    for dir in IMPORTANT_DIRS:
        dir.mkdir(parents=True, exist_ok=True)


setup_tests()


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

    for dir in DEST.glob("*/"):
        shutil.rmtree(dir)


@pytest.fixture(scope="session")  #! This is dumb, remove this
def temp_dir():
    temp_dir = RESOURCES.joinpath(".temp")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def test_files():
    files = []
    letters = string.ascii_lowercase
    for x in range(5):
        result_str = "".join(random.choice(letters) for i in range(1000))
        file = SORT.joinpath(f"file_{x}.txt")

        with open(file, "w") as f:
            f.write(result_str)

        files.append(file)
        sleep(0.1)

    yield files
    shutil.rmtree(SORT)


@pytest.fixture(scope="session")
def file_with_content():
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(1000))

    file = SRC.joinpath("temp_file.txt")

    with open(file, "w") as f:
        f.write(result_str)

    yield file
    shutil.rmtree(SRC)
