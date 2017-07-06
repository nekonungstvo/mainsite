from wtforms import ValidationError

from blueprints.session import get_captcha_session
from model.character import get_character, CharacterNotFound
from model.registration import check_captcha
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


class CheckCaptcha:
    def __call__(self, form, field):
        captcha_type = get_captcha_session()
        captcha_answer = field.data.strip()

        if not check_captcha(captcha_type, captcha_answer):
            raise ValidationError("Неправильный ответ на вопрос капчи.")
