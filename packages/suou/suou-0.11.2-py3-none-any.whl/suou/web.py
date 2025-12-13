"""
Utilities for web applications

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from .functools import not_implemented
from .configparse import ConfigOptions, ConfigValue

class DomainConfig(ConfigOptions):
    domain_name = ConfigValue()

domain_config = None

# lazy
def _get_domain_config():
    global domain_config
    if domain_config is None:
        domain_config = DomainConfig()
    return domain_config

def get_current_domain() -> str:
    return _get_domain_config().domain_name



