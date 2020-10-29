# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, InputRequired

# Workflows


class WorkflowForm(FlaskForm):
    node = StringField(
        "Node", validators=[DataRequired(message="Please enter the node.")]
    )
    total_jobs = IntegerField(
        "Total Jobs", validators=[DataRequired(message="Please enter the total jobs.")]
    )
    completed_jobs = IntegerField(
        "Completed Jobs",
        validators=[InputRequired(message="Please enter the completed jobs.")],
    )
    running_jobs = IntegerField(
        "Running Jobs",
        validators=[InputRequired(message="Please enter the running jobs.")],
    )
    failed_jobs = IntegerField(
        "Failed Jobs",
        validators=[InputRequired(message="Please enter the failed jobs.")],
    )
