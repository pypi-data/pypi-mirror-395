'''
Internationalization (i18n) utilities.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
'''


from __future__ import annotations

from abc import ABCMeta, abstractmethod
import json
import os
import toml
from typing import Mapping

from .exceptions import BabelTowerError

class IdentityLang:
    '''
    Bogus language, translating strings to themselves.
    '''
    def t(self, key: str, /, *args, **kwargs) -> str:
        return key.format(*args, **kwargs) if args or kwargs else key

class I18nLang:
    '''
    Single I18n language.
    '''
    _strings: dict[str, str]
    _fallback: I18nLang | IdentityLang

    def __init__(self, mapping: Mapping | None = None, /):
        self._strings = dict(mapping) if mapping else dict()
        self._fallback = IdentityLang()

    def t(self, key: str, /, *args, **kwargs) -> str:
        s = self._strings.get(key) or self._fallback.t(key)
        if args or kwargs:
            s = s.format(*args, **kwargs)
        return s

    def update(self, keys: dict[str, str], /):
        self._strings.update(keys)

    def add_fallback(self, fb: I18nLang):
        self._fallback = fb


class I18n(metaclass=ABCMeta):
    '''
    Better, object-oriented version of python-i18n.

    This is an __abstract class__! Use the appropriate subclasses in production
    (i.e. JSON, TOML) according to the file format.
    '''
    root: str
    langs: dict[str, I18nLang]
    filename_tmpl: str
    default_lang: str
    autoload: bool
    EXT: str

    @classmethod
    @abstractmethod
    def loads(cls, s: str) -> dict:
        pass

    def load_file(self, filename: str, *, root: str | None = None) -> dict:
        with open(os.path.join(root or self.root, filename)) as f:
            return self.loads(f.read())

    def load_lang(self, name: str, filename: str | None = None) -> I18nLang:
        if not filename:
            filename = self.filename_tmpl.format(lang=name, ext=self.EXT)
        try:
            data = self.load_file(filename)
        except OSError as e:
            raise BabelTowerError(f'unknown language: {name}') from e
        l = self.langs.setdefault(name, I18nLang())
        l.update(data[name] if name in data else data)
        if name != self.default_lang:
            l.add_fallback(self.lang(self.default_lang))
        return l

    def __init__(self, root: str, filename_tmpl: str = 'strings.{lang}.{ext}', *, default_lang: str = 'en', autoload: bool = True):
        self.root = root
        # XXX f before string is MISSING on PURPOSE!
        self.filename_tmpl = filename_tmpl if '{lang}' in filename_tmpl else filename_tmpl + '.{lang}.{ext}'
        self.langs = dict()
        self.default_lang = default_lang
        self.autoload = autoload

    def lang(self, name: str | None) -> I18nLang:
        if not name:
            name = self.default_lang
        if name in self.langs:
            l = self.langs[name]
        else:
            l = self.load_lang(name)
        return l
            

class JsonI18n(I18n):
    EXT = 'json'
    @classmethod
    def loads(cls, s: str) -> dict:
        return json.loads(s)

class TomlI18n(I18n):
    EXT = 'toml'
    @classmethod
    def loads(cls, s: str) -> dict:
        return toml.loads(s)


__all__ = ('I18n', 'JsonI18n', 'TomlI18n')