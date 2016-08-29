from backend.model import User


def test_user_change_password():
    user = User()
    user.change_password('hunter2')

    assert user.password == 'hunter2'
    assert user.password != 'mahpassword'
    assert user.password_changed_at
