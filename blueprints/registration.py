from flask import Blueprint, request, url_for, redirect, render_template
from pony.orm import db_session

from blueprints.session import clear_captcha_session, set_captcha_session
from model import registration
from model.forms.definitions import RegistrationForm
from model.registration import get_random_captcha

registration_blueprint = Blueprint(
    'registration',
    __name__,
    template_folder='templates',
    url_prefix="/registration"
)


@registration_blueprint.route('/', methods=["GET", "POST"])
@db_session
def registration_page():
    form = RegistrationForm(request.form)

    username = form.username.data
    password = form.password.data

    # Unique validation moved to mode.forms.validators
    if request.method == 'POST' and form.validate():
        registration.create_user(
            username=username,
            password=password
        )
        print("asdas")
        clear_captcha_session()
        return redirect(url_for('index_page'))

    captcha = get_random_captcha()
    form.set_captcha(captcha)
    set_captcha_session(captcha)

    return render_template(
        'register.html',
        form=form
    )
