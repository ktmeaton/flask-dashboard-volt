# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, request
from flask_login import login_required

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


# Custom routes


@blueprint.route("/database", methods=["GET", "POST"])
@login_required
def route_database_enter():
    workflow_form = WorkflowForm(request.form)
    if request.method == "POST" and workflow_form.validate():
        return render_template(
            "workflow-view.html",
            msg="Workflow created.",
            success=True,
            form=workflow_form,
        )
    else:
        return render_template("database-enter.html", form=workflow_form)


@blueprint.route("/workflow", methods=["GET", "POST"])
@login_required
def route_workflow_view():
    if request.method == "POST":
        print(request.form)
    # Setup the workflow database entry
    # flash(
    #    "New workflow added for "
    #    + "<br>System: {0}".format(workflow_form.system.data)
    #    + "<br>Node: {0}".format(workflow_form.node.data)
    #    + "<br>Jobs: {0}".format(workflow_form.total_jobs.data)
    # )
    new_workflow = Workflow()
    # Check if workflow already in database
    check_workflow = (
        db.session.query(Workflow)
        .filter(Workflow.system == new_workflow.system)
        .filter(Workflow.node == new_workflow.node)
        .filter(Workflow.total_jobs == new_workflow.total_jobs)
        .filter(Workflow.username == new_workflow.username)
        .first()
    )
    # Add workflow to database if it can't be found
    if not check_workflow:
        db.session.add(new_workflow)
        db.session.commit()
    # Otherwise update workflow jobs in database
    else:
        check_workflow.status = new_workflow.status
        check_workflow.progress = new_workflow.progress
        check_workflow.completed_jobs = new_workflow.completed_jobs
        check_workflow.running_jobs = new_workflow.running_jobs
        check_workflow.failed_jobs = new_workflow.failed_jobs
        check_workflow.end_date = new_workflow.end_date

    data = Workflow.query.all()
    data.reverse()
    return render_template("workflow-view.html", workflow_data=data)

    # cursor.execute("select * from table_name")
    # data = cursor.fetchall() #data from database
    # return render_template("example.html", value=data)
