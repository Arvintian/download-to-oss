# -*- coding:utf-8 -*-

from flask import Blueprint, request, current_app
from ..repositorys.props import success, error, panic
from ..types.downloader_schema import OssSchema
import requests
from requests import Response
import oss2
from pretty_logging import pretty_logger
import traceback
from multiprocessing.dummy import Pool as ThreadPool
import uuid
import os

downloader = Blueprint("downloader", __name__)
thread_pool = ThreadPool()
config = current_app.config


@downloader.route("/oss", methods=["POST"])
@panic(OssSchema)
def to_oss(args):
    name = args.get("name")
    url = args.get("url")
    thread_pool.apply_async(_download_to_oss, (name, url))
    return success()


def _download_to_oss(name, url):
    local_file = "/tmp/{}".format(str(uuid.uuid1()))
    try:
        pretty_logger.info("downloading {} {}".format(name, url))
        upload_dir = config.get("OSS_DIR")
        if upload_dir.endswith("/"):
            upload_dir = upload_dir.rstrip("/")
        file_key = "{}/{}".format(upload_dir, name)
        bucket = oss2.Bucket(oss2.Auth(config.get("OSS_ACCESS_KEY_ID"), config.get("OSS_ACCESS_KEY_SECRET")),
                             config.get("OSS_ENDPOINT"), config.get("OSS_BUCKET"))
        with _download(url) as rsp:
            with open(local_file, "wb") as fd:
                for chunk in rsp.iter_content(chunk_size=2048):
                    fd.write(chunk)
        bucket.put_object_from_file(file_key, local_file)
        file_url = bucket.sign_url('GET', file_key, config.get("OSS_URL_EXPIRE"))
        ding("下载完成", "{}\n{}".format(name, file_url))
    except Exception as e:
        pretty_logger.error(traceback.format_exc())
        ding("下载失败", name)
    finally:
        os.remove(local_file)


def _download(url) -> Response:
    return requests.get(url, stream=True)


def ding(title, text):
    try:
        payload = {
            "msgtype": "text",
            "text": {
                "content": "{}\n{}\n{}".format(config.get("DINGTALK_KEYWORD"), title, text)
            }
        }
        requests.post(config.get("DINGTALK_WEBHOOK"), json=payload, timeout=5)
    except Exception as e:
        pretty_logger.error(traceback.format_exc())
