"""
Utilities for Diversity, Equity, Inclusion.

This implements a cool compact representation for pronouns, inspired by the one in use at <https://pronoundb.org/>

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
from functools import wraps
from typing import Callable, TypeVar

_T = TypeVar('_T')
_U = TypeVar('_U')


BRICKS = '@abcdefghijklmnopqrstuvwxyz+?-\'/'
"""
Legend:
a through z, ' (apostrophe) and - (hyphen/dash) mean what they mean.
? is an unknown symbol or non-ASCII/non-alphabetic character.
+ is a suffix separator (like / but allows for a more compact notation).
/ is the separator.

Except for the presets (see Pronoun.PRESETS below), pronouns expand to the
given notation: e.g. ae+r is ae/aer.
"""

class Pronoun(int):
    """
    Implementation of pronouns in a compact style.
    A pronoun is first normalized, then furtherly compressed by turning it
    into an integer (see Pronoun.from_short()).

    Subclass of int, ideal for databases. Short form is recommended in
    transfer (e.g. if writing a REST).
    """
    PRESETS = {
        'hh': 'he/him',
        'sh': 'she/her',
        'tt': 'they/them',
        'ii': 'it/its',
        'hs': 'he/she',
        'ht': 'he/they',
        'hi': 'he/it',
        'shh': 'she/he',
        'st': 'she/they',
        'si': 'she/it',
        'th': 'they/he',
        'ts': 'they/she',
        'ti': 'they/it',
    }

    UNSPECIFIED = 0

    ## presets from PronounDB
    ## DO NOT TOUCH the values unless you know their exact correspondence!!
    ## hint: Pronoun.from_short()
    HE = HE_HIM = 264
    SHE = SHE_HER = 275
    THEY = THEY_THEM = 660
    IT = IT_ITS = 297
    HE_SHE = 616
    HE_THEY = 648
    HE_IT = 296
    SHE_HE = 8467
    SHE_THEY = 657
    SHE_IT = 307
    THEY_HE = 276
    THEY_SHE = 628
    THEY_IT = 308
    ANY = 26049
    OTHER = 19047055
    ASK = 11873
    AVOID = NAME_ONLY = 4505281

    def short(self) -> str:
        i = self
        s = ''
        while i > 0:
            s += BRICKS[i % 32]
            i >>= 5
        return s
    
    def full(self):
        s = self.short()

        if s in self.PRESETS:
            return self.PRESETS[s]
        
        if '+' in s:
            s1, s2 = s.rsplit('+')
            s = s1 + '/' + s1 + s2

        return s
    __str__ = full

    @classmethod
    def from_short(self, s: str) -> Pronoun:
        i = 0
        for j, ch in enumerate(s):
            i += BRICKS.index(ch) << (5 * j)
        return Pronoun(i)



def dei_args(**renames):
    """
    Allow for aliases in the keyword argument names, in form alias='real_name'.

    DEI utility for those programmers who don't want to have to do with
    potentially offensive variable naming.

    Dear conservatives, this does not influence the ability to call the wrapped function
    with the original parameter names.
    """
    def decorator(func: Callable[_T, _U]) -> Callable[_T, _U]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for alias_name, actual_name in renames.items():
                if alias_name in kwargs:
                    val = kwargs.pop(alias_name)
                    kwargs[actual_name] = val
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


