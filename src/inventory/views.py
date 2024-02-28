from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from src import db


inventory_bp = Blueprint("inventory", __name__)


@login_required
@inventory_bp.route("/asset", methods=["GET", "POST"])
def assets():
    return render_template('apps/assets.html')