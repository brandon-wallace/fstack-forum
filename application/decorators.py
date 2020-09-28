# application/decorators.py

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def check_email_confirmation(func):
    '''Check if email has been confirmed'''

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.email_confirmed is False:
            flash('Your account is not confirmed!', 'danger')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)
    return decorated_function
