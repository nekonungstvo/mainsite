from flask import Blueprint, render_template, abort, request, redirect, url_for
from pony.orm import db_session

from database import Character
from model import character as character_model
from model.forms import CharacterForm

character_blueprint = Blueprint(
    'character',
    __name__,
    template_folder='templates',
    url_prefix="/character"
)


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


@character_blueprint.route('/new', methods=["GET", "POST"])
@character_blueprint.route('/<login>/edit', methods=["GET", "POST"])
@db_session
def character_edit_page(login=""):
    character = None
    if login:
        character = character_model.get_character(login)

    form = CharacterForm(request.form, character)

    if request.form and form.validate():
        form.populate_obj(character)
        return redirect(url_for(
            "character.character_page",
            login=form.login.data
        ))

    return render_template(
        'character_edit.jinja2',
        form=form
    )
