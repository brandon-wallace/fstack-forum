# FStack Forum

# A Forum built with Python, Flask, Flask Blueprints, Flask-SQLAlchemy, and Postgresql.

# https://fstackforum.com/

# Screenshots

![screenshot1](application/static/images/screenshot1.png)
![screenshot2](application/static/images/screenshot2.png)
![screenshot3](application/static/images/screenshot3_dark.png)
![screenshot4](application/static/images/screenshot4.png)


```
├── application/
│   ├── admin/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── forum/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── all.css
│   │   │   └── style.css
│   │   ├── images/
│   │   │   ├── default.png
│   │   │   └── favicon.png
│   │   ├── js/
│   │   │   ├── login.js
│   │   │   └── script.js
│   │   └── webfonts/
│   ├── templates/
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── login.html
│   │   │   ├── preferences.html
│   │   │   └── profile.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── logout.html
│   │   │   ├── preferences.html
│   │   │   ├── privacy_policy.html
│   │   │   ├── profile.html
│   │   │   ├── request_reset_password.html
│   │   │   ├── reset_password_token.html
│   │   │   ├── signup.html
│   │   │   └── terms_of_service.html
│   │   ├── forum/
│   │   │   ├── about.html
│   │   │   ├── create_post.html
│   │   │   ├── feedback.html
│   │   │   ├── forum.html
│   │   │   ├── general.html
│   │   │   ├── help.html
│   │   │   ├── html-css.html
│   │   │   ├── index.html
│   │   │   ├── javascript.html
│   │   │   ├── nodejs.html
│   │   │   ├── post.html
│   │   │   ├── python.html
│   │   │   └── support.html
│   │   ├── 403.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── layout.html
│   │   └── macros.html
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── Pipfile
│   └── Pipfile.lock
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── readme.md
├── run.py
└── wsgi.py
```

# Quick Start

1) Clone repository.
```
$ git clone git@github.com:brandon-wallace/fstack-forum.git

$ cd fstack-forum/
```

2) Create a .env file. Add the following settings before starting the virtual environment:
```
$ vim .env

FLASK_ENV=development
FLASK_APP=run.py
DATABASE_URI='postgres://<username>:<password>@<hostname>:<port>/<database_name>'
DEV_DATABASE_URI='sqlite://<database_file>'
SECRET_KEY=<your_secret_key>
SECURITY_PASSWORD_SALT=<your_password_salt>
MAIL_SERVER=<your_email_server>
MAIL_PORT=<port_number>
MAIL_USERNAME=<your_username>
MAIL_PASSWORD=<your_password>
MAIL_DEFAULT_SENDER=<your_default_email_address>
```

3) Initialize and activate virtual environment.
```
$ pipenv shell
```

4) Install dependencies.
```
$ pipenv install

$ pipenv install flask-debugtoolbar --dev
```

5) Create a Sqlite3 database for development purposes or create a PostgreSQL 
database for production.

Sqlite3
```
$ sqlite3 application/fstackforum.db
```

Postgresql:
```
$ psql

# CREATE DATABASE fstackforum.db

# \q
```

6) Create tables.
```
$ python3 

>>> from application import db, create_app

>>> db.create_all(app=create_app())

>>> exit()
```

7) Start the development server.
```
$ flask run -h 127.0.0.1 -p 5000
```

8) Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)


# License

This project is licensed under the GPL-3.0 License.
