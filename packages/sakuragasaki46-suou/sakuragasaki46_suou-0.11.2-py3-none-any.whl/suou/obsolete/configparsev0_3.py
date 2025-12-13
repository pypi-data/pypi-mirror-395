"""
Utilities for parsing config variables.

BREAKING older, non-generalized version, kept for backwards compability
in case 0.4+ version happens to break.

WILL BE removed in 0.5.0.

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
from typing import Any, Callable, Iterator
from collections import OrderedDict
import warnings

from ..functools import deprecated
from ..exceptions import MissingConfigError, MissingConfigWarning

warnings.warn('This module will be removed in 0.5.0 and is kept only in case new implementation breaks!\n'\
    'Do not use unless you know what you are doing.', DeprecationWarning)

MISSING = object()
_T = TypeVar('T')


@deprecated('use configparse')
class ConfigSource(Mapping):
    '''
    Abstract config source.
    '''
    __slots__ = ()

@deprecated('use configparse')
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

@deprecated('use configparse')
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

@deprecated('use configparse')
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

@deprecated('use configparse')
class ConfigValue:
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
    # XXX disabled per https://stackoverflow.com/questions/45864273/slots-conflicts-with-a-class-variable-in-a-generic-class
    #__slots__ = ('_srcs', '_val', '_default', '_cast', '_required', '_preserve_case')

    _srcs: dict[str, str] | None
    _preserve_case: bool = False
    _val: Any | MISSING = MISSING
    _default: Any | None
    _cast: Callable | None
    _required: bool
    _pub_name: str | bool = False
    def __init__(self, /,
            src: str | None = None, *, default = None, cast: Callable | None = None,
            required: bool = False, preserve_case: bool = False, prefix: str | None = None, 
            public: str | bool = False, **kwargs):
        self._srcs = dict()
        self._preserve_case = preserve_case
        if src:
            self._srcs['default'] = src if preserve_case else src.upper()
        elif prefix:
            self._srcs['default'] = f'{prefix if preserve_case else prefix.upper}?'
        self._default = default
        self._cast = cast
        self._required = required
        self._pub_name = public
        for k, v in kwargs.items():
            if k.endswith('_src'):
                self._srcs[k[:-4]] = v
            else:
                raise TypeError(f'unknown keyword argument {k!r}')
    def __set_name__(self, owner, name: str):
        if 'default' not in self._srcs:
            self._srcs['default'] = name if self._preserve_case else name.upper() 
        elif self._srcs['default'].endswith('?'):
            self._srcs['default'] = self._srcs['default'].rstrip('?') + (name if self._preserve_case else name.upper() )
        
        if self._pub_name is True:
            self._pub_name = name
        if self._pub_name and isinstance(owner, ConfigOptions):
            owner.expose(self._pub_name, name)
    def __get__(self, obj: ConfigOptions, owner=False):
        if self._val is MISSING:
            v = MISSING
            for srckey, src in obj._srcs.items():
                if srckey in self._srcs:
                    v = src.get(self._srcs[srckey], v)
            if self._required and (not v or v is MISSING):
                raise MissingConfigError(f'required config {self._srcs['default']} not set!')
            if v is MISSING:
                v = self._default
            if callable(self._cast):
                v = self._cast(v) if v is not None else self._cast()
            self._val = v
        return self._val

    @property
    def source(self, /):
        return self._srcs['default']

@deprecated('use configparse')
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

    add_config_source = deprecated_alias(add_source)

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
    'MissingConfigError', 'MissingConfigWarning', 'ConfigOptions', 'EnvConfigSource', 'ConfigParserConfigSource', 'DictConfigSource', 'ConfigSource', 'ConfigValue'
)


