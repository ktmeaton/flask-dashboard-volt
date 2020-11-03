# from app.base.models import User
from app.home.models import Workflow
import datetime
import math


class DashboardData:

    tracked_jobs = 0
    tracked_jobs_fmt = ""
    username = ""
    workflow_first = None
    workflow_last = None
    workflow_date_range = None
    month_delta = ""
    system_share = {}
    daily_jobs = {}
    month_jobs = {}
    monthly_delta = 0
    last_month_jobs = 0

    def __init__(self, user):
        self.get_tracked_jobs(user)
        self.get_username(user)
        self.get_workflow_date_range(user)
        self.get_system_share(user)
        self.get_daily_jobs(user)
        self.get_monthly_jobs(user)
        self.get_monthly_delta()

    def get_tracked_jobs(self, user):
        # Count workflows, and get date range
        self.tracked_jobs = 0
        for workflow in user.workflows.all():
            self.tracked_jobs += workflow.total_jobs

        if self.tracked_jobs >= 10000:
            self.tracked_jobs_fmt = str(int(self.tracked_jobs / 1000)) + "k"
        elif self.tracked_jobs >= 1000000:
            self.tracked_jobs_fmt = str(int(self.tracked_jobs / 1000000)) + "M"
        else:
            self.tracked_jobs_fmt = str(self.tracked_jobs)

    def get_username(self, user):
        self.username = user.username
        return self.username

    def get_workflow_date_range(self, user):
        if len(user.workflows.all()) > 0:
            self.workflow_first = user.workflows.order_by(Workflow.id).first()
            self.workflow_last = user.workflows.order_by(Workflow.id.desc()).first()
            self.workflow_date_range = "{} - {}".format(
                self.workflow_first.start_date.strftime("%b %d %Y"),
                self.workflow_last.start_date.strftime("%b %d %Y"),
            )

    def get_system_share(self, user):
        self.system_share = {}
        for workflow in user.workflows.all():
            if workflow.system not in self.system_share:
                self.system_share[workflow.system] = 0
            self.system_share[workflow.system] += workflow.total_jobs
        # Convert from jobs to percent
        self.system_share = {
            k: int((v / self.tracked_jobs) * 100) for k, v in self.system_share.items()
        }

    def get_daily_jobs(self, user):
        self.daily_jobs = {}
        # jobs for today are from the beginning of the day until now
        cur = datetime.datetime.utcnow()
        prev = cur.replace(hour=0, minute=0, second=0, microsecond=0)
        workflows = user.workflows.all()
        for _i in range(1, 7):
            self.daily_jobs[prev] = 0
            for workflow in workflows:
                if workflow.start_date >= prev and workflow.start_date < cur:
                    self.daily_jobs[prev] += workflow.total_jobs
            cur = prev
            prev = prev - datetime.timedelta(days=1)
        self.daily_jobs = {k.strftime("%b %d"): v for k, v in self.daily_jobs.items()}

    def get_monthly_jobs(self, user):
        self.monthly_jobs = {}
        # jobs for this month are from the beginning of the month
        # Add 1 day to the current time
        cur = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        prev = cur.replace(day=1, hour=0, minute=0, microsecond=0)
        workflows = user.workflows.all()
        for _i in range(1, 13):
            self.monthly_jobs[prev] = 0
            for workflow in workflows:
                if workflow.start_date >= prev and workflow.start_date < cur:
                    self.monthly_jobs[prev] += workflow.total_jobs
            cur = prev
            prev = prev.replace(
                month=prev.month - 1 if prev.month > 1 else 12,
                year=prev.year if prev.month > 1 else prev.year - 1,
            )
        self.monthly_jobs = {
            k.strftime("%b %Y"): v for k, v in self.monthly_jobs.items()
        }

    def get_monthly_delta(self):
        cur_month = datetime.datetime.utcnow()
        cur_month_str = cur_month.strftime("%b %Y")
        prev_month = cur_month.replace(
            month=cur_month.month - 1 if cur_month.month > 1 else 12
        )
        prev_month_str = prev_month.strftime("%b %Y")
        self.last_month_jobs = self.monthly_jobs[prev_month_str]
        try:
            self.month_delta = math.ceil(
                (self.monthly_jobs[cur_month_str] / self.monthly_jobs[prev_month_str])
                * 100
            )

        except ZeroDivisionError:
            self.month_delta = "Inf"

        self.month_delta = "{}".format(self.month_delta)

    def __repr__(self):
        return "<DashboardData username: {}; tracked_jobs: {}>".format(
            self.username, self.tracked_jobs
        )
