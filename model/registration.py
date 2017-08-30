"""
Module containing registration functions.
"""

from random import choice

from model.database import User
from model.authorization import hash_password, Role

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


def get_random_captcha() -> str:
    """
    Returns random captcha question.
    """
    return choice(list(CAPTCHA.keys()))


def check_captcha(question: str, answer: str) -> bool:
    """
    Checks if captcha answer is correct.
    :param question: Question text.
    :param answer: User's input.
    :return: True if answer is correct and False if not.
    """
    captcha_answer = CAPTCHA.get(question, None)
    return (
        captcha_answer is not None
    ) and (
        captcha_answer.lower() == answer.lower()
    )


def create_user(username: str, password: str) -> User:
    """
    Creates user database record.
    :param username: New user's name.
    :param password: New user's password.
    :return: New user's orm object.
    """
    return User(
        username=username,
        password_hash=hash_password(password),
        about_text="",
        role=Role.USER
    )
