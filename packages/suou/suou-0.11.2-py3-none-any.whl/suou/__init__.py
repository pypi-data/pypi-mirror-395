"""
The SUOU (SIS Unified Object Underarmor) library's entry point.

See README.md for a description.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from .iding import Siq, SiqCache, SiqType, SiqGen
from .codecs import (StringCase, cb32encode, cb32decode, b32lencode, b32ldecode, b64encode, b64decode, b2048encode, b2048decode,
    jsonencode, twocolon_list, want_bytes, want_str, ssv_list, want_urlsafe, want_urlsafe_bytes)
from .bits import count_ones, mask_shift, split_bits, join_bits, mod_ceil, mod_floor
from .calendar import want_datetime, want_isodate, want_timestamp, age_and_days
from .configparse import MissingConfigError, MissingConfigWarning, ConfigOptions, ConfigParserConfigSource, ConfigSource, DictConfigSource, ConfigValue, EnvConfigSource
from .collections import TimedDict
from .dei import dei_args
from .functools import deprecated, not_implemented, timed_cache, none_pass, alru_cache, future
from .classtools import Wanted, Incomplete
from .itertools import makelist, kwargs_prefix, ltuple, rtuple, additem, addattr
from .i18n import I18n, JsonI18n, TomlI18n
from .signing import UserSigner
from .snowflake import Snowflake, SnowflakeGen
from .lex import symbol_table, lex, ilex
from .strtools import PrefixIdentifier
from .validators import matches, not_less_than, not_greater_than, yesno
from .redact import redact_url_password
from .http import WantsContentType
from .color import chalk, WebColor

__version__ = "0.11.2"

__all__ = (
    'ConfigOptions', 'ConfigParserConfigSource', 'ConfigSource', 'ConfigValue',
    'DictConfigSource', 'EnvConfigSource', 'I18n', 'Incomplete', 'JsonI18n',
    'MissingConfigError', 'MissingConfigWarning', 'PrefixIdentifier',
    'Siq', 'SiqCache', 'SiqGen', 'SiqType', 'Snowflake', 'SnowflakeGen',
    'StringCase', 'TimedDict', 'TomlI18n', 'UserSigner', 'Wanted', 'WantsContentType',
    'WebColor',
    'addattr', 'additem', 'age_and_days', 'alru_cache', 'b2048decode', 'b2048encode',
    'b32ldecode', 'b32lencode', 'b64encode', 'b64decode', 'cb32encode',
    'cb32decode', 'chalk', 'count_ones', 'dei_args', 'deprecated',
    'future', 'ilex', 'join_bits',
    'jsonencode', 'kwargs_prefix', 'lex', 'ltuple', 'makelist', 'mask_shift',
    'matches', 'mod_ceil', 'mod_floor', 'must_be', 'none_pass', 'not_implemented',
    'not_less_than', 'not_greater_than',
    'redact_url_password', 'rtuple', 'split_bits', 'ssv_list', 'symbol_table',
    'timed_cache', 'twocolon_list', 'want_bytes', 'want_datetime', 'want_isodate',
    'want_str', 'want_timestamp', 'want_urlsafe', 'want_urlsafe_bytes', 'yesno',
    'z85encode', 'z85decode'
)
