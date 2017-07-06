from flask import Blueprint, request, url_for, redirect, render_template
from pony.orm import db_session

from model import registration
from model.forms.definitions import RegistrationForm

registration_blueprint = Blueprint(
    'registration',
    __name__,
    template_folder='templates',
    url_prefix="/registration"
)


@registration_blueprint.route('/', methods=["GET", "POST"])
@db_session
def registration_page(user_model=None):
    form = RegistrationForm(request.form)

    username = form.username.data
    password = form.password.data

    # Unique validation moved to mode.forms.validators
    if request.method == 'POST' and form.validate():
        registration.create_user(
            username=username,
            password=password
        )

        return redirect(url_for('index_page'))

    return render_template(
        'register.html',
        form=form
    )
