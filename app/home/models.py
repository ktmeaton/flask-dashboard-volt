# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import Integer, String, Column, Date
from app import db
import datetime


class Workflow(db.Model):

    __tablename__ = "Workflow"

    id = Column(Integer, primary_key=True)
    system = Column(String, unique=False)
    node = Column(String, unique=False)
    status = Column(String, unique=False)
    progress = Column(Integer, unique=False)
    total_jobs = Column(Integer, unique=False)
    completed_jobs = Column(Integer, unique=False)
    running_jobs = Column(Integer, unique=False)
    failed_jobs = Column(Integer, unique=False, nullable=True)
    start_date = Column(Date, unique=False)
    end_date = Column(Date, unique=False, nullable=True)
    username = Column(String, unique=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == "start_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%d")

            if property == "end_date":
                value = datetime.datetime.strptime(value, "%Y-%m-%d")

            setattr(self, property, value)

    def __repr__(self):
        return str([self.system, self.node, self.total_jobs])

    def as_dict(self):
        workflow_dict = {}
        workflow_dict[self.id] = {}
        for attr in vars(self):
            if attr == "_sa_instance_state":
                continue
            val = getattr(self, attr)
            if isinstance(val, datetime.date):
                workflow_dict[self.id][attr] = val.strftime("%Y-%m-%d")
            else:
                workflow_dict[self.id][attr] = getattr(self, attr)
        return workflow_dict
