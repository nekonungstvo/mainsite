from database import User
from model.authorization import has_permission


class UserNotFound(Exception):
    def __init__(self, username):
        super().__init__("{username} не найден".format(username=username))
        self.username = username


def get_user(username: str) -> User:
    user = User.select(
        lambda db_user: db_user.username == username
    ).first()

    if not user:
        raise UserNotFound(username=username)

    return user


def can_edit_profile(user, owener):
    return has_permission(user, "edit_profiles") or user == owener
