# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

# Workflows


class WorkflowForm(FlaskForm):
    system = StringField("System", validators=[DataRequired()])
    node = StringField("Node", validators=[DataRequired()])
    jobs = IntegerField("Jobs", validators=[DataRequired()])
    submit = SubmitField("Submit")


class TestForm(FlaskForm):
    test = StringField("Test", validators=[DataRequired()])
    submit = SubmitField("Submit")
