# application/__init__.py

import logging
from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension

logging.basicConfig(filename='error.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()
toolbar = DebugToolbarExtension()


def create_app():
    '''Get application set up'''

    app = Flask(__name__)

    logging.debug('Running create_app function.')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DEV_DATABASE_URL')
    app.config['DEBUG_TB_ENABLED'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEBUG'] = True
    app.config['TESTING'] = False
    # app.config['MAIL_MAX_EMAILS'] = 99
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_ASCII_ATTACHMENTS'] = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    toolbar.init_app(app)

    from application.auth.routes import auth
    app.register_blueprint(auth)

    from application.admin.routes import admin
    app.register_blueprint(admin)

    from application.forum.routes import forum
    app.register_blueprint(forum)

    return app
