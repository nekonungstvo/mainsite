from random import choice

from database import User


class AuthorizationException(Exception):
    status_code = 403

    def __init__(self, message):
        super().__init__(message)
        self.message = message


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


CAPTCHA = {
    "Антоним слова «хороший»": "плохой",
    "Фамилия первого советского космонавта": "гагарин",
    "Какое из слов лишнее: город, посёлок, село, ананас": "ананас",
    "Какое из слов лишнее: лопата, клавиатура, кирка, мотыга": "клавиатура",
    "Сколько месяцев в году? (ответ числом)": "12",
    "Сколько дней в неделе? (ответ цифрой)": "7",
    "Столица России": "москва",
    "Столица Украины": "киев",
    "Сколько минут в одном часе? (ответ числом)": "60",
    "Сколько часов в сутках? (ответ числом)": "24",
    "(Гоголь) В России две беды — дураки и ...": "дороги",
    "Какая фамилия у поэта Александра Сергеевича?": "пушкин",
    "Какое из слов лишнее: тигр, лев, сова, пантера": "сова",
    "Просто напишите букву «Ц» семь раз подряд": "ццццццц",
}


def get_random_captcha():
    question = choice(CAPTCHA.keys())
    return question, CAPTCHA.get(question)


def check_captcha(question, answer):
    return CAPTCHA.get(question) == answer
