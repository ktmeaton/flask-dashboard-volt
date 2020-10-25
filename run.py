# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sys import exit
from app import db, create_app
import config as local_config
from decouple import config
import os
from app.home.models import Workflow
from app.base.models import User


# Load current configuration
FLASK_ENV = config("FLASK_ENV", default="development")
if FLASK_ENV == "development":
    app_config = local_config.DevelopmentConfig
elif FLASK_ENV == "staging":
    app_config = local_config.StagingConfig
elif FLASK_ENV == "production":
    app_config = local_config.ProductionConfig
else:
    exit(
        "Error: Invalid <config_mode>. "
        + "Expected values [production, staging, development] "
    )

# Run the creat config in __init__.py
app = create_app(app_config)

# Flask shell session
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Workflow": Workflow}


if __name__ == "__main__":
    app.run()
