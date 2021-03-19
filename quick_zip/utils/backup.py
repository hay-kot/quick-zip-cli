import errno
import json
import shutil

import requests

from quick_zip.schema.backup_job import PostData


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def post_file_data(url, body: PostData):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    requests.post(url, json=body.json(), headers=headers, timeout=5, verify=False)
