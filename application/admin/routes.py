# application/admin/routes.py

# import os
# from PIL import Image
# from datetime import datetime
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from application import db, bcrypt
from application.forms import LoginForm, UpdateAccountForm
from application.models import User
from flask_login import login_user, logout_user, login_required, current_user
admin = Blueprint('admin', __name__)


@admin.route('/login', methods=['GET', 'POST'])
def admin_page():
    '''Login administrator'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)
            return redirect(url_for('forum.forum_route'))
        else:
            flash('Login unsuccessful', 'fail')
    return render_template('admin/login.html', form=form)


@admin.route('/dashboard')
# @login_required
def dashboard():
    '''Dashboard route'''

    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)


@admin.route('/profile')
def profile():
    '''Profile route'''

    return render_template('admin/profile.html')


@admin.route('/preferences', methods=['GET', 'POST'])
# @login_required
def preferences():
    '''Update profile information'''

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            pass
            # profile_image = save_profile_picture(form.profile_picture.data)
            # current_user.image_file = profile_image
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully.', 'success')
        return redirect(url_for('admin.profile'))
    elif request.method == 'GET':
        # Populate username and email upon page load.
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static', filename='images/{}'.format(
                            current_user.image_file))
    return render_template('admin/preferences.html',
                           image_file=profile_image, form=form)


@admin.route('/logout')
def logout():
    '''Log user out'''

    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('forum.index'))
