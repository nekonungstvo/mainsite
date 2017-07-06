import hashlib

from database import User


class AuthorizationException(Exception):
    status_code = 403

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


def check_password(user: User, password):
    return user.password_hash == hash_password(password)


class Role:
    ANONYMOUS = 0
    BANNED = 1
    USER = 2
    ELITE = 3
    GM = 4
    ADMIN = 5


roles_perm = dict()
roles_perm[Role.ANONYMOUS] = []

roles_perm[Role.BANNED] = []

roles_perm[Role.USER] = []

roles_perm[Role.ELITE] = [
    *roles_perm.get(Role.USER),
    "gallery"
]

roles_perm[Role.GM] = [
    *roles_perm.get(Role.USER),
    "gallery",
    "see_characters",
    "edit_characters"
]

roles_perm[Role.ADMIN] = [
    *roles_perm.get(Role.GM),
    "edit_profiles",
    "edit_custom_pages",
    "set_role"
]


def has_permission(user: User, permission: str) -> bool:
    if not user.is_authenticated:
        return permission in roles_perm.get(Role.ANONYMOUS, [])
    return permission in roles_perm.get(user.role, [])
