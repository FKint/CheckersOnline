from flask import render_template, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired

from data_interface import games
from helpers.session import login_required, get_user_id
from main import app


class NewGameForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    opponent = SelectField('Opponent', choices=[("-1", 'Computer')], validators=[])
    own_side = SelectField('Your colour', choices=[("0", 'White'), ("1", 'Black')])
    submit = SubmitField('Submit')


@app.route('/games/new', methods=['GET', 'POST'])
@login_required
def create_new_game():
    form = NewGameForm()
    if form.validate_on_submit():
        if form.own_side.data == 0:
            white_user_id = get_user_id()
            black_user_id = form.opponent.data
        else:
            white_user_id = form.opponent.data
            black_user_id = get_user_id()
        game_id = games.create_new_game(game_name=form.name.data,
                                        white_user_id=white_user_id,
                                        black_user_id=black_user_id)
        return redirect(url_for('.show_game', game_id=game_id))
    return render_template('new_game.html', new_game_form=form)


@app.route('/games')
@login_required
def show_games():
    your_turn_games = games.get_your_turn_games(get_user_id())
    return render_template("games.html", your_turn_games=your_turn_games)


@app.route('/game/<string:game_id>/current')
@login_required
def get_game_status(game_id):
    game_data = games.get_game_data(game_id)
    states = game_data['GameStates']
    return jsonify({"data": games.convert_coordinate_game_state_to_tuple(states[-1]), "error": None})


@app.route('/game/<string:game_id>')
@login_required
def show_game(game_id):
    return render_template("game.html", game=games.get_game_data(game_id))


@app.route('/game/<string:game_id>/move', methods=['POST'])
@login_required
def game_move(game_id):
    return jsonify({"ok": True, "error": None})
