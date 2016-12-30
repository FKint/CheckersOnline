from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from data_interface import users
from helpers.session import login_required, get_user_account
from application import app


class AddFriendForm(FlaskForm):
    handle = StringField("Handle", validators=[InputRequired()])
    submit = SubmitField("Submit")


@app.route('/friends', methods=['GET', 'POST'])
@login_required
def show_friends():
    user_data = get_user_account()
    form = AddFriendForm()
    if form.validate_on_submit():
        if users.add_friend(form.handle.data):
            flash('Friendship successfully added', 'success')
            return redirect(url_for('.show_friends'))
        else:
            flash('Error adding friendship', 'danger')
    friends = map(lambda x: {"Handle": x}, user_data['Friends'])
    return render_template('friends.html', friends=friends, add_friend_form=form)


@app.route('/user/<string:user_id>')
@login_required
def show_user(user_id):
    return "To be implemented: user {}".format(user_id)
