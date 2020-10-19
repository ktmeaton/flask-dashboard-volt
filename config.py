# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from decouple import config


class Config(object):

    # Set up the App SECRET_KEY
    SECRET_KEY = config("SECRET_KEY")
    SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT")

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security settings
    CSRF_ENABLED = True
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
