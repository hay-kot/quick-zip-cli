import errno
import json
import shutil
import urllib.request


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def post_file_data(url, body):
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    jsondata = json.dumps(body)
    json_data_as_bytes = jsondata.encode("utf-8")
    req.add_header("Content-Length", len(json_data_as_bytes))

    urllib.request.urlopen(req, json_data_as_bytes)
