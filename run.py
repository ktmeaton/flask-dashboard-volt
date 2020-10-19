# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from app import create_app, db

import os

# Load current configuration
try:
    # Load the configuration using the default values
    app_config = eval(os.environ["APP_SETTINGS"])

except KeyError:
    exit(
        "Error: Invalid <config_mode>. "
        + "Expected values [Production, Staging, Development] "
    )

# Run the creat config in __init__.py
app = create_app(app_config)

# Configure database
Migrate(app, db)

if __name__ == "__main__":
    app.run()
