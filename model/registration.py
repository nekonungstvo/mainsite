from random import choice

from database import User
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


def get_random_captcha():
    return choice(list(CAPTCHA.keys()))


def check_captcha(question, answer):
    captcha_answer = CAPTCHA.get(question, None)
    return captcha_answer and (captcha_answer.lower() == answer.lower())


def create_user(username: str, password: str):
    return User(
        username=username,
        password_hash=hash_password(password),
        about_text="",
        role=Role.USER
    )
