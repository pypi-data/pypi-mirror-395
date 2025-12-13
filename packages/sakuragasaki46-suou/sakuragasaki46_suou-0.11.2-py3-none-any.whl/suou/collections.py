"""
Miscellaneous iterables

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
import time
from typing import Iterator, TypeVar


_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

class TimedDict(dict[_KT, _VT]):
    """
    Dictionary where keys expire after the defined time to live, expressed in seconds.

    *New in 0.5.0*
    """
    _expires: dict[_KT, int]
    _ttl: int

    def __init__(self, ttl: int, /, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ttl = ttl
        self._expires = dict()

    def check_ex(self, key: _KT):
        if super().__contains__(key):
            ex = self._expires[key]
            now = int(time.time())
            if ex < now:
                del self._expires[key]
                super().__delitem__(key)
        elif key in self._expires:
            del self._expires[key]

    def __getitem__(self, key: _KT, /) -> _VT:
        self.check_ex(key)
        return super().__getitem__(key)

    def get(self, key: _KT, default: _VT | None = None, /) -> _VT | None:
        self.check_ex(key)
        return super().get(key)

    def __setitem__(self, key: _KT, value: _VT, /) -> None:
        self._expires = int(time.time() + self._ttl)
        super().__setitem__(key, value)
    
    def setdefault(self, key: _KT, default: _VT, /) -> _VT:
        self.check_ex(key)
        self._expires = int(time.time() + self._ttl)
        return super().setdefault(key, default)

    def __delitem__(self, key: _KT, /) -> None:
        del self._expires[key]
        super().__delitem__(key)

    def __iter__(self) -> Iterator[_KT]:
        for k in super():
            self.check_ex(k)
        return super().__iter__()

__all__ = ('TimedDict',)
