# from app.base.models import User
from app.home.models import Workflow
import datetime

dashboard_data = {"tracked_jobs": ""}


class DashboardData:

    tracked_jobs = 0
    tracked_jobs_fmt = ""
    last_month_jobs = 0
    last_two_month_jobs = 0
    username = ""
    workflow_first = None
    workflow_last = None
    workflow_date_range = None
    month_delta = ""
    system_share = {}

    def __init__(self, user):
        self.get_tracked_jobs(user)
        self.get_username(user)
        self.get_workflow_dates(user)
        self.get_workflows_last_month(user)
        self.get_system_share(user)

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

    def get_workflow_dates(self, user):
        if len(user.workflows.all()) > 0:
            self.workflow_first = user.workflows.order_by(Workflow.id).first()
            self.workflow_last = user.workflows.order_by(Workflow.id.desc()).first()
            self.workflow_date_range = "{} - {}".format(
                self.workflow_first.start_date.strftime("%b %d %Y"),
                self.workflow_last.start_date.strftime("%b %d %Y"),
            )

    def get_workflows_last_month(self, user):
        self.last_month_jobs = 0
        self.last_two_month_jobs = 0
        now = datetime.datetime.utcnow()
        last_month = now - datetime.timedelta(days=30)
        last_two_month = last_month - datetime.timedelta(days=30)
        for workflow in user.workflows.all():
            if workflow.start_date >= last_month and workflow.start_date <= now:
                self.last_month_jobs += workflow.total_jobs
            if (
                workflow.start_date >= last_two_month
                and workflow.start_date <= last_month
            ):
                self.last_two_month_jobs += workflow.total_jobs
        try:
            self.month_delta = int(
                (self.last_month_jobs / self.last_two_month_jobs) * 100
            )
        except ZeroDivisionError:
            self.month_delta = "Inf"
        self.month_delta = "{}".format(self.month_delta)

    def get_system_share(self, user):
        for workflow in user.workflows.all():
            if workflow.system not in self.system_share:
                self.system_share[workflow.system] = 0
            self.system_share[workflow.system] += workflow.total_jobs

    def __repr__(self):
        return "<DashboardData username: {}; tracked_jobs: {}>".format(
            self.username, self.tracked_jobs
        )
