# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, DataRequired

## Workflows

class WorkflowForm(FlaskForm):
    system = StringField( 'System' , validators=[DataRequired()])
    node  = StringField(  'Node'   , validators=[DataRequired()])
    jobs  = StringField(  'Jobs'   , validators=[DataRequired()])
    #jobs = IntegerField('Jobs'   , validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReusableForm(FlaskForm):
    name = TextField('Name:', validators=[DataRequired()])
