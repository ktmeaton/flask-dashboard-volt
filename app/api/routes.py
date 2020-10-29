"""
API Routes
https://github.com/miguelgrinberg/microblog/blob/master/app/api/
"""

# General
from flask import jsonify
from app.api import blueprint
from app.base.models import User
from app import db

# Authentication
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

# Errors
from werkzeug.http import HTTP_STATUS_CODES

# Setup
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

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


@blueprint.route("/tokens", methods=["POST"])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({"token": token})


@blueprint.route("/tokens", methods=["DELETE"])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return "", 204


# -----------------------------------------------------------------------------#
# Users
# -----------------------------------------------------------------------------#


@blueprint.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())
