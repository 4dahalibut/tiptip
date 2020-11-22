# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import json
import requests
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from tiptip.extensions import login_manager
from tiptip.public.forms import LoginForm
from tiptip.user.forms import MerchantRegisterForm, RegisterForm
from tiptip.user.models import Customer, Merchant, User
from tiptip.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")

login_manager.login_view = "/"


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user, remember=True)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        customer = Customer.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        login_user(customer)
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("user.members"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/registerMerchant/", methods=["GET", "POST"])
def register_merchant():
    """Register new merchant."""
    form = MerchantRegisterForm(request.form)
    if form.validate_on_submit():
        merchant = Merchant.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        login_user(merchant)
        flash(
            "Thank you for registering. You will have to wait for an admin to approve before you are able to take payments.",
            "success",
        )
        return redirect(url_for("user.members"))
    else:
        flash_errors(form)
    return render_template("public/register_merchant.html", form=form)


@blueprint.route("/signup/", methods=["post"])
def signup():
    data = {
        "email_address": request.form["email"],
        "status": "subscribed",
    }
    response = requests.post(
        url="https://us7.api.mailchimp.com/3.0/lists/{list_id}/members".format(
            list_id="85ebad71ac"
        ),
        data=json.dumps(data),
        auth=("key", current_app.config["MAILCHIMP_KEY"]),
    )
    if response.status_code == 400:
        return "Your email {} was already added to our list!".format(
            request.form["email"]
        )
    else:
        assert response.status_code == 200, response.content
    return "success!"


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
