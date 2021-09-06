# application/auth/routes.py

import logging
import secrets
from os import environ, path
from PIL import Image
from datetime import datetime
from flask import (Blueprint, render_template, url_for,
                   flash, redirect, request, current_app)
# from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message, Mail
from itsdangerous import (URLSafeTimedSerializer, BadTimeSignature,
                          SignatureExpired)
from application import db, bcrypt
from application.forms import (SignUpForm, LoginForm,
                               UpdateAccountForm,
                               RequestPasswordResetForm,
                               SendConfirmationLinkForm,
                               ResetPasswordForm)
from application.models import User
from application.decorators import check_email_confirmation
from application.generate_avatar import create_image

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('auth_error.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: \
                              %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

auth = Blueprint('auth', __name__)


def create_confirmation_token(email):
    '''Create a confirmation token'''

    serializer = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
    return serializer.dumps(email, salt=environ.get('SECURITY_PASSWORD_SALT'))


def confirm_token(token, expiration=86400):
    '''Confirm email address with token'''

    serializer = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
    try:
        email = serializer.loads(token,
                                 salt=environ.get('SECURITY_PASSWORD_SALT'),
                                 max_age=expiration)
    except Exception:
        logger.error(f'Confirm token error', exc_info=True)
        return False
    return email


@auth.route('/confirm')
def confirm():
    '''Email confirmation route'''

    return render_template('auth/confirm.html')


@auth.route('/confirm/<token>')
def confirm_email(token):
    '''Confirm user's email'''

    try:
        email = confirm_token(token)
    except BadTimeSignature:
        flash('Email confirmation failed.', 'fail')
        logger.error('BadTimeSignature Error!!!!', exc_info=True)
        return
    except SignatureExpired:
        flash('Token exired.', 'fail')
        logger.error('SignatureExpired Error!!!!', exc_info=True)
        return

    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account confirmed. Please login.', 'success')
        return redirect(url_for('auth.login_route', _external=True))
    else:
        user.email_confirmed = True
        user.email_confirmed_date = datetime.utcnow()
        db.session.commit()
        flash('Account creation successful. Please login.', 'success')
    return redirect(url_for('auth.login_route', _external=True))


@auth.route('/unconfirmed')
def email_not_confirmed():
    '''
    Give user another chance to confirm their email
    '''

    form = SendConfirmationLinkForm()
    if form.validate_on_submit():
        email = request.form['email']
        msg = Message('Confirm Your Email Address',
                      sender='no-reply@fstackforum.com',
                      recipients=[email])
        link = generate_url('auth.confirm_email',
                            create_confirmation_token(email))
        msg.body = f'''Hi!

Please confirm your email account to complete registration at Fstackforum.com.
Click on the link or copy and paste it into the address bar.
Email confirmation link:

{link}

If you did not make this request ignore this email.

This link will expire in 24 hours.
'''
        with current_app.app_context():
            mail = Mail()
            mail.send(msg)
        flash('Check your email for the confirmation link.', 'success')
        return redirect(url_for('auth.login_route', _external=True))
    return render_template('auth/unconfirmed.html', form=form)


def generate_url(endpoint, token):
    '''Generate confirmation URL'''

    return url_for(endpoint, token=token, _external=True)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    '''Sign up new users'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index'))

    form = SignUpForm()
    if form.validate_on_submit():
        email = request.form['email']
        msg = Message('Verify Your Email Address',
                      sender='no-reply@fstackforum.com',
                      recipients=[email])
        link = generate_url('auth.confirm_email',
                            create_confirmation_token(email))
        msg.body = f'''Hi {request.form['username']}!,

Please confirm your email account to complete registration at Fstackforum.com.
Click on the link or copy and paste it into the address bar.
Email confirmation link:

{link}

If you did not make this request ignore this email.

This link will expire in 24 hours.
'''
        with current_app.app_context():
            mail = Mail()
            mail.send(msg)
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data
                                                            ).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data,
                        email_confirmed=False,
                        image_file=create_image(),
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            db.session.remove()
            return redirect(url_for('auth.confirm', _external=True))
        except Exception:
            logger.error('Sign up route error!!!!', exc_info=True)
            db.session.rollback()
            return redirect(url_for('auth.sign_up', _external=True))
    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login_route():
    '''Login registered users'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            view_count = int(request.cookies.get('view-count', 0))
            view_count += 1
            # user_agent = request.headers.get('User-Agent')
            # host = request.headers.get('Host')
            # referer = request.headers.get('Referer')
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                pass
            #     return redirect(next_page)
            return redirect(url_for('forum.forum_route', _external=True))
        else:
            logger.warn('Login failure!!!!', exc_info=True)
            flash('Login failed. Check your email/password.', 'fail')
    return render_template('auth/login.html', form=form)


@auth.route('/profile')
@login_required
@check_email_confirmation
def profile():
    '''Profile route'''

    profile_image = url_for('static', filename='images/{}'.format(
                            current_user.image_file))
    return render_template('auth/profile.html', image_file=profile_image)


def save_profile_picture(image_file):
    '''Save user's profile picture'''

    random_hex = secrets.token_hex(8)
    _, file_ext = path.splitext(image_file.filename)
    picture_filename = random_hex + file_ext
    picture_path = path.join(current_app.root_path,
                             'static/images', picture_filename)
    output_size = (125, 125)
    pic = Image.open(image_file)
    pic.thumbnail(output_size)
    pic.save(picture_path)

    return picture_filename


@auth.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    '''Update profile information'''

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_image = save_profile_picture(form.profile_picture.data)
            current_user.image_file = profile_image
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        db.session.commit()
        db.session.remove()
        flash('Account updated successfully.', 'success')
        return redirect(url_for('auth.profile', _external=True))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.location.data = current_user.location
    profile_image = url_for('static', filename='images/{}'.format(
                            current_user.image_file))
    return render_template('auth/preferences.html',
                           image_file=profile_image, form=form)


@auth.route('/logout')
@login_required
def logout():
    '''Log user out'''

    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login_route', _external=True))


def send_reset_email(user):
    '''Send email route'''

    msg = Message('Password Reset Request',
                  sender=('no-reply', 'no-reply@fstackforum.com'),
                  recipients=[user.email])
    link = generate_url('auth.reset_token',
                        user.retrive_password_reset_token())
    msg.body = f'''To reset your password please click on this link or or cut
and paste it into your browser.

{link}

This link will expire in 15 minutes.

The Fstackforum Team
-
'''
    with current_app.app_context():
        mail = Mail()
        mail.send(msg)


@auth.route('/request_reset_password', methods=['GET', 'POST'])
def request_reset_password():
    '''Request password reset route'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index_page', _external=True))

    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        send_reset_email(user)
        flash('Check your email for reset link.', 'info')
        return redirect(url_for('auth.login_route', _external=True))
    return render_template('auth/request_reset_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    '''Reset password route'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index_page', _external=True))

    user = User.verify_password_reset_token(token)
    if user is None:
        flash('Invalid/Expired token', 'warning')
        return redirect(url_for('auth.request_reset_password', _external=True))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_passwd = bcrypt.generate_password_hash(form.password.data).decode(
                                                   'utf-8')
        user.password = new_passwd
        db.session.commit()
        flash('Your password has been reset!', 'success')
        return redirect(url_for('auth.login_route', _external=True))
    return render_template('auth/reset_password_token.html', form=form)


@auth.route('/privacy_policy')
def privacy_policy():
    '''Privacy Policy'''

    return render_template('auth/privacy_policy.html')


@auth.route('/terms_of_service')
def terms_of_service():
    '''Terms Of Service'''

    return render_template('auth/terms_of_service.html')
