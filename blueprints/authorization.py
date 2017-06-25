import hashlib

from flask import Blueprint, redirect, url_for, abort, request, render_template
from flask_login import logout_user, login_user
from pony.orm import db_session, exists

from database import User
from forms import LoginForm, RegistrationForm

authorization_blueprint = Blueprint('authorization', __name__, template_folder='templates')


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


@authorization_blueprint.route('/register', methods=["GET", "POST"])
@db_session
def registration_page():
    form = RegistrationForm(request.form)
    errors = []

    username = form.username.data
    password = form.password.data

    unique = not exists(
        user for user in User
        if user.username == username
    )

    if request.method == 'POST' and form.validate() and unique:
        user = User(
            username=username,
            password_hash=hash_password(password),
            about_text=""
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
        'register.jinja2',
        form=form,
        errors=errors
    )


@authorization_blueprint.route('/login', methods=["POST"])
@db_session
def login_action():
    form = LoginForm(request.form)

    username = form.username.data
    password = form.password.data

    user = User.select(
        lambda db_user: db_user.username == username
    ).first()

    if not user:
        return abort(404)

    if user.password_hash == hash_password(password):
        login_user(user)
        return redirect(url_for('index_page'))


@authorization_blueprint.route('/logout')
@db_session
def logout_action():
    logout_user()
    return redirect(url_for('index_page'))
