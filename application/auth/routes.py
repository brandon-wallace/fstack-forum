# application/auth/routes.py

import secrets
from os import environ, path
from PIL import Image
from flask import Blueprint
from datetime import datetime
from flask import (render_template, url_for, flash,
                   redirect, request, current_app)
# from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from itsdangerous import (TimedJSONWebSignatureSerializer,
                          BadTimeSignature, SignatureExpired)
from application import db, bcrypt, mail
from application.forms import (SignUpForm, LoginForm,
                               UpdateAccountForm,
                               RequestPasswdResetForm,
                               ResetPasswdForm)
from application.models import User
# from application.decorators import check_email_confirmation

auth = Blueprint('auth', __name__)


def create_confirmation_token(email):
    '''Create a confirmation token'''

    serializer = TimedJSONWebSignatureSerializer(environ.get('SECRET_KEY'))
    return serializer.dumps(email, salt=environ.get('SECURITY_PASSWORD_SALT'))


def confirm_token(token, expiration=3600):
    '''Confirm email address with token'''

    serializer = TimedJSONWebSignatureSerializer(environ.get('SECRET_KEY'))
    try:
        email = serializer.loads(token,
                                 salt=environ.get('SECURITY_PASSWORD_SALT'),
                                 max_age=expiration)
    except Exception:
        return False
    return email


@auth.route('/confirm/<token>')
def confirm_email(token):
    '''Confirm user's email'''

    try:
        email = confirm_token(token)
    except BadTimeSignature:
        return 'Email confirmation failed.'
    except SignatureExpired:
        return 'Token expired.'
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account has been confirmed. Please login.', 'success')
        return redirect(url_for('auth.login_route', _external=True))
    if email:
        current_user.email_confirmed = True
        current_user.email_confirmed_date = datetime.utcnow()
        db.session.commit()
        flash('Account creation successful. Please login.', 'success')
    return redirect(url_for('auth.login_route', _external=True))


@auth.route('/unconfirmed')
def unconfirmed():
    '''
    Give user another chance to confirm their email
    '''

    flash('Please confirm your account.', 'warning')
    return render_template('auth/unconfirmed.html')


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
        # msg = Message('Verify Your Email Address',
        #               sender='no-reply@fstackforum.com',
        #               recipients=[request.form['email']])
        # link = generate_url('auth.confirm_email',
        #                     create_confirmation_token(request.form['email']))
        # msg.body = f'''Your email confirmation link is: {link}
        # If you did not make this request then simply
        # ignore this email and no changes will be made.
        # '''
        # mail.send(msg)
        # flash('Please check your email for account confirmation link.',
        #       'success')
        # return redirect(url_for('auth.login'))
        # return link
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data
                                                            ).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data,
                        email_confirmed=False,
                        password=hashed_password,
                        location=form.location.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        except Exception:
            db.session.rollback()
            flash('Something has gone wrong.', 'fail')
            return redirect(url_for('auth.signup'))
    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
# @check_email_confirmation
def login():
    '''Login registered users'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index_page'))

    print(current_user)
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
                return redirect(next_page)
            return redirect(url_for('forum.forum_route'))
        else:
            flash('Login failed. Check your email/password.',
                  'fail')
    return render_template('auth/login.html', form=form)


@auth.route('/profile')
@login_required
def profile():
    '''Profile route'''

    return render_template('auth/profile.html')


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
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.location.data = current_user.location
    profile_image = url_for('static', filename='images/{}'.format(
                            current_user.image_file))
    return render_template('auth/preferences.html',
                           image_file=profile_image, form=form)


@auth.route('/logout')
def logout():
    '''Log user out'''

    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/send_email')
def send_reset_email(user):
    '''Send email route'''

    token = user.retrive_passwd_reset_token(1800)
    msg = Message('Password Reset Request', sender='root@fstackforum.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password click on this link:
{ url_for('auth.reset_token', token=token, _external=True)}
'''
    mail.send(msg)


@auth.route('/reset_password', methods=['GET', 'POST'])
def request_reset_password():
    '''Reset password route'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index_page'))

    form = RequestPasswdResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/request_reset_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    '''Reset password route'''

    if current_user.is_authenticated:
        return redirect(url_for('forum.index_page'))

    user = User.verify_passwd_reset_token(token)
    if user is None:
        flash('Invalid/Expired token', 'warning')
        return redirect(url_for('auth.request_reset_password'))

    form = ResetPasswdForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        db.session.remove()
        flash('Your password has been reset!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_token.html', form=form)


@auth.route('/privacy_policy')
def privacy_policy():
    '''Terms Of Service'''

    return render_template('auth/privacy_policy.html')


@auth.route('/terms_of_service')
def terms_of_service():
    '''Terms Of Service'''

    return render_template('auth/terms_of_service.html')


@auth.route('/bulk')
def bulk_email():
    '''Send email in bulk'''

    users = [{'name': 'Brandon Wallace', 'email': 'brandon@wallace.me'}]

    with mail.connect() as conn:
        for user in users:
            msg = Message('BULK', recipients=[user['email']])
            msg.body = 'Hey everyone!'
            conn.send(msg)
