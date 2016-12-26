from flask import render_template, jsonify

import data_interface
import views.login
import views.tests
from helpers.session import login_required, is_logged_in
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


@app.route('/games')
@login_required
def show_games():
    print(is_logged_in())
    return "To be implemented"


@app.route('/settings/account')
@login_required
def show_account_settings():
    return "To be implemented"


@app.route('/game/<string:game_id>/current')
@login_required
def get_game_status(game_id):
    return jsonify({"data": data_interface.get_game_status(game_id), "error": None})


@app.route('/game/<string:game_id>')
@login_required
def show_game(game_id):
    return render_template("game.html", game_id=game_id)
