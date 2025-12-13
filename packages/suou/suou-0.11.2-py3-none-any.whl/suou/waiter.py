"""
Content serving API over HTTP, based on Starlette.

*New in 0.6.0*

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""


from typing import Callable
import warnings
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Route

from suou.itertools import makelist
from suou.functools import future

@future()
class Waiter():
    _cached_app: Callable | None = None

    def __init__(self):
        self.routes: list[Route] = []
        self.production = False
        
    async def __call__(self, *args):
        return await self._build_app()(*args)
    
    def _build_app(self) -> Starlette:
        if not self._cached_app:
            self._cached_app = Starlette(
                debug = not self.production,
                routes= self.routes
            )
        return self._cached_app 

    def get(self, endpoint: str, *a, **k):
        return self._route('GET', endpoint, *a, **k)

    def post(self, endpoint: str, *a, **k):
        return self._route('POST', endpoint, *a, **k)

    def delete(self, endpoint: str, *a, **k):
        return self._route('DELETE', endpoint, *a, **k)

    def put(self, endpoint: str, *a, **k):
        return self._route('PUT', endpoint, *a, **k)

    def patch(self, endpoint: str, *a, **k):
        return self._route('PATCH', endpoint, *a, **k)

    def _route(self, methods: list[str], endpoint: str, **kwargs):
        def decorator(func):
            self.routes.append(Route(endpoint, func, methods=makelist(methods, False), **kwargs))
            return func
        return decorator

    ## TODO get, post, etc.

def ok(content = None, **ka):
    if content is None:
        return Response(status_code=204, **ka)
    elif isinstance(content, dict):
        return JSONResponse(content, **ka)
    elif isinstance(content, str):
        return PlainTextResponse(content, **ka)
    return content

def ko(status: int, /, content = None, **ka):
    if status < 400 or status > 599:
        warnings.warn(f'HTTP {status} is not an error status', UserWarning)
    if content is None:
        return Response(status_code=status, **ka)
    elif isinstance(content, dict):
        return JSONResponse(content, status_code=status, **ka)
    elif isinstance(content, str):
        return PlainTextResponse(content, status_code=status, **ka)
    return content

# This module is experimental and therefore not re-exported into __init__
__all__ = ('ko', 'ok', 'Waiter')