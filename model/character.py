from database import Character, User
from model.authorization import has_permission


class CharacterNotFound(Exception):
    def __init__(self, login):
        super().__init__("{login} не найден".format(login=login))
        self.login = login


def get_character_get_generator(login):
    return lambda character: character.login == login


def get_character(login: str) -> Character:
    character = Character.select(
        get_character_get_generator(login)
    ).first()

    if not character:
        raise CharacterNotFound(login)

    return character


def create_character(login, user: User):
    return Character(
        login=login,
        user=user,
        status=1
    )


def delete_character(character: Character):
    character.delete()


def can_edit_characters(user: User, author: User):
    return has_permission(user, "edit_characters") or user == author


def can_see_characters(user: User, author: User):
    return has_permission(user, "see_characters") or user == author
