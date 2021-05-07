import os
import sys
from datetime import datetime
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
import pytest
from application.models import User


@pytest.fixture(scope='module')
def new_user():

    user = User(username='brandon',
                password='asdfasdf',
                email='brandon@example.com',
                account_created_on=datetime.utcnow().strftime('%Y-%m-%d'))
    return user
