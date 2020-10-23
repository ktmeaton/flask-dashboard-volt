# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean  # , ForeignKey

# Binary, DateTime
# from sqlalchemy.orm import relationship

from app import db, login_manager

# from app.base.util import hash_pass

# import datetime

# from app.home.models import Workflow


class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    password = Column(String(128))
    remember_me = Column(Boolean, default=False)
    # registered_on = Column(DateTime, nullable=True)
    # admin = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)
    # confirmed_on = Column(DateTime, nullable=True)

    # Relationships
    # workflow_id = Column(Integer, ForeignKey("workflow.id"))
    # workflow = relationship("Workflow")

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            # if property == "password":
            #    value = hash_pass(value)  # we need bytes here (not plain str)
            #

            setattr(self, property, value)

    def __repr__(self):
        return "<User {}>".format(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()
    return user if user else None
