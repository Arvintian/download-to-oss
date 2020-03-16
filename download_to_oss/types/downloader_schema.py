# coding:utf-8

from marshmallow import Schema, fields


class OssSchema(Schema):
    name = fields.Str(required=True)
    url = fields.Str(required=True)

    class Meta:
        strict = True
