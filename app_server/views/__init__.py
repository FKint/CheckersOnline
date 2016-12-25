from main import app
import data_interface
from flask import render_template, jsonify

from views.tests import *
from views.login import *

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


@app.route('/game/<string:game_id>/current')
def get_game_status(game_id):
    return jsonify({"data": data_interface.get_game_status(game_id), "error": None})


@app.route('/game/<string:game_id>')
def show_game(game_id):
    return render_template("game.html", game_id=game_id)
