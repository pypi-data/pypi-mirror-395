"""
Utilities for console I/O and text user interfaces (TUI)

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
import sys
from suou.exceptions import TerminalRequiredError


def terminal_required(func):
    """
    Requires the decorated callable to be fully connected to a terminal.

    *New in 0.7.0*
    """
    @wraps(func)
    def wrapper(*a, **ka):
        if not (sys.stdin.isatty() and sys.stdout.isatty() and sys.stderr.isatty()):
            raise TerminalRequiredError('this program must be run from a terminal')
        return func(*a, **ka)
    return wrapper

__all__ = ('terminal_required',)