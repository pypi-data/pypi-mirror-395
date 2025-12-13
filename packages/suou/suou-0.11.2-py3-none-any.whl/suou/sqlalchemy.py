"""
Utilities for SQLAlchemy

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
from typing import Callable, Iterable, Never, TypeVar
import warnings
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Date, Dialect, ForeignKey, LargeBinary, Column, MetaData, SmallInteger, String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Relationship, Session, declarative_base as _declarative_base, relationship

from .snowflake import SnowflakeGen
from .itertools import kwargs_prefix, makelist
from .signing import HasSigner, UserSigner
from .codecs import StringCase
from .functools import deprecated, not_implemented
from .iding import Siq, SiqGen, SiqType, SiqCache
from .classtools import Incomplete, Wanted

_T = TypeVar('_T')

# SIQs are 14 bytes long. Storage is padded for alignment
# Not to be confused with SiqType.
IdType: type[LargeBinary] = LargeBinary(16)

@not_implemented
def sql_escape(s: str, /, dialect: Dialect) -> str:
    """
    Escape a value for SQL embedding, using SQLAlchemy's literal processors.
    Requires a dialect argument.

    XXX this function is not mature yet, do not use
    """
    if isinstance(s, str):
        return String().literal_processor(dialect=dialect)(s)
    raise TypeError('invalid data type')


def create_session(url: str) -> Session:
    """
    Create a session on the fly, given a database URL. Useful for
    contextless environments, such as Python REPL.

    Heads up: a function with the same name exists in core sqlalchemy, but behaves 
    completely differently!!
    """
    engine = create_engine(url)
    return Session(bind = engine)

def id_column(typ: SiqType, *, primary_key: bool = True, **kwargs):
    """
    Marks a column which contains a SIQ.
    """
    def new_id_factory(owner: DeclarativeBase) -> Callable:
        domain_name = owner.metadata.info['domain_name']
        idgen = SiqCache(SiqGen(domain_name), typ)
        def new_id() -> bytes:
            return Siq(idgen.generate()).to_bytes()
        return new_id
    if primary_key:
        return Incomplete(Column, IdType, primary_key = True, default = Wanted(new_id_factory), **kwargs)
    else:
        return Incomplete(Column, IdType, unique = True, nullable = False, default = Wanted(new_id_factory), **kwargs)

def snowflake_column(*, primary_key: bool = True, **kwargs):
    """
    Same as id_column() but with snowflakes.

    XXX this is meant ONLY as means of transition; for new stuff, use id_column() and SIQ.
    """
    def new_id_factory(owner: DeclarativeBase) -> Callable:
        epoch = owner.metadata.info['snowflake_epoch']
        # more arguments will be passed on (?)
        idgen = SnowflakeGen(epoch)
        def new_id() -> int:
            return idgen.generate_one()
        return new_id
    if primary_key:
        return Incomplete(Column, BigInteger, primary_key = True, default = Wanted(new_id_factory), **kwargs)
    else:
        return Incomplete(Column, BigInteger, unique = True, nullable = False, default = Wanted(new_id_factory), **kwargs)


def match_constraint(col_name: str, regex: str, /, dialect: str = 'default', constraint_name: str | None = None) -> CheckConstraint:
    """
    Shorthand for a check constraint. Several dialects are supported.
    """
    return CheckConstraint(text(match_constraint.TEXT_DIALECTS.get(dialect, match_constraint.TEXT_DIALECTS['default'])).bindparams(n=col_name, re=regex),
            name=constraint_name)

match_constraint.TEXT_DIALECTS = {
    'default': ':n ~ :re',
    'postgresql': ':n ~ :re',
    'mariadb': ':n RLIKE :re'
}

def match_column(length: int, regex: str, /, case: StringCase = StringCase.AS_IS, *args, constraint_name: str | None = None, **kwargs) -> Incomplete[Column[str]]:
    """
    Syntactic sugar to create a String() column with a check constraint matching the given regular expression.

    TODO application side validation
    """
    if case != StringCase.AS_IS: # TODO
        warnings.warn('case arg is currently not working', FutureWarning)
    return Incomplete(Column, String(length), Wanted(lambda x, n: match_constraint(n, regex, #dialect=x.metadata.engine.dialect.name,
            constraint_name=constraint_name or f'{x.__tablename__}_{n}_valid')), *args, **kwargs)


def bool_column(value: bool = False, nullable: bool = False, **kwargs) -> Column[bool]:
    """
    Column for a single boolean value.

    NEW in 0.4.0
    """
    def_val = text('true') if value else text('false')
    return Column(Boolean, server_default=def_val, nullable=nullable, **kwargs)


def declarative_base(domain_name: str, master_secret: bytes, metadata: dict | None = None, **kwargs) -> type[DeclarativeBase]:
    """
    Drop-in replacement for sqlalchemy.orm.declarative_base()
    taking in account requirements for SIQ generation (i.e. domain name).
    """
    if not isinstance(metadata, dict):
        metadata = dict()
    if 'info' not in metadata:
        metadata['info'] = dict()
    # snowflake metadata
    snowflake_kwargs = kwargs_prefix(kwargs, 'snowflake_', remove=True, keep_prefix=True)
    metadata['info'].update(
        domain_name = domain_name,
        secret_key = master_secret,
        **snowflake_kwargs
    )
    Base = _declarative_base(metadata=MetaData(**metadata), **kwargs)
    return Base
entity_base = deprecated('use declarative_base() instead')(declarative_base)


def token_signer(id_attr: Column | str, secret_attr: Column | str) -> Incomplete[UserSigner]:
    """
    Generate a user signing function.

    Requires a master secret (taken from Base.metadata), a user id (visible in the token)
    and a user secret.
    """
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
            return UserSigner(owner.metadata.info['secret_key'], id_val.__get__(self, owner), secret_val.__get__(self, owner))
        my_signer.__name__ = name
        return my_signer
    return Incomplete(Wanted(token_signer_factory))


def author_pair(fk_name: str, *, id_type: type = IdType, sig_type: type | None = None, nullable: bool = False, sig_length: int | None = 2048, **ka) -> tuple[Column, Column]:
    """
    Return an owner ID/signature column pair, for authenticated values.
    """
    id_ka = kwargs_prefix(ka, 'id_')
    sig_ka = kwargs_prefix(ka, 'sig_')
    id_col = Column(id_type, ForeignKey(fk_name), nullable = nullable, **id_ka)
    sig_col = Column(sig_type or LargeBinary(sig_length), nullable = nullable, **sig_ka)
    return (id_col, sig_col)


def age_pair(*, nullable: bool = False, **ka) -> tuple[Column, Column]:
    """
    Return a SIS-compliant age representation, i.e. a date and accuracy pair.

    Accuracy is represented by a small integer:
    0 = exact
    1 = month and day
    2 = year and month
    3 = year
    4 = estimated year
    """
    date_ka = kwargs_prefix(ka, 'date_')
    acc_ka = kwargs_prefix(ka, 'acc_')
    date_col = Column(Date, nullable = nullable, **date_ka)
    acc_col = Column(SmallInteger, nullable = nullable, **acc_ka)
    return (date_col, acc_col)


def parent_children(keyword: str, /, *, lazy='selectin', **kwargs) -> tuple[Incomplete[Relationship], Incomplete[Relationship]]:
    """
    Self-referential one-to-many relationship pair.
    Parent comes first, children come later.

    keyword is used in back_populates column names: convention over
    configuration. Naming it otherwise will BREAK your models.
    
    Additional keyword arguments can be sourced with parent_ and child_ argument prefixes,
    obviously.

    CHANGED 0.5.0: the both relationship()s use lazy='selectin' attribute now by default.
    """

    parent_kwargs = kwargs_prefix(kwargs, 'parent_')
    child_kwargs = kwargs_prefix(kwargs, 'child_')

    parent = Incomplete(relationship, Wanted(lambda o, n: o.__name__), back_populates=f'child_{keyword}s', lazy=lazy, **parent_kwargs)
    child = Incomplete(relationship, Wanted(lambda o, n: o.__name__), back_populates=f'parent_{keyword}', lazy=lazy, **child_kwargs)

    return parent, child


def unbound_fk(target: str | Column | InstrumentedAttribute, typ: _T | None = None, **kwargs) -> Column[_T | IdType]:
    """
    Shorthand for creating a "unbound" foreign key column from a column name, the referenced column.

    "Unbound" foreign keys are nullable and set to null when referenced object is deleted.

    If target is a string, make sure to pass the column type at typ= (default: IdType aka varbinary(16))!
    
    NEW 0.5.0
    """
    if isinstance(target, (Column, InstrumentedAttribute)):
        target_name = f'{target.table.name}.{target.name}'
        typ = target.type
    elif isinstance(target, str):
        target_name = target
        if typ is None:
            typ = IdType

    return Column(typ, ForeignKey(target_name, ondelete='SET NULL'), nullable=True, **kwargs)

def bound_fk(target: str | Column | InstrumentedAttribute, typ: _T = None, **kwargs) -> Column[_T | IdType]:
    """
    Shorthand for creating a "bound" foreign key column from a column name, the referenced column.

    "Bound" foreign keys are not nullable and cascade when referenced object is deleted. It means,
    parent deleted -> all children deleted.

    If target is a string, make sure to pass the column type at typ= (default: IdType aka varbinary(16))!
    
    NEW 0.5.0
    """
    if isinstance(target, (Column, InstrumentedAttribute)):
        target_name = f'{target.table.name}.{target.name}'
        typ = target.type
    elif isinstance(target, str):
        target_name = target
        if typ is None:
            typ = IdType

    return Column(typ, ForeignKey(target_name, ondelete='CASCADE'), nullable=False, **kwargs)

def want_column(cls: type[DeclarativeBase], col: Column[_T] | str) -> Column[_T]:
    """
    Return a table's column given its name.

    XXX does it belong outside any scopes?
    """
    if isinstance(col, Incomplete):
        raise TypeError('attempt to pass an uninstanced column. Pass the column name as a string instead.')
    elif isinstance(col, Column):
        return col
    elif isinstance(col, str):
        return getattr(cls, col)
    else:
        raise TypeError

## Utilities for use in web apps below

class AuthSrc(metaclass=ABCMeta):
    '''
    AuthSrc object required for require_auth_base().

    This is an abstract class and is NOT usable directly.

    This is not part of the public API
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

    def decorator(func: Callable):
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

# Optional dependency: do not import into __init__.py
__all__ = (
    'IdType', 'id_column', 'entity_base', 'declarative_base', 'token_signer', 'match_column', 'match_constraint',
    'author_pair', 'age_pair', 'require_auth_base', 'bound_fk', 'unbound_fk', 'want_column'
)