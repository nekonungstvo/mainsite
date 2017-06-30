from database import User
from model.authorization import Role, has_permission


def get_user_get_generator(username):
    return lambda db_user: db_user.username == username


def get_user(username: str) -> User:
    user = User.select(
        get_user_get_generator(username)
    ).first()

    if not user:
        raise Exception("USER NOT FOUND")

    return user


def check_user_exists(username: str) -> bool:
    return User.exists(
        get_user_get_generator(username)
    )


def create_user(username: str, password_hash: str):
    return User(
        username=username,
        password_hash=password_hash,
        about_text="",
        role=Role.USER
    )


def can_edit_profile(user, owener):
    return has_permission(user, "edit_profiles") or user == owener
