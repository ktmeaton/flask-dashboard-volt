# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from jinja2 import TemplateNotFound

from app.home.forms import WorkflowForm
from app import db  # Database
from app.home.models import Workflow  # Database model

# from app.base.models import User
from app.home.dashboard_data import DashboardData

import locale

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


@blueprint.route("/index")
@login_required
def index():
    dash_data = DashboardData(current_user)
    return render_template(
        "index.html",
        segment="index",
        last_month_jobs=locale.format("%d", dash_data.last_month_jobs, grouping=True),
        tracked_jobs_fmt=dash_data.tracked_jobs_fmt,
        workflow_date_range=dash_data.workflow_date_range,
        month_delta=dash_data.month_delta,
        system_share_values=list(dash_data.system_share.values()),
        system_share_keys=list(dash_data.system_share.keys()),
    )


@blueprint.route("/<template>")
@login_required
def route_template(template):
    try:

        if not template.endswith(".html"):
            template += ".html"

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)

    except TemplateNotFound:
        return render_template("page-404.html"), 404

    except Exception:
        return render_template("page-500.html"), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except Exception:
        return None


# -----------------------------------------------------------------------------#
# Database
# -----------------------------------------------------------------------------#
# Enter
@blueprint.route("/database", methods=["GET", "POST"])
@login_required
def database():
    workflow_form = WorkflowForm(request.form)
    # -------------------------------------------------------------------------#
    # POST Request - Valid
    if workflow_form.validate_on_submit():
        new_workflow = Workflow(**request.form, user=current_user)

        check_workflow = (
            Workflow.query.filter(Workflow.node == new_workflow.node)
            .filter(Workflow.total_jobs == new_workflow.total_jobs)
            .filter(Workflow.user == new_workflow.user)
            .all()
        )

        # Add workflow to database if it can't be found
        if len(check_workflow) == 1:
            db.session.add(new_workflow)
            flash(
                "New workflow added for "
                + "<br>System: {0}".format(new_workflow.system)
                + "<br>Node: {0}".format(new_workflow.node)
                + "<br>Jobs: {0}".format(new_workflow.total_jobs),
                "info",
            )
        # Otherwise update workflow jobs in database
        else:
            (
                Workflow.query.filter_by(id=check_workflow[0].id).update(
                    dict(
                        completed_jobs=new_workflow.completed_jobs,
                        running_jobs=new_workflow.running_jobs,
                        failed_jobs=new_workflow.failed_jobs,
                        end_date=new_workflow.end_date,
                        progress=new_workflow.progress,
                        status=new_workflow.status,
                    )
                )
            )
            flash(
                "Updated workflow for "
                + "<br>System: {0}".format(new_workflow.system)
                + "<br>Node: {0}".format(new_workflow.node)
                + "<br>Jobs: {0}".format(new_workflow.total_jobs),
                "info",
            )
            # For some reason, new_workflow gets automatically added. Delete for now.
            db.session.delete(new_workflow)
            # recent_id = max(db.session.query(Workflow.id).all())[0]
            # Workflow.query.filter(Workflow.id == recent_id).delete()

        db.session.commit()
        return redirect(url_for("home_blueprint.workflows"))

    else:
        return render_template("database-enter.html", form=workflow_form)


@blueprint.route("/workflows", methods=["GET", "POST"])
@login_required
def workflows():
    data = current_user.workflows.all()
    data.reverse()
    return render_template("workflow-view.html", workflow_data=data)
