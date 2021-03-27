import json
from typing import List

import requests
from quick_zip.schema.backup_job import BackupResults


def create_post_data(body: List[BackupResults]):
    dictionary = {x.name: x.dict() for x in body}
    return json.dumps(dictionary, default=str)


def post_file_data(url, body: List[BackupResults]):
    body = create_post_data(body)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    requests.post(url, json=body, headers=headers, timeout=5, verify=False)
