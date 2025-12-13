"""
Fortune, RNG and esoterism.

*New in 0.7.0*

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from functools import wraps
from typing import Callable, Generic, Iterable, TypeVar
import random
from suou.exceptions import BadLuckError

_T = TypeVar('_T')
_U = TypeVar('_U')


def lucky(validators: Iterable[Callable[[_U], bool]] = ()):
    """
    Add one or more constraint on a function's return value.
    Each validator must return a boolean. If false, the result is considered
    unlucky and BadLuckError() is raised.

    UNTESTED 

    *New in 0.7.0*
    """
    def decorator(func: Callable[_T, _U]) -> Callable[_T, _U]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> _U:
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                raise BadLuckError(f'exception happened: {e}') from e
            for v in validators:
                try:
                    if not v(result):
                        message = 'result not expected'
                        raise BadLuckError(f'{message}: {result!r}')
                except BadLuckError:
                    raise
                except Exception as e:
                    raise BadLuckError(f'cannot validate: {e}') from e
            return result
        return wrapper
    return decorator

class RngCallable(Callable, Generic[_T, _U]):
    """
    Overloaded ...randomly chosen callable.

    UNTESTED

    *New in 0.7.0*
    """
    def __init__(self, /, func: Callable[_T, _U] | None = None, weight: int = 1):
        self._callables = []
        self._max_weight = 0
        if callable(func):
            self.add_callable(func, weight)
    def add_callable(self, func: Callable[_T, _U], weight: int = 1):
        """
        """
        weight = int(weight)
        if weight <= 0:
            return
        self._callables.append((func, weight))
        self._max_weight += weight
    def __call__(self, *a, **ka) -> _U:
        choice = random.randrange(self._max_weight)
        for w, c in self._callables:
            if choice < w:
                return c(*a, **ka)
            elif choice < 0:
                raise RuntimeError('inconsistent state')
            else:
                choice -= w


def rng_overload(prev_func: RngCallable[..., _U] | int | None, /, *, weight: int = 1) -> RngCallable[..., _U]:
    """
    Decorate the first function with @rng_overload and the weight= parameter
    (default 1, must be an integer) to create a "RNG" overloaded callable.

    Each call chooses randomly one candidate (weight is taken in consideration),
    calls it, and returns the result.

    UNTESTED 

    *New in 0.7.0*
    """
    if isinstance(prev_func, int) and weight == 1:
        weight, prev_func = prev_func, None

    def decorator(func: Callable[_T, _U]) -> RngCallable[_T, _U]:
        nonlocal prev_func
        if prev_func is None:
            prev_func = RngCallable(func, weight=weight)
        else:
            prev_func.add_callable(func, weight=weight)
        return prev_func
    return decorator

    
# This module is experimental and therefore not re-exported into __init__
__all__ = ('lucky', 'rng_overload')