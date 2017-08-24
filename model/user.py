from database import User
from model.authorization import has_permission


class UserNotFound(Exception):
    """
    Exception is thrown when no user found,
    """

    def __init__(self, username):
        super().__init__("{username} не найден".format(username=username))
        self.username = username


def get_user(username: str) -> User:
    """
    Fetchig user by his username.
    Throws `UserNotFound` exception when there is no user.

    :param username: Username.
    :return: User orm object.
    """

    user = User.select(
        lambda db_user: db_user.username == username
    ).first()

    if not user:
        raise UserNotFound(username=username)

    return user


def can_edit_profile(user: User, owner: User) -> bool:
    """
    Checks if user can edit other user's profile.

    :param user: User orm object.
    :param owner: Profile's owner orm object.
    :return: True if can and False if can't.
    """

    return has_permission(user, "edit_profiles") or user == owner
