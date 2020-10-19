# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User

from app.base.util import verify_pass
from app.base.token import generate_confirmation_token, confirm_token
from app.base.email import send_email

import datetime  # confirmed_on

from smtplib import SMTPAuthenticationError


@blueprint.route("/")
def route_default():
    return redirect(url_for("base_blueprint.login"))


# -----------------------------------------------------------------------------#
# Account
# -----------------------------------------------------------------------------#


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    if "login" in request.form:

        # read form data
        username = request.form["username"]
        password = request.form["password"]

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        # User and pass ok, but not confirmed
        if user and verify_pass(password, user.password) and not user.confirmed:
            flash("User has not confirmed by email.")
            return render_template(
                "accounts/login.html",
                msg="User has not confirmed by email.",
                form=login_form,
            )

        # User or pass not ok
        elif not user or not verify_pass(password, user.password):
            flash("Wrong user or password.")
            return render_template(
                "accounts/login.html",
                msg="Wrong username or password.",
                form=login_form,
            )

        # User and pass ok
        elif user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for("home_blueprint.index"))

        # Unhandled
        else:
            flash("Unknown error.")
            return render_template(
                "accounts/login.html", msg="Unknown error.", form=login_form
            )

    if not current_user.is_authenticated:
        return render_template("accounts/login.html", form=login_form)

    # Otherwise send them home
    return redirect(url_for("home_blueprint.index"))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    # login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if "register" in request.form:

        username = request.form["username"]
        email = request.form["email"]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already registered")
            return render_template(
                "accounts/register.html",
                msg="Username already registered",
                success=False,
                form=create_account_form,
            )

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered")
            return render_template(
                "accounts/register.html",
                msg="Email already registered",
                success=False,
                form=create_account_form,
            )

        # else we can create the user
        user = User(**request.form)
        user.registered_on = datetime.datetime.now()

        # Send an activation email
        token = generate_confirmation_token(user.email)
        confirm_url = url_for(
            "base_blueprint.confirm_email", token=token, _external=True
        )
        html = render_template("accounts/activate.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        try:
            send_email(user.email, subject, html)
        except SMTPAuthenticationError:
            flash(
                "Server-side authentication eror. "
                + "Was mail properly configured for this app?"
            )
            return redirect(url_for("base_blueprint.login"))

        db.session.add(user)
        db.session.commit()

        flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for("base_blueprint.route_default"))

    else:
        return render_template("accounts/register.html", form=create_account_form)


@blueprint.route("/confirm/<token>")
# @login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except Exception:
        flash("The confirmation link is invalid or has expired.", "danger")
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed.", "success")
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    return redirect(url_for("base_blueprint.login"))


# -----------------------------------------------------------------------------#
# Logout
# -----------------------------------------------------------------------------#


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("base_blueprint.login"))


@blueprint.route("/shutdown")
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return "Server shutting down..."


# -----------------------------------------------------------------------------#
# Errors
# -----------------------------------------------------------------------------#


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("errors/page-403.html"), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template("errors/page-403.html"), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template("errors/page-404.html"), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template("errors/page-500.html"), 500
