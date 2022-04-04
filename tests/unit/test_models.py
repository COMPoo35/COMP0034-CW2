from my_app.models import User


def test_new_user_details_correct():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, email, and password fields are defined correctly
    """
    user_data = {
        'username': 'YouKnowWho',
        'first_name': 'Meat',
        'last_name': 'Loaf',
        'password': 'BatOutOfHell',
        'email': 'meat@bat.org'
    }

    user = User(username=user_data['username'], first_name=user_data['first_name'], last_name=user_data['last_name'],
                email=user_data['email'], password=user_data['password'])

    assert user.username == 'YouKnowWho'
    assert user.first_name == 'Meat'
    assert user.last_name == 'Loaf'
    assert user.email == 'meat@bat.org'
    assert user.password == 'BatOutOfHell'