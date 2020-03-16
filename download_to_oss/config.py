# -*- coding:utf-8 -*-
from .helpers import env


class Config(object):
    DEBUG = env("DEBUG", cast=bool)
    OSS_ACCESS_KEY_ID = env("OSS_ACCESS_KEY_ID", cast=str)
    OSS_ACCESS_KEY_SECRET = env("OSS_ACCESS_KEY_SECRET", cast=str)
    OSS_ENDPOINT = env("OSS_BUCKET", cast=str)
    OSS_DIR = env("OSS_DIR", cast=str)
    OSS_URL_EXPIRE = env("OSS_URL_EXPIRE", cast=str)
    DINGTALK_WEBHOOK = env("DINGTALK_WEBHOOK", cast=str)
    DINGTALK_KEYWORD = env("DINGTALK_KEYWORD", cast=str)
