# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from app import db
import datetime


class Workflow(db.Model):

    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True)
    system = Column(String(64), unique=False)
    node = Column(String(64), unique=False)
    status = Column(String(64), unique=False)
    progress = Column(Integer, unique=False)
    total_jobs = Column(Integer, unique=False)
    completed_jobs = Column(Integer, unique=False, nullable=True)
    running_jobs = Column(Integer, unique=False, nullable=True)
    failed_jobs = Column(Integer, unique=False, nullable=True)
    start_date = Column(
        DateTime, unique=False, index=True, default=datetime.datetime.utcnow
    )
    end_date = Column(DateTime, unique=False, nullable=True)
    # username = Column(String(64), index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    # Relationships
    # user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return "<System {}; Node {}; Total Jobs {}>".format(
            self.system, self.node, self.total_jobs
        )

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

    def end(self):
        self.end_date = datetime.datetime.utcnow
