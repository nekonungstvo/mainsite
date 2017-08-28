"""
Module contains ORM objects and database connections.
"""

import datetime

from flask_login import UserMixin
from pony.orm import Database, Required, Optional, Set, sql_debug

db: Database = Database()

db.bind('sqlite', 'database_file.sqlite', create_db=True)
sql_debug(False)


class News(db.Entity):
    """
    ORM object for site news.
    """
    title = Required(str)
    content = Required(str)
    timestamp = Required(datetime.datetime, default=datetime.datetime.now)


class User(db.Entity, UserMixin):
    """
    ORM object for registered users.
    """
    username = Required(str, unique=True)
    password_hash = Required(str)
    about_text = Optional(str)
    role = Required(int)

    characters = Set(lambda: Character)
    ips = Set(lambda: Ip)


class Ip(db.Entity):
    """
    ORM object for loging users' ip.
    """
    ip = Required(str)
    users = Set(lambda: User)


class Character(db.Entity):
    """
    ORM object for storing characters.
    """
    login = Required(str, unique=True)

    name = Optional(str)
    appearance = Optional(str)
    story = Optional(str)

    user = Required(lambda: User)
    status = Required(int)


class CustomPage(db.Entity):
    """
    ORM object for storing custom page.
    """
    identifier = Required(str, unique=True)
    title = Optional(str)
    content = Optional(str)


db.generate_mapping(create_tables=True)
