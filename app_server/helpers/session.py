from functools import wraps

from flask import redirect, url_for, flash, session

from data_interface import users


def get_user_account():
    if 'logged_in_user' in session:
        return session['logged_in_user']
    return None


def update_user_account():
    set_user_account(users.get_public_user_account(get_user_id()))


def is_logged_in():
    return get_user_account() is not None


def get_user_id():
    return get_user_account()['Handle']


def set_user_account(user):
    session['logged_in_user'] = user


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if is_logged_in():
            return f(*args, **kwargs)
        else:
            flash("You need to sign in first.", "danger")
            return redirect(url_for('.login'))

    return wrap


def logout():
    set_user_account(None)
