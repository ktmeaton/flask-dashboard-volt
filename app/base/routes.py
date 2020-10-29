# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user
from app import db  # , login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User
from app.base.token import generate_confirmation_token, confirm_token
from app.base.email import send_email
from werkzeug.urls import url_parse

# import datetime  # confirmed_on

from smtplib import SMTPAuthenticationError

# -----------------------------------------------------------------------------#
# Account
# -----------------------------------------------------------------------------#
# Default path routes to login
@blueprint.route("/")
def route_default():
    return redirect(url_for("base_blueprint.login"))


# Terms of Agreement
@blueprint.route("/terms", methods=["GET"])
def terms():
    return render_template("accounts/terms.html")


# -----------------------------------------------------------------------------#
# Login Page
@blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    # -------------------------------------------------------------------------#
    # POST Request - Valid
    if login_form.validate_on_submit():
        # Search for user in database
        user = User.query.filter_by(username=login_form.username.data).first()

        # Username invalid
        if not user:
            flash("Invalid username or password.", "info")
            return render_template(
                "accounts/login.html",
                msg="Invalid username or password.",
                form=login_form,
            )
        # Password is invalid
        elif not user.check_password(login_form.password.data):
            flash("Invalid username or password.", "info")
            return render_template(
                "accounts/login.html",
                msg="Invalid username or password.",
                form=login_form,
            )
        # Account is not confirmed
        elif (
            user
            and user.check_password(login_form.password.data)
            and not user.confirmed
        ):
            flash("User has not confirmed by email.", "info")
            return render_template(
                "accounts/login.html",
                msg="User has not confirmed by email.",
                form=login_form,
            )
        # Valid login
        elif user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            next_page = request.args.get("next")
            # only allow relative links
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("home_blueprint.index")
            return redirect(next_page)
        # Unhandled
        else:
            flash("Unknown error.", "error")
            return render_template(
                "accounts/login.html", msg="Unknown error.", form=login_form
            )
    # -------------------------------------------------------------------------#
    # GET Request - Non-Authenticated User
    if not current_user.is_authenticated:
        return render_template("accounts/login.html", form=login_form)
    # -------------------------------------------------------------------------#
    # GET Request - Authenticated User
    else:
        return redirect(url_for("home_blueprint.index"))


# -----------------------------------------------------------------------------#
# Registration Page
@blueprint.route("/register", methods=["GET", "POST"])
def register():
    create_account_form = CreateAccountForm(request.form)
    # -------------------------------------------------------------------------#
    # POST Request - Valid
    if create_account_form.validate_on_submit():

        user = User.query.filter_by(username=create_account_form.username.data).first()
        # Check if usename exists
        if user:
            flash("Username already registered.", "info")
            return render_template(
                "accounts/register.html",
                msg="Username already registered.",
                form=create_account_form,
            )

        # Check if email exists
        user = User.query.filter_by(email=create_account_form.email.data).first()
        if user:
            flash("Email already registered.", "info")
            return render_template(
                "accounts/register.html",
                msg="Email already registered.",
                form=create_account_form,
            )

        # Create user from data
        user = User(**request.form)

        # Send an activation email
        confirmation_token = generate_confirmation_token(user.email)
        confirm_url = url_for(
            "base_blueprint.confirm_email", token=confirmation_token, _external=True
        )
        html = render_template("accounts/activate.html", confirm_url=confirm_url)
        subject = "Please confirm your email."
        try:
            send_email(user.email, subject, html)

        except SMTPAuthenticationError:
            flash(
                "Server-side authentication eror. "
                + "Was mail properly configured for this app?",
                "error",
            )
            return redirect(url_for("base_blueprint.login"))

        # Add the unconfirmed user
        db.session.add(user)
        db.session.commit()

        flash("A confirmation email has been sent.", "success")
        return redirect(url_for("base_blueprint.route_default"))

    # GET Request
    else:
        return render_template("accounts/register.html", form=create_account_form)


# -----------------------------------------------------------------------------#
# Account Confirmation
@blueprint.route("/confirm/<token>")
# @login_required
def confirm_email(token):
    # Check for valid confirmation token
    try:
        email = confirm_token(token)
    except Exception:
        flash("The confirmation link is invalid or has expired.", "error")
        return redirect(url_for("base_blueprint.login"))

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed.", "success")
    else:
        user.confirmed = True
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


# @login_manager.unauthorized_handler
# def unauthorized_handler():
#    flash("Please login to access the requested page.", "info")
#    return redirect(url_for("base_blueprint.login"))


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template("errors/page-403.html"), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template("errors/page-404.html"), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template("errors/page-500.html"), 500
