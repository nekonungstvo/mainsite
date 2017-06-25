from flask import Blueprint, abort, render_template
from pony.orm import db_session, desc

from database import User

profile_blueprint = Blueprint('profile', __name__, template_folder='templates')


@profile_blueprint.route('/<username>')
@db_session
def profile_page(username):
    user = User.select(
        lambda db_user: db_user.username == username
    ).first()

    if not user:
        return abort(404)

    return render_template(
        'profile.jinja2',
        user=user,
        characters=user.characters.order_by(
            lambda ch: (desc(ch.status), desc(ch.id))
        )
    )
