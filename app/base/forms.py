# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError
from wtforms.widgets import PasswordInput
from app.base.models import User


class LoginForm(FlaskForm):
    username = TextField(
        "Username", validators=[DataRequired(message="Please enter a username.")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Please enter a password.")]
    )
    remember_me = BooleanField("Remember Me")


class CreateAccountForm(FlaskForm):
    username = TextField("Username", validators=[DataRequired()])
    email = TextField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="This field is required.")],
        widget=PasswordInput(hide_value=True),
    )
    password2 = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(message="Please enter your password twice."),
            EqualTo("password", message="Passwords do not match."),
        ],
        widget=PasswordInput(hide_value=True),
    )
    agree_terms = BooleanField(
        "Agree Terms",
        validators=[DataRequired(message="Please agree to the terms of service.")],
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if "@" not in email.data:
            raise ValidationError("Please include an '@' in the email.")
        if user is not None:
            raise ValidationError("Please use a different email.")
