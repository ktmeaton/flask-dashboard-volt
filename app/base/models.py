# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.home.models import Workflow  # noqa, flake8 issue
from hashlib import md5

# import datetime


class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    password_hash = Column(String(128))
    remember_me = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)
    avatar = Column(String(128))

    # Relationships
    workflows = relationship("Workflow", backref="user", lazy="dynamic")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == "password":
                self.set_password(value)

            setattr(self, property, value)

        self.set_avatar()

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_avatar(self, size=128):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        avatar_url = "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )
        self.avatar = avatar_url


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    return user if user else None
