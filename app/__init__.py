# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import schema
from importlib import import_module
from flask_mail import Mail

from flask_wtf.csrf import CSRFProtect  # Form security
from flask_bootstrap import Bootstrap  # Bootstrap WTF Forms
from flask_jwt_extended import JWTManager  # Web tokens


# Naming Convention for SQLite rendering in batch
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=schema.MetaData(naming_convention=naming_convention))
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
jwt = JWTManager()
migrate = Migrate()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ("base", "home", "api"):
        module = import_module("app.{}.routes".format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__, static_folder="base/static")
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    with app.app_context():
        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)

    Bootstrap(app)
    return app
