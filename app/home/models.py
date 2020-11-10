# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from app import db
import datetime
from app.home.systems import system_map


class Workflow(db.Model):

    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True)
    node = Column(String(64), unique=False, default="N/A")
    total_jobs = Column(Integer, unique=False, default=0)
    completed_jobs = Column(Integer, unique=False, default=0, nullable=True)
    running_jobs = Column(Integer, unique=False, default=0, nullable=True)
    failed_jobs = Column(Integer, unique=False, default=0, nullable=True)
    start_date = Column(
        DateTime, unique=False, index=True, default=datetime.datetime.utcnow
    )
    end_date = Column(DateTime, unique=False, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    # Inferred attributes
    status = Column(String(64), unique=False, default="N/A")
    progress = Column(Integer, unique=False, default=0)
    system = Column(String(64), unique=False, default="NA")

    # Relationships
    # username will be a backref from model User

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if (
                hasattr(value, "__iter__")
                and not isinstance(value, str)
                and property != "user"
            ):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

        # Inferred attributes
        for system in system_map:
            for node in system_map[system]:
                if node in self.node:
                    self.system = system

        self.progress = int(int(self.completed_jobs) / int(self.total_jobs) * 100)
        self.status = (
            "Failed"
            if int(self.failed_jobs) > 0
            else ("Completed" if int(self.progress) == 100 else "Running")
        )
        if self.progress == 100 or self.status == "Failed":
            self.end_date = datetime.datetime.utcnow()
        else:
            self.end_date = None

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        data = {
            "id": self.id,
            "system": self.system,
            "node": self.node,
            "status": self.status,
            "progress": self.progress,
            "total_jobs": self.total_jobs,
            "completed_jobs": self.completed_jobs,
            "running_jobs": self.running_jobs,
            "failed_jobs": self.failed_jobs,
            "start_date": self.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": self.end_date.strftime("%Y-%m-%d %H:%M:%S")
            if self.end_date
            else self.end_date,
        }
        return data

    def end(self):
        self.end_date = datetime.datetime.utcnow
        return self.end_date
