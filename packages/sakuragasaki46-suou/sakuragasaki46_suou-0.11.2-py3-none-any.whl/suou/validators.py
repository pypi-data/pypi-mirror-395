"""
Miscellaneous validator closures.

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

from typing import Any, Iterable, TypeVar

from suou.classtools import MISSING

_T = TypeVar('_T')

def matches(regex: str | int, /, length: int = 0, *, flags=0):
    """
    Return a function which returns True if X is shorter than length and matches the given regex.
    """
    if isinstance(regex, int):
        length = regex
        regex = '.*'
    def validator(s: str):
        return (not length or len(s) < length) and bool(re.fullmatch(regex, s, flags=flags))
    return validator


def must_be(obj: _T | Any, typ: type[_T] | Iterable[type], message: str, *, exc = TypeError) -> _T:
    """
    Raise TypeError if the requested object is not of the desired type(s), with a nice message.

    (Not properly a validator.)
    """
    if not isinstance(obj, typ):
        raise TypeError(f'{message}, not {obj.__class__.__name__!r}')
    return obj


def not_greater_than(y):
    """
    Return a function that returns True if X is not greater than (i.e. lesser than or equal to) the given value.
    """
    return lambda x: x <= y

def not_less_than(y):
    """
    Return a function that returns True if X is not less than (i.e. greater than or equal to) the given value.
    """
    return lambda x: x >= y

def yesno(x: str | int | bool | None) -> bool:
    """
    Returns False if x.lower() is in '0', '', 'no', 'n', 'false' or 'off'.

    *New in 0.9.0*

    *Changed in 0.11.1*: now accepts None and bool.
    """
    if x in (None, MISSING):
        return False
    if isinstance(x, bool):
        return x
    if isinstance(x, int):
        return x != 0
    if isinstance(x, str):
        return x.lower() not in ('', '0', 'off', 'n', 'no', 'false', 'f')
    return True
    

__all__ = ('matches', 'must_be', 'not_greater_than', 'not_less_than', 'yesno')

