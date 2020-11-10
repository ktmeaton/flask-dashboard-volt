"""
API Routes
https://github.com/miguelgrinberg/microblog/blob/master/app/api/
"""

# General
from flask import jsonify
from app.api import blueprint
from app.base.models import User
from app.home.models import Workflow
from app import db, csrf

# API
from flask_restful import Api, Resource, reqparse

# Authentication
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

# from flask_login import current_user

# Errors
from werkzeug.http import HTTP_STATUS_CODES

# Setup
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

api = Api(blueprint, decorators=[csrf.exempt])

# -----------------------------------------------------------------------------#
# Authentication
# -----------------------------------------------------------------------------#


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)


# -----------------------------------------------------------------------------#
# Errors
# -----------------------------------------------------------------------------#


def error_response(status_code, message=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)


# -----------------------------------------------------------------------------#
# Tokens
# -----------------------------------------------------------------------------#


# @blueprint.route("/tokens", methods=["POST"])
# @basic_auth.login_required
# def get_token():
#    token = basic_auth.current_user().get_token()
#    db.session.commit()
#    return jsonify({"token": token})


# @blueprint.route("/tokens", methods=["DELETE"])
# @token_auth.login_required
# def revoke_token():
#    token_auth.current_user().revoke_token()
#    db.session.commit()
#    return "", 204


class TokenAPI(Resource):
    @basic_auth.login_required
    def get(self):
        token = basic_auth.current_user().get_token()
        db.session.commit()
        return {"token": token}, 200

    def delete(self):
        pass


api.add_resource(TokenAPI, "/tokens", endpoint="tokens")

# -----------------------------------------------------------------------------#
# Workflows
# -----------------------------------------------------------------------------#


class WorkflowByIDAPI(Resource):
    decorators = [token_auth.login_required]

    def get(self, id):
        """GET a workflow by id."""
        workflow_dict = Workflow.query.get_or_404(id).to_dict()
        return {"workflow": workflow_dict}, 200

    def put(self, id):
        """
        PUT new attributes into an existing workflow by searching for
        username, node, and total_jobs.
        params:
            node (str):
            total_jobs (int):
        """
        pass


class WorkflowByAttrAPI(Resource):
    decorators = [token_auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "system", type=str, required=False, help="No workflow system provided.",
        )
        self.reqparse.add_argument(
            "node", type=str, required=False, help="No workflow node provided."
        )
        self.reqparse.add_argument(
            "total_jobs",
            type=int,
            required=False,
            help="No workflow total_jobs provided.",
        )
        self.reqparse.add_argument(
            "completed_jobs",
            type=int,
            required=False,
            help="No workflow completed_jobs provided.",
        )
        self.reqparse.add_argument(
            "running_jobs",
            type=int,
            required=False,
            help="No workflow running_jobs provided.",
        )
        self.reqparse.add_argument(
            "failed_jobs",
            type=int,
            required=False,
            help="No workflow failed_jobs provided.",
        )
        super(WorkflowByAttrAPI, self).__init__()

    def get(self):
        """
       GET a workflow by attribute(s).
       curl -H "Authorization: Bearer $TOKEN"
         http://localhost:5000/api/workflows/attr?node=cedar5&total_jobs=50
       """
        user = token_auth.current_user()
        self.reqargs = self.reqparse.parse_args()
        filter_attr = {attr: val for attr, val in self.reqargs.items() if val}
        # If no filtered attributes
        if len(filter_attr) == 0:
            return 400
        # Otherwise query by attributes
        check_workflow = (
            Workflow.query.filter_by(**filter_attr).filter(Workflow.user == user).all()
        )
        workflow_dict = {workflow.id: workflow.to_dict() for workflow in check_workflow}
        return {"workflows": workflow_dict}, 200

    def put(self):
        """
        PUT new workflow attributes into an existing workflow.
        curl -H "Authorization: Bearer $TOKEN"
          http://localhost:5000/api/workflows/attr?
          node=cedar5&
          total_jobs=50&
          completed_jobs=40&
          running_jobs=10&
          failed_jobs=0
        """
        user = token_auth.current_user()
        self.reqparse.add_argument(
            "node", type=str, required=True, help="No workflow node provided."
        )
        self.reqparse.add_argument(
            "total_jobs",
            type=int,
            required=True,
            help="No workflow total_jobs provided.",
        )
        self.reqparse.add_argument(
            "completed_jobs",
            type=int,
            required=True,
            help="No workflow completed_jobs provided.",
        )
        self.reqparse.add_argument(
            "running_jobs",
            type=int,
            required=True,
            help="No workflow running_jobs provided.",
        )
        self.reqparse.add_argument(
            "failed_jobs",
            type=int,
            required=True,
            help="No workflow failed_jobs provided.",
        )
        self.reqargs = self.reqparse.parse_args()

        # Check the workflow exists
        check_workflow = (
            Workflow.query.filter(Workflow.node == self.reqargs["node"])
            .filter(Workflow.total_jobs == self.reqargs["total_jobs"])
            .filter(Workflow.user == user)
            .all()
        )
        # If not just one workflow found, return 400
        if len(check_workflow) != 1:
            return 400

        check_workflow = check_workflow[0]

        # Create a new workflow to take advantage of model logic
        new_workflow = Workflow(
            user=user,
            node=check_workflow.node,
            system=check_workflow.system,
            total_jobs=check_workflow.total_jobs,
            completed_jobs=self.reqargs["completed_jobs"],
            running_jobs=self.reqargs["running_jobs"],
            failed_jobs=self.reqargs["failed_jobs"],
            start_date=check_workflow.start_date,
        )
        Workflow.query.filter_by(id=check_workflow.id).update(
            dict(
                completed_jobs=new_workflow.completed_jobs,
                running_jobs=new_workflow.running_jobs,
                failed_jobs=new_workflow.failed_jobs,
                end_date=new_workflow.end_date,
                progress=new_workflow.progress,
                status=new_workflow.status,
            )
        )
        # For some reason, new_workflow gets automatically added. Delete for now.
        db.session.delete(new_workflow)
        # Now add only updates
        db.session.commit()

        return 201


class WorkflowListAPI(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        user = token_auth.current_user()
        print(user)
        try:
            workflows = user.workflows
        except AttributeError:
            return 401
        workflows_dict = {workflow.id: workflow.to_dict() for workflow in workflows}
        return {"workflows": workflows_dict}, 200


api.add_resource(WorkflowByIDAPI, "/workflows/id/<int:id>", endpoint="workflow-id")
api.add_resource(WorkflowByAttrAPI, "/workflows/attr", endpoint="workflow-attr")
api.add_resource(WorkflowListAPI, "/workflows", endpoint="workflows")
