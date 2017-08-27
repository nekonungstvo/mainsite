"""
Responsible for handling character page processes.
"""

from database import Character, User
from model.authorization import has_permission


class CharacterNotFound(Exception):
    """
    Exception is raised when no character found.
    """

    def __init__(self, login):
        super().__init__("{login} не найден".format(login=login))
        self.login = login


def get_character(login: str) -> Character:
    """
    Get character.

    :param login: Character login.
    :return: Character ORM object.
    """

    character = Character.select(
        lambda character: character.login == login
    ).first()

    if not character:
        raise CharacterNotFound(login)

    return character


def create_character(login: str, user: User) -> Character:
    """
    Creates empty character.

    :login: New character's login.
    :return: New character ORM object.
    """

    return Character(
        login=login,
        user=user,
        status=1
    )


def delete_character(character: Character) -> None:
    """
    Deletes character.
    :param character: Character ORM object.
    :return: Nothing.
    """
    character.delete()


def can_edit_characters(user: User, author: User) -> bool:
    return has_permission(user, "edit_characters") or user == author


def can_see_characters(user: User, author: User) -> bool:
    return has_permission(user, "see_characters") or user == author
