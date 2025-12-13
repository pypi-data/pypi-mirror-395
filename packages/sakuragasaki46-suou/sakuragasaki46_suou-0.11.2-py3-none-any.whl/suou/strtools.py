"""
Utilities for string manipulation.

Why `strtools`? Why not `string`? I just~ happen to not like it

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""


from typing import Callable, Iterable
from pydantic import validate_call

from .itertools import makelist

class PrefixIdentifier:
    _prefix: str

    def __init__(self, prefix: str | None, validators: Iterable[Callable[[str], bool]] | Callable[[str], bool] | None = None):
        prefix = '' if prefix is None else prefix
        if not isinstance(prefix, str):
            raise TypeError
        validators = makelist(validators, wrap=False)
        for validator in validators:
            if not validator(prefix):
                raise ValueError('invalid prefix')
        self._prefix = prefix 
    
    @validate_call()
    def __getattr__(self, key: str):
        return f'{self._prefix}{key}'

    @validate_call()
    def __getitem__(self, key: str) -> str:
        return f'{self._prefix}{key}'

    def __str__(self):
        return f'{self._prefix}'


class SpitText:
    """
    A formatter for pre-compiled strings.

    *New in 0.11.0*
    """

    def format(self, templ: str, *attrs: Iterable[str]) -> str:
        attrs = [getattr(self, attr, f'{{{{ {attr} }}}}') for attr in attrs]
        return templ.format(*attrs).strip()


__all__ = ('PrefixIdentifier',)

