from main import app

from flask import render_template


@app.route('/')
@app.route('/home')
@app.route('/index')
def show_index():
    return render_template("home.html")


@app.route('/friends')
def show_friends():
    return "To be implemented"


@app.route('/games')
def show_games():
    return "To be implemented"


@app.route('/settings/account')
def show_account_settings():
    return "To be implemented"


@app.route('/logout')
def logout():
    return "To be implemented"
