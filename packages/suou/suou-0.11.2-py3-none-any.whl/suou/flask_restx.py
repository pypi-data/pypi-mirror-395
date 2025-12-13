"""
Utilities for Flask-RestX

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from typing import Any, Mapping
import warnings
from flask import Response, current_app, make_response
from flask_restx import Api as _Api

from .codecs import jsondecode, jsonencode, want_bytes, want_str


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body.
    
    The difference with flask_restx.representations handler of the 
    same name is suou.codecs.jsonencode() being used in place of plain json.dumps().
    
    Opinionated: some RESTX_JSON settings are ignored.
    """

    try:
        settings: dict = current_app.config.get("RESTX_JSON", {}).copy()
        settings.pop('indent', 0)
        settings.pop('separators', 0)
    except TypeError:
        warnings.warn('illegal value for RESTX_JSON', UserWarning)
        settings = {}

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = jsonencode(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp

class Api(_Api):
    """
    Improved flask_restx.Api() with better defaults.

    Notably, all JSON is whitespace-free and .message is remapped to .error
    """
    def handle_error(self, e):
        ### XXX in order for errors to get handled the correct way, import 
        ### suou.flask_restx.Api() NOT flask_restx.Api() !!!!
        res = super().handle_error(e)
        if isinstance(res, Mapping) and 'message' in res:
            res['error'] = res['message']
            del res['message']
        elif isinstance(res, Response):
            try:
                body = want_str(res.response[0])
                bodj = jsondecode(body)
                if 'message' in bodj:
                    bodj['error'] = bodj.pop('message')
                res.response = [want_bytes(jsonencode(bodj))]
            except (IndexError, KeyError):
                pass
        return res
    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)
        self.representations['application/json'] = output_json

# Optional dependency: do not import into __init__.py
__all__ = ('Api',)