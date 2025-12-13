"""
Helpers for "Glue" code, aka code meant to adapt or patch other libraries

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

import importlib
from types import ModuleType

from functools import wraps
from suou.classtools import MISSING
from suou.functools import future


@future()
class FakeModule(ModuleType):
    """
    Fake module used in @glue() in case of import error
    """
    def __init__(self, name: str, exc: Exception):
        super().__init__(name)
        self._exc = exc
    def __getattr__(self, name: str):
        raise AttributeError(f'Module {self.__name__} not found; this feature is not available ({self._exc})') from self._exc


@future()
def glue(*modules):
    """
    Helper for "glue" code -- it imports the given modules and passes them as keyword arguments to the wrapped functions.

    EXPERIMENTAL
    """
    module_dict = dict()
    imports_succeeded = True

    for module in modules:
        try:
            module_dict[module] = importlib.import_module(module)
        except Exception as e:
            imports_succeeded = False
            module_dict[module] = FakeModule(module, e)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*a, **k):
            try:
                result = func(*a, **k)
            except Exception:
                if not imports_succeeded:
                    ## XXX return an iterable? A Fake****?
                    return MISSING
                raise
            return result
        return wrapper
    return decorator

# This module is experimental and therefore not re-exported into __init__
__all__ = ('glue', 'FakeModule')