# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import Integer, String, Column
from app import db


class Workflow(db.Model):

    __tablename__ = "Workflow"

    id = Column(Integer, primary_key=True)
    system = Column(String, unique=False)
    node = Column(String, unique=False)
    # jobs = Column(String, unique=False)
    jobs = Column(Integer, unique=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            else:
                value = value

            setattr(self, property, value)

    def __repr__(self):
        return str(self.system)
