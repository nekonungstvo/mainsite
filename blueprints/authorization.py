import hashlib

from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import logout_user, login_user
from pony.orm import db_session

from model import user as user_model
from model.authorization import AuthorizationException
from model.forms import LoginForm, RegistrationForm
from model.user import UserNotFound

authorization_blueprint = Blueprint(
    'authorization',
    __name__,
    template_folder='templates',
    url_prefix="/auth"
)


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


@authorization_blueprint.route('/register', methods=["GET", "POST"])
@db_session
def registration_page():
    form = RegistrationForm(request.form)
    errors = []

    username = form.username.data
    password = form.password.data

    unique = not user_model.check_user_exists(username)

    if request.method == 'POST' and form.validate() and unique:
        user_model.create_user(
            username=username,
            password_hash=hash_password(password)
        )

        return redirect(url_for('index_page'))

    if not unique:
        errors.append("Это имя пользователя уже занято.")

    errors += [
        message
        for messages in form.errors.values()
        for message in messages

    ]

    return render_template(
        'register.html',
        form=form,
        errors=errors
    )


@authorization_blueprint.route('/login', methods=["POST"])
@db_session
def login_action():
    form = LoginForm(request.form)

    username = form.username.data
    password = form.password.data

    user = user_model.get_user(username)

    if user.password_hash != hash_password(password):
        raise AuthorizationException("Неверный пароль")

    login_user(user)
    return redirect(url_for('index_page'))


@authorization_blueprint.route('/logout')
@db_session
def logout_action():
    logout_user()
    return redirect(url_for('index_page'))


@authorization_blueprint.errorhandler(UserNotFound)
def user_not_found(error: UserNotFound):
    return render_template(
        'message.html',
        title="Ошибка авторизации",
        message="Пользователь {username} не найден.".format(
            username=error.username
        )
    ), 404


@authorization_blueprint.app_errorhandler(AuthorizationException)
def handle_auth_error(error: AuthorizationException):
    return render_template(
        "message.html",
        title="Ошибка авторизации",
        message=error.message
    ), error.status_code
