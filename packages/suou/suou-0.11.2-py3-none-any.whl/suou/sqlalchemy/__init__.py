"""
Utilities for SQLAlchemy.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from functools import wraps
from typing import Any, Callable, Iterable, Never, TypeVar
import warnings
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Date, Dialect, ForeignKey, LargeBinary, Column, MetaData, SmallInteger, String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Relationship, Session, declarative_base as _declarative_base, relationship
from sqlalchemy.types import TypeEngine

from ..snowflake import SnowflakeGen
from ..itertools import kwargs_prefix, makelist
from ..signing import HasSigner, UserSigner
from ..codecs import StringCase
from ..functools import deprecated, not_implemented
from ..iding import Siq, SiqGen, SiqType, SiqCache
from ..classtools import Incomplete, Wanted


_T = TypeVar('_T')
_U = TypeVar('_U')

IdType: TypeEngine = LargeBinary(16)
"""
Database type for SIQ.

SIQs are 14 bytes long. Storage is padded for alignment
Not to be confused with SiqType.
"""

def create_session(url: str) -> Session:
    """
    Create a session on the fly, given a database URL. Useful for
    contextless environments, such as Python REPL.

    Heads up: a function with the same name exists in core sqlalchemy, but behaves 
    completely differently!!
    """
    engine = create_engine(url)
    return Session(bind = engine)


def token_signer(id_attr: Column | str, secret_attr: Column | str) -> Incomplete[UserSigner]:
    """
    Generate a user signing function.

    Requires a master secret (taken from Base.metadata), a user id (visible in the token)
    and a user secret.
    """
    id_val: Column | Wanted[Column]
    if isinstance(id_attr, Column):
        id_val = id_attr
    elif isinstance(id_attr, str):
        id_val = Wanted(id_attr)
    if isinstance(secret_attr, Column):
        secret_val = secret_attr
    elif isinstance(secret_attr, str):
        secret_val = Wanted(secret_attr)
    def token_signer_factory(owner: DeclarativeBase, name: str):
        def my_signer(self):
            return UserSigner(
                owner.metadata.info['secret_key'], 
                id_val.__get__(self, owner), secret_val.__get__(self, owner)  # pyright: ignore[reportAttributeAccessIssue]
            )
        my_signer.__name__ = name
        return my_signer
    return Incomplete(Wanted(token_signer_factory))


## (in)Utilities for use in web apps below

@deprecated('not part of the public API and not even working. Will be removed in 0.14.0')
class AuthSrc(metaclass=ABCMeta):
    '''
    AuthSrc object required for require_auth_base().

    This is an abstract class and is NOT usable directly.

    This is not part of the public API

    DEPRECATED
    '''
    def required_exc(self) -> Never:
        raise ValueError('required field missing')
    def invalid_exc(self, msg: str = 'validation failed') -> Never:
        raise ValueError(msg)
    @abstractmethod
    def get_session(self) -> Session:
        pass
    def get_user(self, getter: Callable):
        return getter(self.get_token())
    @abstractmethod
    def get_token(self):
        pass
    @abstractmethod
    def get_signature(self):
        pass


@deprecated('not working and too complex to use. Will be removed in 0.14.0')
def require_auth_base(cls: type[DeclarativeBase], *, src: AuthSrc, column: str | Column[_T] = 'id', dest: str = 'user',
        required: bool = False, signed: bool = False, sig_dest: str = 'signature', validators: Callable | Iterable[Callable] | None = None):
    '''
    Inject the current user into a view, given the Authorization: Bearer header.

    For portability reasons, this is a partial, two-component function, requiring a AuthSrc() object.
    '''
    col = want_column(cls, column)
    validators = makelist(validators)

    def get_user(token) -> DeclarativeBase:
        if token is None:
            return None
        tok_parts = UserSigner.split_token(token)
        user: HasSigner = src.get_session().execute(select(cls).where(col == tok_parts[0])).scalar()
        try:
            signer: UserSigner = user.signer()
            signer.unsign(token)
            return user
        except Exception:
            return None

    def _default_invalid(msg: str = 'Validation failed'):
        raise ValueError(msg)
        
    invalid_exc = src.invalid_exc or _default_invalid
    required_exc = src.required_exc or (lambda: _default_invalid('Login required'))

    def decorator(func: Callable[_T, _U]) -> Callable[_T, _U]:
        @wraps(func)
        def wrapper(*a, **ka):
            ka[dest] = get_user(src.get_token())
            if not ka[dest] and required:
                required_exc()
            if signed:
                ka[sig_dest] = src.get_signature()
            for valid in validators:
                if not valid(ka[dest]):
                    invalid_exc(getattr(valid, 'message', 'validation failed').format(user=ka[dest]))
            return func(*a, **ka)
        return wrapper
    return decorator


from .asyncio import SQLAlchemy, AsyncSelectPagination, async_query
from .orm import (
    id_column, snowflake_column, match_column, match_constraint, bool_column, declarative_base, parent_children,
    author_pair, age_pair, bound_fk, unbound_fk, want_column, a_relationship, BitSelector, secret_column, username_column
)

# Optional dependency: do not import into __init__.py
__all__ = (
    'IdType', 'id_column', 'snowflake_column', 'entity_base', 'declarative_base', 'token_signer',
    'match_column', 'match_constraint', 'bool_column', 'parent_children',
    'author_pair', 'age_pair', 'bound_fk', 'unbound_fk', 'want_column',
    'a_relationship', 'BitSelector', 'secret_column', 'username_column',
    # .asyncio
    'SQLAlchemy', 'AsyncSelectPagination', 'async_query', 'SessionWrapper'
)