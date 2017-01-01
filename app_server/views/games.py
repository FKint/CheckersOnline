from flask import render_template, redirect, url_for, jsonify, request
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired

from application import app
from data_interface import games, users
from game_model import checkers
from helpers.session import login_required, get_user_id, get_user_account


class NewGameForm(FlaskForm):
    name = StringField('Game name', validators=[InputRequired()])
    opponent = SelectField('Opponent (computer or one of your friends)', choices=[("-1", 'Computer')], validators=[])
    own_side = SelectField('Your colour', choices=[(checkers.WHITE, 'White'), (checkers.BLACK, 'Black')],
                           default=checkers.WHITE)
    submit = SubmitField('Submit')


@app.route('/games/new', methods=['GET', 'POST'])
@login_required
def create_new_game():
    form = NewGameForm()
    form.opponent.choices = [("-1", "Computer")] + [(friend, friend) for friend in get_user_account()["Friends"]]
    if form.validate_on_submit():
        if form.own_side.data == checkers.WHITE:
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


class NewGameWithUserForm(FlaskForm):
    name = StringField('Game name', validators=[InputRequired()])
    own_side = SelectField('Your colour', choices=[(checkers.WHITE, 'White'), (checkers.BLACK, 'Black')],
                           default=checkers.WHITE)
    submit = SubmitField('Submit')


@app.route('/games/new/opponent/<string:user_id>', methods=['GET', 'POST'])
@login_required
def start_game_with_user(user_id):
    form = NewGameWithUserForm()
    if form.validate_on_submit():
        if form.own_side.data == checkers.WHITE:
            white_user_id = get_user_id()
            black_user_id = user_id
        else:
            white_user_id = user_id
            black_user_id = get_user_id()
        game_id = games.create_new_game(game_name=form.name.data, white_user_id=white_user_id,
                                        black_user_id=black_user_id)
        return redirect(url_for('.show_game', game_id=game_id))
    return render_template('new_game_with_user.html', user_id=user_id, new_game_form=form)


@app.route('/games')
@login_required
def show_games():
    your_turn_games = games.get_your_turn_games()
    subscribed_games = games.get_subscribed_games()
    participating_games = games.get_participating_games()
    return render_template("games.html", your_turn_games=your_turn_games, subscribed_games=subscribed_games,
                           participating_games=participating_games)


@app.route('/game/<string:game_id>/current')
@login_required
def get_game_status(game_id):
    last_game_state = games.get_current_game_state(game_id)
    return jsonify({"data": last_game_state, "error": None})


@app.route('/game/<string:game_id>')
@login_required
def show_game(game_id):
    game_data = games.get_game_data(game_id)
    own_color = None
    if game_data['BlackPlayerId'] == get_user_id():
        own_color = "BLACK"
    elif game_data['WhitePlayerId'] == get_user_id():
        own_color = "WHITE"

    return render_template("game.html", game=game_data, own_color=own_color,
                           subscribed=(game_id in get_user_account()['GameSubscriptions']))


@app.route('/game/<string:game_id>/move', methods=['POST'])
@login_required
def game_move(game_id):
    data = request.get_json()
    try:
        games.execute_move(game_id, data['src'], data['dst'])
        return jsonify({"ok": True, "error": None})
    except checkers.InvalidTurnException as ex:
        return jsonify({"ok": False, "error": ex.message})


@app.route('/game/<string:game_id>/subscribe')
@login_required
def subscribe_to_game(game_id):
    users.add_game_subscription(get_user_id(), game_id)
    return redirect(url_for('.show_game', game_id=game_id))


@app.route('/game/<string:game_id>/unsubscribe')
@login_required
def unsubscribe_from_game(game_id):
    users.remove_game_subscription(get_user_id(), game_id)
    return redirect(url_for('.show_game', game_id=game_id))
