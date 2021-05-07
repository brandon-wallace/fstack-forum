import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import pytest
from application.models import User


@pytest.fixture(scope='module')
def new_user():

    user = User('brandon', 'brandon@example.com')
    return user
