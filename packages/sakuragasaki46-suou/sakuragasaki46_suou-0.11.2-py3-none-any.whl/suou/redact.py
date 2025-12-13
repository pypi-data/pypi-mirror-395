"""
"Security through obscurity" helpers for less sensitive logging

*New in 0.5.0*

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import re


def redact_url_password(u: str) -> str:
    """
    Remove password from URIs.

    The password part in URIs is:
    scheme://username:password@hostname/path?query
                      ^------^

    *New in 0.5.0*
    """
    return re.sub(r':[^@:/ ]+@', ':***@', u)


__all__ = ('redact_url_password', )