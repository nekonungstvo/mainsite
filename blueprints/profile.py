from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from pony.orm import db_session, desc

from model import user as user_model
from model.authorization import AuthorizationException
from model.character import can_edit_characters, can_see_characters
from model.forms import AboutForm
from model.user import can_edit_profile

profile_blueprint = Blueprint(
    'profile',
    __name__,
    template_folder='templates',
    url_prefix="/profile"
)


@profile_blueprint.route('/<username>')
@db_session
def profile_page(username):
    user = user_model.get_user(username)
    return render_template(
        'profile.jinja2',
        user=user,
        characters=user.characters.order_by(
            lambda ch: (desc(ch.status), desc(ch.id))
        )
    )


@profile_blueprint.route('/<username>/edit', methods=["GET", "POST"])
@db_session
def profile_edit_page(username):
    user = user_model.get_user(username)
    form = AboutForm(request.form, obj=user)

    if not can_edit_profile(current_user, user):
        raise AuthorizationException("YOU ARE NOT ALLOWED TO CHANGE USER INFO")

    if request.form and form.validate():
        form.populate_obj(user)
        return redirect(
            url_for(
                'profile.profile_page',
                username=username
            )
        )

    return render_template(
        'profile_edit.jinja2',
        user=user,
        form=form
    )


@profile_blueprint.context_processor
def inject_auth_functions():
    return dict(
        can_edit_profile=can_edit_profile,
        can_edit_characters=can_edit_characters,
        can_see_characters=can_see_characters
    )
