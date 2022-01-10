# application/__init__.py

import logging
from os import environ
from datetime import datetime, timedelta
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('flask_error.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: \
                              %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

db = SQLAlchemy()
security = Security()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login_route'
mail = Mail()
administrator = Admin(name='fstack-forum')
ckeditor = CKEditor()


def datetime_format(value, format="%Y-%m-%d %H:%M:%S"):
    '''Format datetime'''

    time_passed = datetime.utcnow() + timedelta(days=value.day,
                                                minutes=value.minute,
                                                hours=value.hour)
    return time_passed.strftime(format)


def create_app():
    '''Get application set up'''

    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
    # app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DEV_DATABASE_URI')
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = environ.get('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = environ.get('SENDGRID_API_KEY')
    app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEBUG'] = True
    app.config['TESTING'] = False
    # app.config['MAIL_MAX_EMAILS'] = 1
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_ASCII_ATTACHMENTS'] = True

    with app.app_context():
        db.init_app(app)
    administrator.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)

    from application.auth.routes import auth
    app.register_blueprint(auth)

    from application.admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    from application.forum.routes import forum
    app.register_blueprint(forum)

    app.jinja_env.filters['datetime_format'] = datetime_format

    # security.init_app(app, user_datastore)

    return app


from flask_admin.contrib.sqla import ModelView
from application.models import db, User, Role
administrator.add_view(ModelView(User, db.session))
