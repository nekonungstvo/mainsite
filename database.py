import datetime

from flask_login import UserMixin
from pony.orm import Database, Required, Optional, Set, sql_debug

db = Database()

db.bind('sqlite', 'database_file.sqlite', create_db=True)
sql_debug(False)


class News(db.Entity):
    title = Required(str)
    text = Required(str)

    created_at = Required(datetime.datetime, default=datetime.datetime.now)


class User(db.Entity, UserMixin):
    username = Required(str, unique=True)
    password_hash = Required(str)

    about_text = Optional(str)

    characters = Set(lambda: Character)
    ips = Set(lambda: Ip)


class Ip(db.Entity):
    ip = Required(str)
    users = Set(lambda: User)


class Character(db.Entity):
    login = Required(str, unique=True)

    name = Optional(str)
    appearance = Optional(str)
    story = Optional(str)

    user = Required(lambda: User)
    status = Required(lambda: CharacterStatus)


class CharacterStatus(db.Entity):
    identifier = Optional(str, unique=True)
    characters = Set(lambda: Character)


class CustomPages(db.Entity):
    identifier = Required(str, unique=True)
    title = Optional(str)
    content = Optional(str)


db.generate_mapping(create_tables=True)
