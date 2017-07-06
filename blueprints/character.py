from typing import Union

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from pony.orm import db_session

from database import Character, User
from model import character as character_model
from model import user as user_model
from model.authorization import AuthorizationException
from model.character import can_edit_characters, can_see_characters, CharacterNotFound
from model.forms.definitions import CharacterForm

character_blueprint = Blueprint(
    'character',
    __name__,
    template_folder='templates',
    url_prefix="/character"
)


@character_blueprint.route('/<login>')
@db_session
def character_page(login):
    character = character_model.get_character(login)

    return render_template(
        'character.html',
        character=character
    )


def create_edit_character_page(character: Union[None, Character], user: User) -> str:
    form = CharacterForm(request.form, character)

    if not can_edit_characters(current_user, user):
        raise AuthorizationException("У вас нет прав для редактирования этого персонажа.")

    if request.method == 'POST':
        # Unique validation moved to mode.forms.validators
        if request.form.get("submit") and form.validate():
            if not character:
                character = character_model.create_character(form.login.data, user)

            form.populate_obj(character)

            return redirect(url_for(
                "character.character_page",
                login=form.login.data
            ))
        elif request.form.get("delete"):
            if character:
                character_model.delete_character(character)

            return redirect(url_for(
                "profile.profile_page",
                username=user.username
            ))

    return render_template(
        'character_edit.html',
        form=form,
        create=not character
    )


@character_blueprint.route('/<username>/new', methods=["GET", "POST"])
@db_session
def character_create_page(username):
    return create_edit_character_page(
        character=None,
        user=user_model.get_user(username)
    )


@character_blueprint.route('/<login>/edit', methods=["GET", "POST"])
@db_session
def character_edit_page(login):
    character = character_model.get_character(login)
    return create_edit_character_page(
        character=character,
        user=character.user
    )


@character_blueprint.context_processor
def inject_auth_functions():
    return dict(
        can_edit_characters=can_edit_characters,
        can_see_characters=can_see_characters
    )


@character_blueprint.errorhandler(CharacterNotFound)
def character_not_found(error: CharacterNotFound):
    return render_template(
        'message.html',
        title="Персонаж не найден",
        message="Персонаж с ником \"{login}\" не найден.".format(
            login=error.login
        )
    ), 404
