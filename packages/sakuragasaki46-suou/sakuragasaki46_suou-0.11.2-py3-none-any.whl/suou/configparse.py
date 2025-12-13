"""
Utilities for parsing config variables.

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

from ast import TypeVar
from collections.abc import Mapping
from configparser import ConfigParser as _ConfigParser
import os
from typing import Any, Callable, Iterator, override
from collections import OrderedDict

from argparse import Namespace

from .classtools import ValueSource, ValueProperty
from .functools import deprecated
from .exceptions import MissingConfigError, MissingConfigWarning



_T = TypeVar('T')



class ConfigSource(ValueSource):
    '''
    Abstract config value source.
    '''
    __slots__ = ()


class EnvConfigSource(ConfigSource):
    '''
    Config source from os.environ aka .env
    '''
    def __getitem__(self, key: str, /) -> str:
        return os.environ[key]
    def get(self, key: str, fallback = None, /):
        return os.getenv(key, fallback)
    def __contains__(self, key: str, /) -> bool:
        return key in os.environ
    def __iter__(self) -> Iterator[str]:
        yield from os.environ
    def __len__(self) -> int:
        return len(os.environ)


class ConfigParserConfigSource(ConfigSource):
    '''
    Config source from ConfigParser
    '''
    __slots__ = ('_cfp', )
    _cfp: _ConfigParser

    def __init__(self, cfp: _ConfigParser):
        if not isinstance(cfp, _ConfigParser):
           raise TypeError(f'a ConfigParser object is required (got {cfp.__class__.__name__!r})')
        self._cfp = cfp
    def __getitem__(self, key: str, /) -> str:
        k1, _, k2 = key.partition('.')
        return self._cfp.get(k1, k2)
    def get(self, key: str, fallback = None, /):
        k1, _, k2 = key.partition('.')
        return self._cfp.get(k1, k2, fallback=fallback)
    def __contains__(self, key: str, /) -> bool:
        k1, _, k2 = key.partition('.')
        return self._cfp.has_option(k1, k2)
    def __iter__(self) -> Iterator[str]:
        for k1, v1 in self._cfp.items():
            for k2 in v1:
                yield f'{k1}.{k2}'
    def __len__(self) -> int:
        ## XXX might be incorrect but who cares
        return sum(len(x) for x in self._cfp)

class DictConfigSource(ConfigSource):
    '''
    Config source from Python mappings. Useful with JSON/TOML config
    '''
    __slots__ = ('_d',)

    _d: dict[str, Any]

    def __init__(self, mapping: dict[str, Any]):
        self._d = mapping
    def __getitem__(self, key: str, /) -> str:
        return self._d[key]
    def get(self, key: str, fallback: _T = None, /):
        return self._d.get(key, fallback)
    def __contains__(self, key: str, /) -> bool:
        return key in self._d
    def __iter__(self) -> Iterator[str]:
        yield from self._d
    def __len__(self) -> int:
        return len(self._d)

class ArgConfigSource(ValueSource):
    """
    Config source that assumes arguments have already been parsed.

    *New in 0.6.0*
    """
    _ns: Namespace
    def __init__(self, ns: Namespace):
        super().__init__()
        self._ns = ns
    def __getitem__(self, key):
        return getattr(self._ns, key)
    def get(self, key, value):
        return getattr(self._ns, key, value)
    def __contains__(self, key: str, /) -> bool:
        return hasattr(self._ns, key)
    @deprecated('Here for Mapping() implementation. Untested and unused')
    def __iter__(self) -> Iterator[str]:
        yield from self._ns._get_args()
    @deprecated('Here for Mapping() implementation. Untested and unused')
    def __len__(self) -> int:
        return len(self._ns._get_args())

class ConfigValue(ValueProperty):
    """
    A single config property.

    By default, it is sourced from os.environ — i.e. environment variables,
    and property name is upper cased.

    You can specify further sources, if the parent ConfigOptions class
    supports them.

    Arguments:
    - public: mark value as public, making it available across the app (e.g. in Jinja2 templates).
    - prefix: src but for the lazy
    - preserve_case: if True, src is not CAPITALIZED. Useful for parsing from Python dictionaries or ConfigParser's
    - required: throw an error if empty or not supplied
    """
    
    _preserve_case: bool = False
    _prefix: str | None = None
    _not_found = MissingConfigError

    def __init__(self, /,
            src: str | None = None, *, default = None, cast: Callable | None = None,
            required: bool = False, preserve_case: bool = False, prefix: str | None = None, 
            public: str | bool = False, **kwargs):
        self._preserve_case = preserve_case
        if src and not preserve_case:
            src = src.upper()
        if not src and prefix:
            self._prefix = prefix
            if not preserve_case:
                src = f'{prefix.upper()}?'
            else:
                src = f'{prefix}?'

        super().__init__(src, default=default, cast=cast, 
            required=required, public=public, **kwargs
        )
        
    def __set_name__(self, owner, name: str):
        src_name = name if self._preserve_case else name.upper()

        super().__set_name__(owner, name, src_name=src_name)

        if self._pub_name and isinstance(owner, ConfigOptions):
            owner.expose(self._pub_name, name)
        

    @override
    def _getter(self, obj: ConfigOptions, name: str = 'default') -> ConfigSource:
        if not isinstance(obj._srcs, Mapping):
            raise RuntimeError('attempt to get config value with no source configured')
        return obj._srcs.get(name)


class ConfigOptions:
    """
    Base class for loading config values.

    It is intended to get subclassed; config values must be defined as
    ConfigValue() properties.

    Further config sources can be added with .add_source()
    """

    __slots__ = ('_srcs', '_pub')

    _srcs: OrderedDict[str, ConfigSource]
    _pub: dict[str, str]

    def __init__(self, /):
        self._srcs = OrderedDict(
            default = EnvConfigSource()
        )
        self._pub = dict()

    def add_source(self, key: str, csrc: ConfigSource, /, *, first: bool = False):
        self._srcs[key] = csrc
        if first:
            self._srcs.move_to_end(key, False)

    add_config_source = deprecated('use add_source() instead')(add_source)

    def expose(self, public_name: str, attr_name: str | None = None) -> None:
        '''
        Mark a config value as public.

        Called automatically by ConfigValue.__set_name__().
        '''
        attr_name = attr_name or public_name
        self._pub[public_name] = attr_name
    
    def to_dict(self, /):
        d = dict()
        for k, v in self._pub.items():
            d[k] = getattr(self, v)
        return d


__all__ = (
    'MissingConfigError', 'MissingConfigWarning', 'ConfigOptions', 'EnvConfigSource', 'ConfigParserConfigSource', 'DictConfigSource', 'ConfigSource', 'ConfigValue',
    'ArgConfigSource'
)


