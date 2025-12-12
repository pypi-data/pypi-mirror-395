"""
Database management for BasketCase.
"""

import sqlite3
from importlib import resources
import re
import logging
from datetime import datetime
from pathlib import Path

from basketcase.models import User, Cookie


def _user_factory(cursor: sqlite3.Cursor, row: tuple) -> User:
    user = User(
        id=row[0],
        name=row[1],
        created=row[2],
        cookies=[],
    )

    return user


def _datetime_adapter(datetime_: datetime) -> str:
    return datetime_.isoformat(sep=' ')


def _datetime_converter(datetime_: bytes) -> datetime:
    return datetime.fromisoformat(datetime_.decode())


def _boolean_adapter(boolean: bool) -> int:
    return int(boolean)


def _boolean_converter(integer: bytes) -> bool:
    integer = integer.decode()
    integer = int(integer)
    return bool(integer)


def connect(database_file: Path | str) -> sqlite3.Connection:
    """
    Connect to a database file and return the connection instance.

    Option 'autocommit' is not yet being used, but the code to enable
    it was added here in advance — commented out.

    Enabling foreign_keys only works outside a transaction, and PEP-249
    transaction control (autocommit=False) keeps a transaction open at
    all times. To work around this problem, the connection is first
    created with 'autocommit=True'.
    """
    connection = sqlite3.connect(
        database=database_file,
        # autocommit=True,  # Wait for Python 3.12
        detect_types=sqlite3.PARSE_DECLTYPES,
    )

    connection.execute('PRAGMA foreign_keys = ON')
    # connection.autocommit = False  # Wait for Python 3.12

    sqlite3.register_adapter(datetime, _datetime_adapter)
    sqlite3.register_converter('datetime', _datetime_converter)
    sqlite3.register_adapter(bool, _boolean_adapter)
    sqlite3.register_converter('boolean', _boolean_converter)

    return connection


def migrate(database_file: Path | str):
    """
    Find available database migrations and execute them.
    """
    connection = connect(database_file)
    logger = logging.getLogger(__name__)

    # Get current database version
    cursor = connection.cursor()
    cursor.execute('PRAGMA user_version')
    current_version = f'v{cursor.fetchone()[0]}'
    logger.info('Current database version: %s', current_version)

    # Find available migrations
    available_migrations = []
    migrations_dir = resources.files('basketcase.migrations').iterdir()

    for file in migrations_dir:
        if not file.is_dir():
            continue

        if re.fullmatch(r'v[0-9]+', file.name) is None:
            continue

        if current_version >= file.name:
            continue

        if not file.joinpath('up.sql').is_file():
            continue

        available_migrations.append(file)
        logger.debug('Migration available: %s', file.name)

    available_migrations.sort()

    # Run the migrations
    for migration in available_migrations:
        cursor.executescript(migration.joinpath('up.sql').read_text())
        connection.commit()
        logger.info('Database version is now %s', migration.name)

    connection.close()


class Session:
    """Provide database operations for User and Cookie objects"""

    IG_COOKIE_DOMAIN = '.instagram.com'

    def __init__(self, database_file: Path | str):
        self.connection = connect(database_file)
        self.connection.row_factory = _user_factory

    def _get_cookies(self, users: User | list[User]) -> User | list[User]:
        cursor = self.connection.cursor()
        cursor.row_factory = None
        user_list = []

        if isinstance(users, User):
            # Always force a User into a list, to reuse code
            user_list.append(users)

        if isinstance(users, list):
            user_list.extend(users)

        for user in user_list:
            for row in cursor.execute(
                    '''
                    SELECT * FROM cookie
                    WHERE user = :user
                    ''',
                    {'user': user.id}):
                cookie = Cookie(
                    id=row[0],
                    name=row[1],
                    value=row[2],
                    domain=row[3],
                    user=row[4],
                )

                user.cookies.append(cookie)


        # Return the same type that was passed
        if isinstance(users, list):
            return user_list

        return user_list[0]

    def get_one_by_id(self, uid: int) -> User:
        """
        Get a user by its identifier.

        Arguments:
            uid -- The row ID of a user.
        """
        cursor = self.connection.cursor()

        cursor.execute(
            '''
            SELECT * FROM user
            WHERE id = :id
            ''',
            {'id': uid}
        )

        user = cursor.fetchone()

        if user is None:
            raise ValueError(f'Failed to locate a session with ID {uid}')

        user = self._get_cookies(user)

        return user

    def get_all(self) -> list[User]:
        """
        Get a list of all users.
        """
        cursor = self.connection.cursor()

        cursor.execute(
            '''
            SELECT * FROM user
            '''
        )

        users = cursor.fetchall()
        users = self._get_cookies(users)

        return users

    def update(self, user: User, cursor: sqlite3.Cursor | None = None):
        """
        Update an existing user.

        Arguments:
            user -- User dataclass instance.
            cursor -- Optional cursor (for transaction control).
        """
        cursor_ = self.connection.cursor()

        if cursor is not None:
            cursor_ = cursor

        cursor_.execute(
            '''
            UPDATE user SET
                name = :name,
                created = :created
            WHERE id = :id
            ''',
            {
                'id': user.id,
                'name': user.name,
                'created': user.created,
            }
        )

        cursor_.execute(
            '''
            DELETE FROM cookie
            WHERE user = :user
            ''',
            {'user': user.id}
        )

        for cookie in user.cookies:
            cursor_.execute(
                '''
                INSERT INTO cookie (
                    name,
                    value,
                    user,
                    domain
                ) VALUES (
                    :name,
                    :value,
                    :user,
                    :domain
                )
                ''',
                {
                    'name': cookie.name,
                    'value': cookie.value,
                    'user': cookie.user,
                    'domain': cookie.domain if cookie.domain else '',
                }
            )

        if cursor is None:
            self.connection.commit()

    def insert(self, user: User, cursor: sqlite3.Cursor | None = None) -> int:
        """
        Add a new user and return its row ID.

        Arguments:
            user -- User dataclass instance.
            cursor -- Optional cursor (for transaction control).
        """
        cursor_ = self.connection.cursor()

        if cursor is not None:
            cursor_ = cursor

        cursor_.execute(
            '''
            INSERT INTO user (
                name,
                created
            ) VALUES (
                :name,
                :created
            )
            ''',
            {
                'name': user.name,
                'created': user.created,
            }
        )

        if cursor is None:
            self.connection.commit()

        return cursor_.lastrowid

    def delete(self, user: User, cursor: sqlite3.Cursor | None = None):
        """
        Delete a user (and its cookies).

        Arguments:
            user -- User dataclass instance.
            cursor -- Optional cursor (for transaction control).
        """
        cursor_ = self.connection.cursor()

        if cursor is not None:
            cursor_ = cursor

        cursor_.execute(
            '''
            DELETE FROM user
            WHERE id = :id
            ''',
            {'id': user.id}
        )

        if cursor is None:
            self.connection.commit()
