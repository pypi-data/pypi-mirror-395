"""
Class and metaclass utilities.

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

from abc import abstractmethod
from types import EllipsisType
from typing import Any, Callable, Generic, Iterable, Mapping, TypeVar
import logging

_T = TypeVar('_T')

logger = logging.getLogger(__name__)

class MissingType(object):
    __slots__ = ()
    def __bool__(self):
        return False

MISSING = MissingType()

def _not_missing(v) -> bool:
    return v and v is not MISSING

class Wanted(Generic[_T]):
    """
    Placeholder for parameters wanted by Incomplete().
    Must be passed in place of the wanted argument.
    
    May take a getter function, a string or None.
    The getter function takes the same parameters as __set_name__(), those being
    the owner class and the assigned name.
    The string is an attribute name to be sourced from the owner class.
    None is replaced with the name.

    Owner class will call .__set_name__() on the parent Incomplete instance;
    the __set_name__ parameters (owner class and name) will be passed down here.
    """
    _target: Callable | str | None | EllipsisType
    def __init__(self, getter: Callable | str | None | EllipsisType):
        self._target = getter
    def __call__(self, owner: type, name: str | None = None) -> _T | str | None:
        if self._target is None or self._target is Ellipsis:
            return name
        elif isinstance(self._target, str):
            return getattr(owner, self._target)
        elif callable(self._target):
            try:
                return self._target(owner, name)
            except TypeError:
                return self._target(owner)
        else:
            raise TypeError(f'Wanted() requires a str, callable, or None, got {self._target.__class__.__name__!r}')

class Incomplete(Generic[_T]):
    """
    functools.partial() emulation for use in class properties.
    Object is instantiated when .__set_name__() is called.

    Missing arguments must be passed in the appropriate positions
    (positional or keyword) as a Wanted() object.
    """
    _obj: Callable[..., _T]
    _args: Iterable
    _kwargs: dict
    def __init__(self, obj: Callable[..., _T] | Wanted, *args, **kwargs):
        if isinstance(obj, Wanted):
            self._obj = lambda x: x
            self._args = (obj, )
            self._kwargs = {}
        else:
            self._obj = obj
            self._args = args
            self._kwargs = kwargs
    def __set_name__(self, owner, name: str):
        args = []
        for arg in self._args:
            if isinstance(arg, Wanted):
                args.append(arg(owner, name))
            else:
                args.append(arg)
        kwargs = dict()
        for ak, av in self._kwargs.items():
            if isinstance(av, Wanted):
                kwargs[ak] = av(owner, name)
            else:
                kwargs[ak] = av
        self._args = args
        self._kwargs = kwargs

        setattr(owner, name, self.instance())
    def instance(self, /) -> _T:
        if [x for x in self._args if isinstance(x, Wanted)]:
            raise RuntimeError('trying to instance an Incomplete')
        return self._obj(*self._args, **self._kwargs)
    @classmethod
    def unfold(cls, clsdict: dict) -> dict:
        for k, v in clsdict.items():
            if isinstance(v, Incomplete):
                clsdict[k] = v.instance()
        return clsdict


## Base classes for declarative argument / option parsers below

class ValueSource(Mapping):
    """
    Abstract value source.
    """
    pass


class ValueProperty(Generic[_T]):
    _name: str | None
    _srcs: dict[str, str]
    _val: Any | MissingType
    _default: Any | None
    _cast: Callable | None
    _required: bool
    _pub_name: str | bool = False
    _not_found = LookupError

    def __init__(self, /, src: str | None = None, *,
            default = None, cast: Callable | None = None,
            required: bool = False, public: str | bool = False,
            **kwargs
        ):
        self._srcs = dict()
        if src:
            self._srcs['default'] = src
        self._default = default
        self._cast = cast
        self._required = required
        self._pub_name = public
        self._val = MISSING
        for k, v in kwargs.items():
            if k.endswith('_src'):
                self._srcs[k[:-4]] = v
            else:
                raise TypeError(f'unknown keyword argument {k!r}')
        
    def __set_name__(self, owner, name: str, *, src_name: str | None = None):
        self._name = name
        self._srcs.setdefault('default', src_name or name)
        nsrcs = dict()
        for k, v in self._srcs.items():
            if v.endswith('?'):
                nsrcs[k] = v.rstrip('?') + (src_name or name)
        self._srcs.update(nsrcs)
        if self._pub_name is True:
            self._pub_name = name
    def __get__(self, obj: Any, owner = None):
        if self._val is MISSING:
            v = MISSING
            for srckey, src in self._srcs.items():
                if (getter := self._getter(obj, srckey)):
                    v = getter.get(src, v)
                    if _not_missing(v):
                        if srckey != 'default':
                            logger.info(f'value {self._name} found in {srckey} source')
                        break
            if not _not_missing(v):
                if self._required:
                    raise self._not_found(f'required config {self._srcs['default']} not set!')
                else:
                    v = self._default
            if callable(self._cast):
                v = self._cast(v) if v is not None else self._cast()
            self._val = v
        return self._val

    @abstractmethod
    def _getter(self, obj: Any, name: str = 'default') -> ValueSource:
        pass

    @property
    def name(self):
        return self._name

    @property
    def source(self, /):
        return self._srcs['default']
    

__all__ = ('Wanted', 'Incomplete', 'ValueSource', 'ValueProperty')

