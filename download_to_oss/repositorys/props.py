# -*- coding:utf-8 -*-

from flask import request, g
from flask import jsonify
import functools
import traceback
from webargs.flaskparser import FlaskParser

parser = FlaskParser()


class ValidateException(Exception):
    pass


@parser.error_handler
def handle_error(error, req, schema):
    raise ValidateException(error.messages)


def panic(schema=None):
    """异常"""
    def outter(func):
        if schema:
            @parser.use_args(schema)
            def run_func(*args, **kwargs):
                return func(*args, **kwargs)
        else:
            run_func = func

        @functools.wraps(func)
        def warpper(*args, **kwargs):
            try:
                return run_func(*args, **kwargs)
            except ValidateException as e:
                return error(reason="{}".format(e))
            except Exception as e:
                traceback.print_exc()
                return error(reason="{}".format(e))
        return warpper
    return outter


def success(data: dict = None):
    s = {
        "status": "ok"
    }
    if data:
        s.update(data)
    return jsonify(s)


def error(data: dict = None, reason: str = None):
    s = {
        "status": "error",
        "reason": reason
    }
    if data:
        s.update(data)
    return jsonify(s)
