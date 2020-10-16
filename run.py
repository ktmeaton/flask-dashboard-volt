# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config

from config import config_dict
from app import create_app, db

from flask_wtf.csrf import CSRFProtect  # Form security
from flask_bootstrap import Bootstrap  # Bootstrap WTF Forms

# from os import environ

# WARNING: Don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True)

csrf = CSRFProtect()

# The configuration
get_config_mode = "Debug" if DEBUG else "Production"

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit("Error: Invalid <config_mode>. Expected values [Debug, Production] ")

app = create_app(app_config)
Bootstrap(app)
Migrate(app, db)
csrf.init_app(app)

if __name__ == "__main__":
    app.run()
