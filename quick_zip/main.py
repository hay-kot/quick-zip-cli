from core.config import CONFIG_FILE, config
from schema.backup_job import BackupJob
from utils.custom_logger import logger


def pre_work():
    logger.info("-------- START UP --------")

    pass


def clean_up():
    logger.info("-------- FINISHED --------")

    pass


def main():
    pre_work()
    all_jobs = BackupJob.get_job_store(CONFIG_FILE)

    clean_up()


if __name__ == "__main__":
    main()
