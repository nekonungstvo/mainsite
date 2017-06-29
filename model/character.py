from database import Character


def get_character_get_generator(login):
    return lambda character: character.login == login


def get_character(login: str) -> Character:
    character = Character.select(
        get_character_get_generator(login)
    ).first()

    if not character:
        raise Exception("CHARACTER NOT FOUND")

    return character
