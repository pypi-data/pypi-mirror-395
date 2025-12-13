"""
Helpers for asynchronous use of SQLAlchemy.

*New in 0.5.0; moved to ``sqlalchemy.asyncio`` in 0.6.0*

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

from .functools import deprecated



from .sqlalchemy.asyncio import SQLAlchemy, AsyncSelectPagination, async_query

SQLAlchemy = deprecated('import from suou.sqlalchemy.asyncio instead')(SQLAlchemy)
AsyncSelectPagination = deprecated('import from suou.sqlalchemy.asyncio instead')(AsyncSelectPagination)
async_query = deprecated('import from suou.sqlalchemy.asyncio instead')(async_query)

# Optional dependency: do not import into __init__.py
__all__ = ('SQLAlchemy', 'AsyncSelectPagination', 'async_query')