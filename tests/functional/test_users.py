from application.models import User


def test_new_user():
    '''
    Check the email, password, password, creation
    date fields are defined correctly.
    '''

    user = User('brandon', 'brandon@example.com', 'asdfasdf', '2022-12-1')
    assert user.username == 'brandon'
    assert user.email == 'brandon@example.com'
    assert user.password == 'asdfasdf'
    assert user.account_created_on == '2022-12-1'
