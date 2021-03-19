import shutil
from pathlib import Path

import pytest
from quick_zip.schema.backup_job import BackupJob

CWD = Path(__file__).parent
RESOURCES = CWD.joinpath("resources")
DEST = RESOURCES.joinpath("dest")


@pytest.fixture
def job_store():
    return BackupJob(
        name="Test Job", source=RESOURCES.joinpath("src"), destination=DEST
    )


@pytest.fixture
def config_with_vars():
    return RESOURCES.joinpath("config-vars.json")


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
