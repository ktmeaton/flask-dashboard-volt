# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from sqlalchemy import Integer, String, Column, Date
from app import db


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
    failed_jobs = Column(Integer, unique=False)
    start_date = Column(Date, unique=False)
    end_date = Column(Date, unique=False, nullable=True)
    username = Column(String, unique=False)

    # def __repr__(self):
    #    return str([self.system, self.node, self.jobs])
