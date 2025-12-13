"""
Utilities for tokenization of text.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from re import Match


from dataclasses import dataclass
import re
from typing import Any, Callable, Iterable

from .exceptions import InconsistencyError, LexError

from .itertools import makelist


@dataclass
class TokenSym:
    pattern: str
    label: str
    cast: Callable[[str], Any] | None = None
    discard: bool = False

    # convenience methods below
    def match(self, s: str, index: int = 0) -> Match[str] | None:
        return re.compile(self.pattern, 0).match(s, index)

@makelist
def symbol_table(*args: Iterable[tuple | TokenSym], whitespace: str | None = None):
    """
    Make a symbol table from a list of tuples.

    Tokens are in form (pattern, label[, cast]) where:
    - [] means optional
    - pattern is a regular expression (r-string syntax advised)
    - label is a constant string
    - cast is a function 

    Need to strip whitespace? Pass the whitespace= keyword parameter.
    """
    for arg in args:
        if isinstance(arg, TokenSym):
            pass
        elif isinstance(arg, tuple):
            arg = TokenSym(*arg)
        else:
            raise TypeError(f'invalid type {arg.__class__.__name__!r}')
        yield arg
    if whitespace:
        yield TokenSym('[' + re.escape(whitespace) + ']+', '', discard=True)


symbol_table: Callable[..., list]

def ilex(text: str, table: Iterable[TokenSym], *, whitespace = False):
    """
    Return a text as a list of tokens, given a token table (iterable of TokenSym).

    ilex() returns a generator; lex() returns a list.

    table must be a result from symbol_table().
    """
    i = 0
    while i < len(text):
        mo = None
        for sym in table:
            if mo := re.compile(sym.pattern).match(text, i):
                if not sym.discard:
                    mtext = mo.group(0)
                    if callable(sym.cast):
                        mtext = sym.cast(mtext)
                    yield (sym.label, mtext)
                elif whitespace:
                    yield (None, mo.group(0))
                break
        if mo is None:
            raise LexError(f'illegal character near {text[i:i+5]!r}')
        if i == mo.end(0):
            raise InconsistencyError
        i = mo.end(0)

lex: Callable[..., list] = makelist(ilex)

__all__ = ('symbol_table', 'lex', 'ilex')