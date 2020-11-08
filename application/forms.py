# applications/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField,
                     TextAreaField, SelectField)
from wtforms.validators import (InputRequired, Email, EqualTo,
                                ValidationError, Length)
from application.models import User


class SignUpForm(FlaskForm):
    '''Sign up form for new users'''

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(),
                             Length(min=4, max=32)])
    confirm_password = PasswordField('Re-Enter Password', validators=[
                                     InputRequired(), EqualTo('password')])
    location = StringField('Location')
    submit = SubmitField('SIGN UP')

    def validate_email(self, email):
        '''Check for existing email'''

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')

    def validate_username(self, username):
        '''Check for existing username'''

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')


class LoginForm(FlaskForm):
    '''Login form for registered users'''

    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('LOGIN')


class UpdateAccountForm(FlaskForm):
    '''Update users profile'''

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    location = StringField('Location')
    profile_picture = FileField('Update profile image')
    submit = SubmitField('UPDATE', validators=[
                         FileAllowed(['jpg', 'jpeg', 'png'])])

    def validate_email(self, email):
        '''Check for existing email'''

        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists.')

    def validate_username(self, username):
        '''Check for existing username'''

        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists.')


class CreatePostForm(FlaskForm):
    '''Create post form'''

    title = StringField('Title', validators=[InputRequired()])
    category = SelectField('Category', choices=[
                            ('help', 'Help'),
                            ('python', 'Python'),
                            ('nodejs', 'Nodejs'),
                            ('general', 'General'),
                            ('feedback', 'Feedback'),
                            ('html-css', 'HTML CSS'),
                            ('support', 'Support'),
                            ('javascript', 'Javascript')
                            ])
    content = TextAreaField('Content', validators=[
                            InputRequired(), Length(min=20)])
    submit = SubmitField('CREATE')


class UpdatePostForm(FlaskForm):
    '''Update post form'''

    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[
                            InputRequired(), Length(min=20)])
    submit = SubmitField('UPDATE')


class CommentForm(FlaskForm):
    '''Comment post form'''

    content = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('SUBMIT')


class RequestPasswdResetForm(FlaskForm):
    '''Request a reset password form'''

    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('RESET PASSWORD')

    def validate_email(self, email):
        '''Validate email in database'''

        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email does not exist.')


class ResetPasswdForm(FlaskForm):
    ''''Reset password'''

    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Re-Enter Password', validators=[
                                     InputRequired(), EqualTo('password')])
    submit = SubmitField('RESET PASSWORD')
