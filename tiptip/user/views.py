# -*- coding: utf-8 -*-
"""User views."""
import simplejson as json  # Used
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_api import status
from tiptip.user.models import Merchant

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/tip", methods=("POST",))
@login_required
def tip():
    amount = request.form["amount"]
    merchant_id = request.form["merchant_id"].strip()
    merchant = Merchant.get_by_id(merchant_id)
    if merchant is None:
        return status.HTTP_400_BAD_REQUEST
    current_user.charge(amount)
    merchant.pay(amount)

    return "Tip Complete", status.HTTP_202_ACCEPTED


@blueprint.route("/verify", methods=("POST",))
@login_required
def verify():
    """List members."""
    if not current_user.is_authenticated or not current_user.is_admin:
        return status.HTTP_401_UNAUTHORIZED
    merchant_id = request.form["merchant_id"]
    merchant = Merchant.get_by_id(merchant_id)
    merchant.verify()

    return status.HTTP_202_ACCEPTED


@blueprint.route("/charges", methods=("GET",))
@login_required
def get_charges():
    return {"charge": current_user.amount_paid}, status.HTTP_200_OK


@blueprint.route("/earnings", methods=("GET",))
@login_required
def get_earnings():
    """List members."""
    return {"earnings": current_user.amount_earned}, status.HTTP_200_OK


@blueprint.route("/cookie", methods=("GET",))
@login_required
def get_cookie():
    """List members."""
    if not current_user.is_authenticated or not current_user.is_admin:
        return status.HTTP_401_UNAUTHORIZED
    return status.HTTP_202_ACCEPTED, current_user
