"""
Framework-agnostic utilities for web app development.

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
import enum

class WantsContentType(enum.Enum):
    PLAIN = 'text/plain'
    JSON = 'application/json'
    HTML = 'text/html'



__all__ = ('WantsContentType',)