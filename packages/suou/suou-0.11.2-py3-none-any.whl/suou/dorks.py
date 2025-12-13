"""
Web app hardening and PT utilities.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

SENSITIVE_ENDPOINTS = """
/.git
/.gitignore
/node_modules
/wp-admin
/wp-login.php
/.ht
/package.json
/package-lock.json
/composer.
/docker-compose.
/config/
/config.
/secrets.
/credentials.
/.idea/
/.vscode/
/storage/
/logs/
/.DS_Store
/backup
/.backup
/db.sql
/database.sql
/.vite
""".split()

