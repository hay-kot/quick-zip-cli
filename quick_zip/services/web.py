import json
from typing import List

import requests
from quick_zip.schema.backup_job import BackupResults, PostData


def create_post_data(body: List[BackupResults]):
    dictionary = {}
    for x in body:
        dictionary.update({x.name: x.dict()})

    return json.dumps(dictionary, default=str)


def post_file_data(url, body: PostData):
    body = create_post_data(body)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    requests.post(url, json=body, headers=headers, timeout=5, verify=False)
