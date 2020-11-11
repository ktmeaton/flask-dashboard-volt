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


class TokenAPI(Resource):
    @basic_auth.login_required
    def get(self):
        token = basic_auth.current_user().get_token()
        db.session.commit()
        return {"token": token}, 200

    @token_auth.login_required
    def delete(self):
        token_auth.current_user().revoke_token()
        db.session.commit()
        return "", 204


api.add_resource(TokenAPI, "/tokens", endpoint="tokens")

# -----------------------------------------------------------------------------#
# Workflows
# -----------------------------------------------------------------------------#


class WorkflowAPI(Resource):
    decorators = [token_auth.login_required]

    def __init__(self):
        # These are the implemented possible args
        args_implement = {
            "id": int,
            "system": str,
            "node": str,
            "total_jobs": int,
            "completed_jobs": int,
            "running_jobs": int,
            "failed_jobs": int,
        }

        # Parse args from request
        self.reqparse = reqparse.RequestParser()

        for arg_name, arg_type in args_implement.items():
            self.reqparse.add_argument(
                arg_name,
                type=arg_type,
                required=False,
                store_missing=False,
                help="No workflow {} provided.".format(arg_name),
            )

        super(WorkflowAPI, self).__init__()

    def get(self):
        """
        GET a workflow by attribute(s).
        curl -H "Authorization: Bearer $TOKEN
        http://localhost:5000/api/workflows?node=cedar5
        """

        # Get the user based on the provided token
        user = token_auth.current_user()

        # Parse the request args setup in init
        self.reqargs = self.reqparse.parse_args()

        # Query by supplied attributes
        check_workflow = (
            Workflow.query.filter_by(**self.reqargs).filter(Workflow.user == user).all()
        )

        # Construct a dictionary with key=workflow id value=workflow
        workflow_dict = {workflow.id: workflow.to_dict() for workflow in check_workflow}

        # Return the workflow dict as json
        return {"workflows": workflow_dict}, 200

    def post(self):
        """
        POST a new workflow into the database.
        """
        # These are the required args to create a workflow
        args_required = {
            "node": str,
            "total_jobs": int,
            "completed_jobs": int,
            "running_jobs": int,
            "failed_jobs": int,
        }
        # Parse the request args
        for arg_name, arg_type in args_required.items():
            self.reqparse.add_argument(
                arg_name,
                type=arg_type,
                required=True,
                help="No workflow {} provided.".format(arg_name),
            )
        # Parse the request args setup in init and here
        self.reqargs = self.reqparse.parse_args()

        # Get the user based on the provided token
        user = token_auth.current_user()

        # Check if the workflow exists or if hasn't completed
        check_workflow = (
            Workflow.query.filter(Workflow.node == self.reqargs["node"])
            .filter(Workflow.total_jobs == self.reqargs["total_jobs"])
            .filter(Workflow.user == user)
            .filter(Workflow.status != "Completed")
            .filter(Workflow.status != "Failed")
            .first()
        )

        # If an existing workflow was found, can't post
        if check_workflow:
            return {"message": "POST request failure, existing workflow found."}, 400

        # Create a new workflow to take advantage of model logic
        data = self.reqargs
        Workflow(user=user, **data)
        # Commit new workflow
        db.session.commit()
        return {"message": "POST request success, workflow added."}, 200

    def put(self):
        """
        PUT new workflow attributes into an existing workflow.
        """
        # These are the required args to update a workflow
        args_required = {
            "node": str,
            "total_jobs": int,
            "completed_jobs": int,
            "running_jobs": int,
            "failed_jobs": int,
        }
        # Parse the request args
        for arg_name, arg_type in args_required.items():
            self.reqparse.add_argument(
                arg_name,
                type=arg_type,
                required=True,
                help="No workflow {} provided.".format(arg_name),
            )
        # Parse the request args setup in init and here
        self.reqargs = self.reqparse.parse_args()

        # Get the user based on the provided token
        user = token_auth.current_user()

        # Check the workflow exists
        check_workflow = (
            Workflow.query.filter(Workflow.node == self.reqargs["node"])
            .filter(Workflow.total_jobs == self.reqargs["total_jobs"])
            .filter(Workflow.user == user)
            .filter(Workflow.status == "Running")
            .order_by(Workflow.id.desc())
            .first()
        )
        # If no workflow was found, return 400 status code
        if not check_workflow:
            return {"message": "PUT request failed, no workflow found."}, 400

        # Update the workflow attributes
        data = {"data": self.reqargs}
        check_workflow.update_attr(**data)
        # Commit update to database
        db.session.commit()

        return {"message": "PUT request success, workflow updated."}, 201


api.add_resource(WorkflowAPI, "/workflows", endpoint="workflows")
