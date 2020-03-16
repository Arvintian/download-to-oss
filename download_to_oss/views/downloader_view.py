# -*- coding:utf-8 -*-

from flask import Blueprint, request, current_app
from ..repositorys.props import success, error, panic
from ..types.downloader_schema import OssSchema
import requests
from requests import Response
import oss2
from pretty_logging import pretty_logger
import traceback

downloader = Blueprint("downloader", __name__)


@downloader.route("/oss", methods=["POST"])
@panic(OssSchema)
def to_oss(args):
    return success()


def _download_to_oss(name, url):
    try:
        config = current_app.config
        upload_dir = config.get("OSS_DIR")
        if upload_dir.endswith("/"):
            upload_dir = upload_dir.rstrip("/")
        filename = "{}/{}".format(upload_dir, name)
        bucket = oss2.Bucket(oss2.Auth(config.get("OSS_ACCESS_KEY_ID"), config.get("OSS_ACCESS_KEY_SECRET")),
                             config.get("OSS_ENDPOINT"), config.get("OSS_BUCKET"))
        bucket.put_object(filename, _download(url).raw)
        file_url = bucket.sign_url('GET', filename, current_app.config["OSS_URL_EXPIRE"])
        ding("下载完成", "{}\n{}".format(name, file_url))
    except Exception as e:
        ding("下载失败", name)


def _download(url) -> Response:
    return requests.get(url, stream=True)


def ding(title, text):
    config = current_app.config
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
