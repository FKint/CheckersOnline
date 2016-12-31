from functools import wraps
from datetime import datetime

from flask import redirect, url_for, flash, session

from data_interface import users


def get_user_account(fresh=False):
    if 'logged_in_user' in session:
        if fresh:
            should_update = True
            if 'last_update' in session:
                last_update = session['last_update']
                difference = datetime.now() - last_update
                if difference.total_seconds() < 2:
                    should_update = False
            if should_update:
                update_user_account()
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
