"""
Utilities for peewee, the beginner-friendly Python ORM.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""


from contextvars import ContextVar
from typing import Iterable
from playhouse.shortcuts import ReconnectMixin
from peewee import BigIntegerField, CharField, Database, Field, MySQLDatabase, _ConnectionState
import re

from suou.iding import Siq
from suou.snowflake import Snowflake

from .codecs import StringCase


## The following code lines are a contribution of Tiangolo, author of FastAPI,
## an async web framework for Python.
## Source: <https://fastapi.tiangolo.com/advanced/sql-databases-peewee/>

class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

class ConnectToDatabase(object):
    db: Database
    def __init__(self, db):
        self.db = db
    async def __aenter__(self):
        self.db.connect(reuse_if_open=True)
        return self
    async def __aexit__(self, *a):
        self.db.close()

class ReconnectMysqlDatabase(ReconnectMixin, MySQLDatabase):
    """
    MySQLDatabase subclass that correctly handles disconnection
    in long-running processes.
    """
    _reconnect_errors: Iterable[tuple[int, str]] = ReconnectMixin.reconnect_errors
    _reconnect_errors += ((0, ''),)

def connect_reconnect(db):
    '''
    Make a Peewee database object suitable for asynchronous connections.
    '''
    if db.__class__ == MySQLDatabase:
        db.__class__ = ReconnectMysqlDatabase

    db._state = PeeweeConnectionState()
    
    return db

## END async helpers for Peewee

class RegexCharField(CharField):
    '''
    CharField() which validates its input before storing.
    '''
    regex: str
    text_transform: StringCase
    def __init__(self, regex: str, *a, text_transform: StringCase | None = None, **k):
        self.regex = regex
        self.text_transform = text_transform or StringCase.AS_IS
        super().__init__(*a, **k)
    def db_value(self, value: str):
        if self.text_transform == StringCase.UPPER:
            value = value.upper()
        if self.text_transform == StringCase.LOWER:
            value = value.lower()
        rgx: re.Pattern = self.text_transform.compile(self.regex)
        if not rgx.fullmatch(value):
            raise ValueError(f'value does not match regexp {self.regex!r}')
        return CharField.db_value(self, value)


class SiqField(Field):
    '''
    Field holding a SIQ.

    Stored as varbinary(16).

    XXX UNTESTED!
    '''
    field_type = 'varbinary(16)'

    def db_value(self, value: int | Siq | bytes) -> bytes:
        if isinstance(value, int):
            value = Siq(value)
        if isinstance(value, Siq):
            value = value.to_bytes()
        if not isinstance(value, bytes):
            raise TypeError
        return value
    def python_value(self, value: bytes) -> Siq:
        return Siq.from_bytes(value)


class SnowflakeField(BigIntegerField):
    '''
    Field holding a snowflake.

    Stored as bigint.

    XXX UNTESTED!
    '''
    field_type = 'bigint'

    def db_value(self, value: int | Snowflake) -> int:
        if isinstance(value, Snowflake):
            value = int(value)
        if not isinstance(value, int):
            raise TypeError
        return value
    def python_value(self, value: int) -> Snowflake:
        return Snowflake(value)

# Optional dependency: do not import into __init__.py
__all__ = ('connect_reconnect', 'RegexCharField', 'SiqField', 'Snowflake')

