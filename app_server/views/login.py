from flask import redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import Email, EqualTo, InputRequired, Length

import data_interface.users
from helpers import session
from main import app


class LoginForm(FlaskForm):
    handle = StringField("Handle")
    password = PasswordField("Password")
    submit = SubmitField("Submit")


# TODO: add copy of handles and email addresses to local instance to check for duplicates
class RegisterForm(FlaskForm):
    handle = StringField("Handle", validators=[InputRequired()])
    email = StringField("Email", validators=[Email(), InputRequired()])
    password1 = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=30)])
    password2 = PasswordField("Repeat password",
                              validators=[InputRequired(), EqualTo('password1', message="Passwords must match.")])
    submit = SubmitField("Submit")


@app.route('/login', methods=["POST", "GET"])
def login():
    if session.is_logged_in():
        flash('Already logged in', 'warning')
        return redirect(url_for('.show_index'))
    form = LoginForm()
    if form.validate_on_submit():
        error, user = data_interface.users.check_user_login(handle=form.handle.data, password=form.password.data)
        if error is not None:
            flash("An error occurred when logging in: {}".format(error['message']), "danger")
        else:
            flash('Successfully signed in!', 'success')
            session.set_user_account(user)
            return redirect(url_for('.show_index'))
    return render_template('login.html', login_form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    if session.is_logged_in():
        flash('Already logged in', 'warning')
        return redirect(url_for('.show_index'))
    form = RegisterForm()
    if form.validate_on_submit():
        error = data_interface.users.register_user(handle=form.handle.data, email=form.email.data,
                                                   password=form.password1.data)
        if error is not None:
            flash("An error occurred when registering: {}".format(error['message']), "danger")
        else:
            flash('Successfully registered!', 'success')
            return redirect(url_for('.show_index'))
    return render_template('register.html', register_form=form)


@app.route('/logout')
def logout():
    if session.is_logged_in():
        session.logout()
        flash('Successfully logged out!', 'success')
    return redirect(url_for('.show_index'))
