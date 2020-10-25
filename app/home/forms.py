# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField  # , Datefield
from wtforms.validators import DataRequired, InputRequired

# Workflows


class WorkflowForm(FlaskForm):
    node = StringField("Node", validators=[DataRequired()])
    total_jobs = IntegerField("Total Jobs", validators=[DataRequired()])
    completed_jobs = IntegerField("Completed Jobs", validators=[InputRequired()])
    running_jobs = IntegerField("Running Jobs", validators=[InputRequired()])
    failed_jobs = IntegerField("Failed Jobs", validators=[InputRequired()])
    submit = SubmitField("Submit")
