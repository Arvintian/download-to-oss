# -*- coding:utf-8 -*-
import os


def _bool(var, default):
    v: str = os.getenv(var)
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    if v.lower() == "true":
        return True
    return False


def _int(var, default):
    v: str = os.getenv(var)
    if v is None:
        return default
    if isinstance(v, int):
        return v
    return int(v)


def _float(var, default):
    v: str = os.getenv(var)
    if v is None:
        return default
    if isinstance(v, float):
        return v
    return float(v)


def _string(var, default):
    v: default = os.getenv(var)
    if v is None:
        return default
    if isinstance(v, str):
        return v
    return str(v)


def _notype(var, default):
    return os.getenv(var, default=default)


def env(var, cast=None, default=None):
    if cast is bool:
        return _bool(var, default)
    elif cast is int:
        return _int(var, default)
    elif cast is float:
        return _float(var, default)
    elif cast is str:
        return _string(var, default)
    else:
        return _notype(var, default)
