# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = TextField("Username", id="username_login", validators=[DataRequired()])
    password = PasswordField("Password", id="pwd_login", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me", id="remember-me_login")


class CreateAccountForm(FlaskForm):
    username = TextField("Username", id="username_create", validators=[DataRequired()])
    email = TextField("Email", id="email_create", validators=[DataRequired(), Email()])
    password = PasswordField("Password", id="pwd_create", validators=[DataRequired()])
    agree_terms = BooleanField(
        "Agree Terms", id="agree-terms_create", validators=[DataRequired()]
    )
