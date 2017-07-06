from wtforms import ValidationError

from model.character import get_character, CharacterNotFound
from model.user import get_user, UserNotFound


class UserUnique:
    def __init__(self, message="User already exists."):
        self.message = message

    def __call__(self, form, field):
        try:
            get_user(field.data)
            raise ValidationError(self.message)
        except UserNotFound:
            pass


class CharacterUnique:
    def __init__(self, message="Character name already taken."):
        self.message = message

    def __call__(self, form, field):
        try:
            get_character(field.data)
            raise ValidationError(self.message)
        except CharacterNotFound:
            pass
