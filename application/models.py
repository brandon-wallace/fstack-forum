# application/models.py

from os import environ
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from application import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    '''Login user to session'''

    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    '''User table'''

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    account_created_on = db.Column(db.DateTime, nullable=False,
                                   default=datetime.utcnow)
    location = db.Column(db.String(100), nullable=True)
    post_count = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def create_password_reset_token(self):
        '''Create the reset token'''

        serializer = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
        return serializer.dumps({'user_id': self.id})

    # "Self" paramenter not needed since method is static.
    @staticmethod
    def verify_password_reset_token(token):
        '''Load the reset token'''

        serializer = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
        try:
            user_id = serializer.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    '''Post table'''

    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(10), index=True, nullable=False)
    date_posted = db.Column(db.DateTime, index=True, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class Comment(db.Model):
    '''Comment table'''

    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    disabled = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.id)
