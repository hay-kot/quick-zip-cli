import requests
from quick_zip.schema.backup_job import PostData


def post_file_data(url, body: PostData):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    requests.post(url, json=body.json(), headers=headers, timeout=5, verify=False)
