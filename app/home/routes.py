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


@blueprint.route("/index")
@login_required
def index():
    return render_template("index.html", segment="index")


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
    # Need to do user auth here when posting
    workflow_form = WorkflowForm(request.form)
    # -------------------------------------------------------------------------#
    # POST Request - Valid
    if workflow_form.validate_on_submit():
        new_workflow = Workflow(**request.form)

        check_workflow = (
            db.session.query(Workflow)
            .filter(Workflow.system == new_workflow.system)
            .filter(Workflow.node == new_workflow.node)
            .filter(Workflow.total_jobs == new_workflow.total_jobs)
            # .filter(Workflow.username == new_workflow.username)
            # .filter(Workflow.start_date == new_workflow.start_date)
            .first()
        )
        # Add workflow to database if it can't be found
        if not check_workflow:
            db.session.add(new_workflow)
            db.session.commit()
            flash(
                "New workflow added for "
                + "<br>System: {0}".format(workflow_form.system.data)
                + "<br>Node: {0}".format(workflow_form.node.data)
                + "<br>Jobs: {0}".format(workflow_form.total_jobs.data)
            )
        # Otherwise update workflow jobs in database
        else:
            (
                db.session.query(Workflow)
                .filter_by(id=check_workflow.id)
                .update(
                    dict(
                        status=new_workflow.status,
                        progress=new_workflow.progress,
                        completed_jobs=new_workflow.completed_jobs,
                        running_jobs=new_workflow.running_jobs,
                        failed_jobs=new_workflow.failed_jobs,
                        end_date=new_workflow.end_date,
                    )
                )
            )
            db.session.commit()
            flash(
                "Updated workflow for "
                + "<br>System: {0}".format(workflow_form.system.data)
                + "<br>Node: {0}".format(workflow_form.node.data)
                + "<br>Jobs: {0}".format(workflow_form.total_jobs.data)
            )
        return redirect(url_for("home_blueprint.workflows"))

    else:
        return render_template("database-enter.html", form=workflow_form)


@blueprint.route("/workflows", methods=["GET", "POST"])
@login_required
def workflows():
    data = Workflow.query.filter(Workflow.username == str(current_user)).all()
    data.reverse()
    return render_template("workflow-view.html", workflow_data=data)
