from datetime import datetime


def test_new_user(new_user):
    '''
    Check the email, password, password, creation
    date fields are defined correctly.
    '''

    assert new_user.username == 'brandon'
    assert new_user.email == 'brandon@example.com'
    assert new_user.password == 'asdfasdf'
    assert new_user.account_created_on == datetime.utcnow().strftime('%Y-%m-%d')
