# -*- coding:utf-8 -*-

from flask import Flask
from .config import Config

app = Flask(__name__)

# config
app.config.from_object(Config)

# app router
with app.app_context():
    from .views import downloader
    app.register_blueprint(downloader, url_prefix="/v1")
