from flask import session


# TODO: rewrite with serverside sessions
def get_captcha_session():
    return session["captcha"]


def set_captcha_session(captcha):
    session["captcha"] = captcha


def clear_captcha_session():
    session["captcha"] = None
