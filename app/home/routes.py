# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, request, flash
from flask_login import login_required

from jinja2 import TemplateNotFound

from app.home.forms import WorkflowForm

# from app.home.models import Workflow
# from app import db


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


@blueprint.route("/database-enter", methods=["GET", "POST"])
def database_enter():
    workflow_form = WorkflowForm(request.form)
    if request.method == "POST" and workflow_form.validate():
        print(dir(workflow_form.system))
        print(workflow_form.system.data)
        flash(
            "New workflow added for "
            + "<br>System: {0}".format(workflow_form.system.data)
            + "<br>Node: {0}".format(workflow_form.node.data)
            + "<br>Jobs: {0}".format(workflow_form.jobs.data)
        )
        return render_template(
            "workflow.html", msg="Workflow created.", success=True, form=workflow_form
        )
    else:
        return render_template("database.html", form=workflow_form)
