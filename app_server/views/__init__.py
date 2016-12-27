from flask import render_template

import views.games
import views.login
import views.tests
from helpers.session import login_required
from main import app


@app.route('/')
@app.route('/home')
@app.route('/index')
def show_index():
    return render_template("home.html")


@app.route('/friends')
@login_required
def show_friends():
    return "To be implemented"


@app.route('/settings/account')
@login_required
def show_account_settings():
    return "To be implemented"
