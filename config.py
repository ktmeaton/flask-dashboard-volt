# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config("SECRET_KEY", default="S#perS3crEt_007")
    SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT", default="my_precious_two")

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security settings
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Email settings
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ["APP_MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["APP_MAIL_PASSWORD"]

    # mail accounts
    MAIL_DEFAULT_SENDER = "flowdash.bio@gmail.com"


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        config("DB_ENGINE", default="postgresql"),
        config("DB_USERNAME", default="appseed"),
        config("DB_PASS", default="pass"),
        config("DB_HOST", default="localhost"),
        config("DB_PORT", default=5432),
        config("DB_NAME", default="appseed-flask"),
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {"Production": ProductionConfig, "Debug": DebugConfig}
