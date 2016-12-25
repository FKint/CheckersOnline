from functools import wraps

from flask import redirect, url_for, flash


def get_user_account():
    return None


def is_logged_in():
    return get_user_account() is not None


def get_user_id():
    return get_user_account()['UserId']


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if is_logged_in():
            return f(*args, **kwargs)
        else:
            flash("You need to login first.", "danger")
            return redirect(url_for('.login'))

    return wrap
