"""
Utilities for SQLAlchemy; ORM

*New in 0.6.0 (moved)*

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""



from binascii import Incomplete
import os
import re
from typing import Any, Callable, TypeVar
import warnings
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, ForeignKey, LargeBinary, MetaData, SmallInteger, String, text
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Relationship, declarative_base as _declarative_base, relationship
from sqlalchemy.types import TypeEngine
from sqlalchemy.ext.hybrid import Comparator
from suou.functools import future
from suou.classtools import Wanted, Incomplete
from suou.codecs import StringCase
from suou.dei import dei_args
from suou.iding import Siq, SiqCache, SiqGen, SiqType
from suou.itertools import kwargs_prefix
from suou.snowflake import SnowflakeGen
from suou.sqlalchemy import IdType


_T = TypeVar('_T')


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

def match_column(length: int, regex: str | re.Pattern, /, case: StringCase = StringCase.AS_IS, *args, constraint_name: str | None = None, **kwargs) -> Incomplete[Column[str]]:
    """
    Syntactic sugar to create a String() column with a check constraint matching the given regular expression.

    TODO application side validation
    """
    if case != StringCase.AS_IS: # TODO
        warnings.warn('case arg is currently not working', FutureWarning)
    return Incomplete(Column, String(length), Wanted(lambda x, n: match_constraint(n, regex, #dialect=x.metadata.engine.dialect.name,
            constraint_name=constraint_name or f'{x.__tablename__}_{n}_valid')), *args, **kwargs)


def username_column(
        length: int = 32, regex: str | re.Pattern = '[a-z_][a-z0-9_-]+', *args, case: StringCase = StringCase.LOWER,
        nullable : bool = False, **kwargs) -> Incomplete[Column[str] | Column[str | None]]:
    """
    Construct a column containing a unique handle / username.

    Username must match the given `regex` and be at most `length` characters long.

    *New in 0.8.0*
    """
    if case is StringCase.AS_IS:
        warnings.warn('case sensitive usernames may lead to impersonation and unexpected behavior', UserWarning)

    return match_column(length, regex, case=case, nullable=nullable, unique=True, *args, **kwargs)


def bool_column(value: bool = False, nullable: bool = False, **kwargs) -> Column[bool]:
    """
    Column for a single boolean value.

    *New in 0.4.0*
    """
    def_val = text('true') if value else text('false')
    return Column(Boolean, server_default=def_val, nullable=nullable, **kwargs)


@dei_args(primary_secret='master_secret')
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
entity_base = warnings.deprecated('use declarative_base() instead')(declarative_base)



def author_pair(fk_name: str, *, id_type: type | TypeEngine = IdType, sig_type: type | None = None, nullable: bool = False, sig_length: int | None = 2048, **ka) -> tuple[Column, Column]:
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


def secret_column(length: int = 64, max_length: int | None = None, gen: Callable[[int], bytes] = os.urandom, nullable=False, **kwargs):
    """
    Column filled in by default with random bits (64 by default). Useful for secrets.

    *New in 0.6.0*
    """
    max_length = max_length or length
    return Column(LargeBinary(max_length), default=lambda: gen(length), nullable=nullable, **kwargs)



def parent_children(keyword: str, /, *, lazy='selectin', **kwargs) -> tuple[Incomplete[Relationship[Any]], Incomplete[Relationship[Any]]]:
    """
    Self-referential one-to-many relationship pair.
    Parent comes first, children come later.

    keyword is used in back_populates column names: convention over
    configuration. Naming it otherwise will BREAK your models.
    
    Additional keyword arguments can be sourced with parent_ and child_ argument prefixes,
    obviously.

    *Changed in 0.5.0*: the both relationship()s use lazy='selectin' attribute now by default.
    """

    parent_kwargs = kwargs_prefix(kwargs, 'parent_')
    child_kwargs = kwargs_prefix(kwargs, 'child_')

    parent: Incomplete[Relationship[Any]] = Incomplete(relationship, Wanted(lambda o, n: o.__name__), back_populates=f'child_{keyword}s', lazy=lazy, **parent_kwargs)
    child: Incomplete[Relationship[Any]] = Incomplete(relationship, Wanted(lambda o, n: o.__name__), back_populates=f'parent_{keyword}', lazy=lazy, **child_kwargs)

    return parent, child


def a_relationship(primary = None, /, j=None, *, lazy='selectin', **kwargs):
    """
    Shorthand for relationship() that sets lazy='selectin' by default.

    *New in 0.6.0*
    """
    if j:
        kwargs['primaryjoin'] = j
    return relationship(primary, lazy=lazy, **kwargs)  # pyright: ignore[reportArgumentType]


def unbound_fk(target: str | Column | InstrumentedAttribute, typ: _T | None = None, **kwargs) -> Column[_T | IdType]:
    """
    Shorthand for creating a "unbound" foreign key column from a column name, the referenced column.

    "Unbound" foreign keys are nullable and set to null when referenced object is deleted.

    If target is a string, make sure to pass the column type at typ= (default: IdType aka varbinary(16))!
    
    *New in 0.5.0*
    """
    if isinstance(target, (Column, InstrumentedAttribute)):
        target_name = f'{target.table.name}.{target.name}'
        typ = target.type
    elif isinstance(target, str):
        target_name = target
        if typ is None:
            typ = IdType
    else:
        raise TypeError('target must be a str, a Column or a InstrumentedAttribute')

    return Column(typ, ForeignKey(target_name, ondelete='SET NULL'), nullable=True, **kwargs)

def bound_fk(target: str | Column | InstrumentedAttribute, typ: _T = None, **kwargs) -> Column[_T | IdType]:
    """
    Shorthand for creating a "bound" foreign key column from a column name, the referenced column.

    "Bound" foreign keys are not nullable and cascade when referenced object is deleted. It means,
    parent deleted -> all children deleted.

    If target is a string, make sure to pass the column type at typ= (default: IdType aka varbinary(16))!
    
    *New in 0.5.0*
    """
    if isinstance(target, (Column, InstrumentedAttribute)):
        target_name = f'{target.table.name}.{target.name}'
        typ = target.type
    elif isinstance(target, str):
        target_name = target
        if typ is None:
            typ = IdType
    else:
        raise TypeError('target must be a str, a Column or a InstrumentedAttribute')

    return Column(typ, ForeignKey(target_name, ondelete='CASCADE'), nullable=False, **kwargs)


class _BitComparator(Comparator):
    """
    Comparator object for BitSelector()

    *New in 0.6.0*
    """
    _column: Column
    _flag: int
    def __init__(self, col, flag):
        self._column = col
        self._flag = flag
    def _bulk_update_tuples(self, value):
        return [ (self._column, self._upd_exp(value)) ]
    def operate(self, op, other, **kwargs):
        return op(self._sel_exp(), self._flag if other else 0, **kwargs)
    def __clause_element__(self):
        return self._column
    def __str__(self):
        return self._column
    def _sel_exp(self):
        return self._column.op('&')(self._flag)
    def _upd_exp(self, value):
        return self._column.op('|')(self._flag) if value else self._column.op('&')(~self._flag)
        
class BitSelector:
    """
    "Virtual" column representing a single bit in an integer column (usually a BigInteger).

    Mimicks peewee's 'BitField()' behavior, with SQLAlchemy.

    *New in 0.6.0*
    """
    _column: Column
    _flag: int
    _name: str
    def __init__(self, column, flag: int):
        if bin(flag := int(flag))[2:].rstrip('0') != '1':
            warnings.warn('using non-powers of 2 as flags may cause errors or undefined behavior', FutureWarning)
        self._column = column
        self._flag   = flag
    def __set_name__(self, name, owner=None):
        self._name = name
    def __get__(self, obj, objtype=None):
        if obj:
            return getattr(obj, self._column.name) & self._flag > 0
        else:
            return _BitComparator(self._column, self._flag)
    def __set__(self, obj, val):
        if obj:
            orig = getattr(obj, self._column.name)
            if val:
                orig |= self._flag
            else:
                orig &= ~(self._flag)
            setattr(obj, self._column.name, orig)
        else:
            raise NotImplementedError

