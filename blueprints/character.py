from flask import Blueprint, render_template, abort
from pony.orm import db_session

from database import Character

character_blueprint = Blueprint('character', __name__, template_folder='templates')


@character_blueprint.route('/<login>')
@db_session
def character_page(login):
    character = Character.select(
        lambda db_character: db_character.login == login
    ).first()

    if not character:
        return abort(404)

    return render_template(
        'character.jinja2',
        character=character
    )
