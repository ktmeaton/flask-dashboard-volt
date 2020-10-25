# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from decouple import config
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Flask App General
    FLASK_APP = config("FLASK_APP", default="run.py")
    FLASK_ENV = config("FLASK_ENV", default="development")
    DEBUG = config("DEBUG", default=True)
    TEMPLATES_AUTO_RELOAD = config("TEMPLATES_AUTO_RELOAD", default=True)

    # Security
    SECRET_KEY = config("SECRET_KEY", default="S3cr3t_K#Key")

    # Mail
    APP_MAIL_USERNAME = config("APP_MAIL_USERNAME", default="myGmailUsername")
    APP_MAIL_PASSWORD = config("APP_MAIL_PASSWORD", default="myGmailPassword")
    MAIL_DEFAULT_SENDER = config(
        "MAIL_DEFAULT_SENDER", default="flowdash.bio@gmail.com"
    )

    # Database Config, default to sqlite
    SQLALCHEMY_DATABASE_URI = config(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(basedir, "flowdash_bio.sqlite3"),
    )
    # Database Config alterate, default to postgres
    # SQLALCHEMY_DATABASE_URI = config(
    # "DATABASE_URL",
    # default=("postgresql://postgres:postgres@localhost:5432/"
    #          + os.path.join(basedir, "flowdash_bio"))
    # )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security settings
    CSRF_ENABLED = True
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # Remove "Bearer from the JWT header"
    # JWT_HEADER_TYPE = None

    # Email settings
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = config("APP_MAIL_USERNAME")
    MAIL_PASSWORD = config("APP_MAIL_PASSWORD")

    # mail accounts
    MAIL_DEFAULT_SENDER = "flowdash.bio@gmail.com"


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
