"""
Utilities for Flask-SQLAlchemy binding.

This module is deprecated and will be REMOVED in 0.14.0.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from functools import partial
from typing import Any, Callable, Never

from flask import abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Session
from .functools import deprecated

from .codecs import want_bytes
from .sqlalchemy import AuthSrc, require_auth_base

@deprecated('inherits from deprecated and unused class')
class FlaskAuthSrc(AuthSrc):
    '''
    
    '''
    db: SQLAlchemy
    def __init__(self, db: SQLAlchemy):
        super().__init__()
        self.db = db
    def get_session(self) -> Session:
        return self.db.session
    def get_token(self):
        if request.authorization:
            return request.authorization.token
    def get_signature(self) -> bytes:
        sig = request.headers.get('authorization-signature', None)
        return want_bytes(sig) if sig else None
    def invalid_exc(self, msg: str = 'validation failed') -> Never:
        abort(400, msg)
    def required_exc(self):
        abort(401, 'Login required')

@deprecated('not intuitive to use')
def require_auth(cls: type[DeclarativeBase], db: SQLAlchemy) -> Callable[Any, Callable]:
    """
    
    """
    def auth_required(**kwargs):
        return require_auth_base(cls=cls, src=FlaskAuthSrc(db), **kwargs)

    auth_required.__doc__ = require_auth_base.__doc__

    return auth_required

# Optional dependency: do not import into __init__.py
__all__ = ()
