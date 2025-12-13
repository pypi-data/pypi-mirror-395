"""
Function utilities (decorators et al.).

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from collections import namedtuple
import math
from threading import RLock
import time
from types import CoroutineType, NoneType
from typing import Any, Callable, Iterable, Mapping, Never, TypeVar
import warnings
from functools import update_wrapper, wraps, lru_cache

from suou.itertools import hashed_list

_T = TypeVar('_T')
_U = TypeVar('_U')


def _suou_deprecated(message: str, /, *, category=DeprecationWarning, stacklevel: int = 1) -> Callable[[Callable[_T, _U]], Callable[_T, _U]]:
    """
    Backport of PEP 702 for Python <=3.12.
    The stack_level stuff is used by warnings.warn() btw
    """
    def decorator(func: Callable[_T, _U]) -> Callable[_T, _U]:
        @wraps(func)
        def wrapper(*a, **ka):
            if category is not None:
                warnings.warn(message, category, stacklevel=stacklevel)
            return func(*a, **ka)
        func.__deprecated__ = True
        wrapper.__deprecated__ = True
        return wrapper
    return decorator

try:
    from warnings import deprecated
except ImportError:
    # Python <=3.12 does not implement warnings.deprecated
    deprecated = _suou_deprecated

## this syntactic sugar for deprecated() is ... deprecated, which is ironic.
## Needed move because VSCode seems to not sense deprecated_alias()es as deprecated.
@deprecated('use deprecated(message)(func) instead')
def deprecated_alias(func: Callable[_T, _U], /, message='use .{name}() instead', *, category=DeprecationWarning) -> Callable[_T, _U]:
    """
    Syntactic sugar helper for renaming functions.

    DEPRECATED use deprecated(message)(func) instead
    """
    @deprecated(message.format(name=func.__name__), category=category)
    @wraps(func)
    def deprecated_wrapper(*a, **k) -> _U:
        return func(*a, **k)
    return deprecated_wrapper

def not_implemented(msg: Callable | str | None = None):
    """
    A more elegant way to say a method is not implemented, but may get in the future.
    """
    def decorator(func: Callable[_T, Any]) -> Callable[_T, Never]:
        da_msg = msg if isinstance(msg, str) else 'method {name}() is not implemented'.format(name=func.__name__)
        @wraps(func)
        def wrapper(*a, **k):
            raise NotImplementedError(da_msg)
        return wrapper
    if callable(msg):
        return decorator(msg)
    return decorator

def future(message: str | None = None, *, version: str = None):
    """
    Describes experimental or future API's introduced as bug fixes (including as backports)
    but not yet intended for general use (mostly to keep semver consistent).

    version= is the intended version release.

    *New in 0.7.0*
    """
    def decorator(func: Callable[_T, _U]) -> Callable[_T, _U]:
        @wraps(func)
        def wrapper(*a, **k) -> _U:
            warnings.warn(message or (
                f'{func.__name__}() is intended for release on {version} and not ready for use right now'
                if version else
                f'{func.__name__}() is intended for a future release and not ready for use right now'
            ), FutureWarning)
            return func(*a, **k)
        return wrapper
    return decorator

def flat_args(args: Iterable, kwds: Mapping, typed,
             kwd_mark = (object(),),
             fasttypes = {int, str, frozenset, NoneType},
             sorted=sorted, tuple=tuple, type=type, len=len):
    '''Turn optionally positional and keyword arguments into a hashable key for use in caches.
    
    Shamelessly copied from functools._make_key() from the Python Standard Library.
    Never trust underscores, you know.
    
    This assumes all argument types are hashable!'''
    key = args
    if kwds:
        sorted_items = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for k, v in sorted_items)
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return hashed_list(key)

def _make_alru_cache(_CacheInfo):
    def alru_cache(maxsize: int = 128, typed: bool = False):
        """
        Reimplementation of lru_cache(). In fact it's lru_cache() from Python==3.13.7 Standard
        Library with just three lines modified.

        Shamelessly adapted from the Python Standard Library with modifications.

        PSA there is no C speed up. Unlike PSL. Sorry.

        *New in 0.5.0*
        """

        # Users should only access the lru_cache through its public API:
        #       cache_info, cache_clear, and f.__wrapped__
        # The internals of the lru_cache are encapsulated for thread safety and
        # to allow the implementation to change (including a possible C version).
        # suou.alru_cache is based on pure-Python functools.lru_cache() as of Python 3.13.7.

        if isinstance(maxsize, int):
            # Negative maxsize is treated as 0
            if maxsize < 0:
                maxsize = 0
        elif callable(maxsize) and isinstance(typed, bool):
            # The user_function was passed in directly via the maxsize argument
            user_function, maxsize = maxsize, 128
            wrapper = _alru_cache_wrapper(user_function, maxsize, typed)
            wrapper.cache_parameters = lambda : {'maxsize': maxsize, 'typed': typed}
            return update_wrapper(wrapper, user_function)
        elif maxsize is not None:
            raise TypeError(
                'Expected first argument to be an integer, a callable, or None')

        def decorating_function(user_function: CoroutineType):
            wrapper = _alru_cache_wrapper(user_function, maxsize, typed)
            wrapper.cache_parameters = lambda : {'maxsize': maxsize, 'typed': typed}
            return update_wrapper(wrapper, user_function)

        return decorating_function

    def _alru_cache_wrapper(user_function, maxsize, typed):
        # Constants shared by all lru cache instances:
        sentinel = object()          # unique object used to signal cache misses
        make_key = flat_args         # build a key from the function arguments
        PREV, NEXT, KEY, RESULT = 0, 1, 2, 3   # names for the link fields

        cache = {}
        hits = misses = 0
        full = False
        cache_get = cache.get    # bound method to lookup a key or return None
        cache_len = cache.__len__  # get cache size without calling len()
        lock = RLock()           # because linkedlist updates aren't threadsafe
        root = []                # root of the circular doubly linked list
        root[:] = [root, root, None, None]     # initialize by pointing to self

        if maxsize == 0:

            async def wrapper(*args, **kwds):
                # No caching -- just a statistics update
                nonlocal misses
                misses += 1
                result = await user_function(*args, **kwds)
                return result

        elif maxsize is None:

            async def wrapper(*args, **kwds):
                # Simple caching without ordering or size limit
                nonlocal hits, misses
                key = make_key(args, kwds, typed)
                result = cache_get(key, sentinel)
                if result is not sentinel:
                    hits += 1
                    return result
                misses += 1
                result = await user_function(*args, **kwds)
                cache[key] = result
                return result

        else:

            async def wrapper(*args, **kwds):
                # Size limited caching that tracks accesses by recency
                nonlocal root, hits, misses, full
                key = make_key(args, kwds, typed)
                with lock:
                    link = cache_get(key)
                    if link is not None:
                        # Move the link to the front of the circular queue
                        link_prev, link_next, _key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last = root[PREV]
                        last[NEXT] = root[PREV] = link
                        link[PREV] = last
                        link[NEXT] = root
                        hits += 1
                        return result
                    misses += 1
                result = await user_function(*args, **kwds)
                with lock:
                    if key in cache:
                        # Getting here means that this same key was added to the
                        # cache while the lock was released.  Since the link
                        # update is already done, we need only return the
                        # computed result and update the count of misses.
                        pass
                    elif full:
                        # Use the old root to store the new key and result.
                        oldroot = root
                        oldroot[KEY] = key
                        oldroot[RESULT] = result
                        # Empty the oldest link and make it the new root.
                        # Keep a reference to the old key and old result to
                        # prevent their ref counts from going to zero during the
                        # update. That will prevent potentially arbitrary object
                        # clean-up code (i.e. __del__) from running while we're
                        # still adjusting the links.
                        root = oldroot[NEXT]
                        oldkey = root[KEY]
                        oldresult = root[RESULT]
                        root[KEY] = root[RESULT] = None
                        # Now update the cache dictionary.
                        del cache[oldkey]
                        # Save the potentially reentrant cache[key] assignment
                        # for last, after the root and links have been put in
                        # a consistent state.
                        cache[key] = oldroot
                    else:
                        # Put result in a new link at the front of the queue.
                        last = root[PREV]
                        link = [last, root, key, result]
                        last[NEXT] = root[PREV] = cache[key] = link
                        # Use the cache_len bound method instead of the len() function
                        # which could potentially be wrapped in an lru_cache itself.
                        full = (cache_len() >= maxsize)
                return result

        def cache_info():
            """Report cache statistics"""
            with lock:
                return _CacheInfo(hits, misses, maxsize, cache_len())

        def cache_clear():
            """Clear the cache and cache statistics"""
            nonlocal hits, misses, full
            with lock:
                cache.clear()
                root[:] = [root, root, None, None]
                hits = misses = 0
                full = False

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return alru_cache

alru_cache = _make_alru_cache(namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"]))
del _make_alru_cache

def timed_cache(ttl: int, maxsize: int = 128, typed: bool = False, *, async_: bool = False) -> Callable[[Callable], Callable]:
    """
    LRU cache which expires after the TTL in seconds passed as argument.

    Supports coroutines with async_=True.
    
    *New in 0.5.0*
    """
    def decorator(func: Callable[_T, _U]) -> Callable[_T, _U]:
        start_time = None

        if async_:
            @alru_cache(maxsize, typed)
            async def inner_wrapper(ttl_period: int, /, *a, **k):
                return await func(*a, **k)

            @wraps(func)
            async def wrapper(*a, **k):
                nonlocal start_time
                if not start_time:
                    start_time = int(time.time())
                return await inner_wrapper(math.floor((time.time() - start_time) // ttl), *a, **k)

            return wrapper
        else:
            @lru_cache(maxsize, typed)
            def inner_wrapper(ttl_period: int, /, *a, **k):
                return func(*a, **k)

            @wraps(func)
            def wrapper(*a, **k):
                nonlocal start_time
                if not start_time:
                    start_time = int(time.time())
                return inner_wrapper(math.floor((time.time() - start_time) // ttl), *a, **k)
            return wrapper
    return decorator

def none_pass(func: Callable[_T, _U], *args, **kwargs) -> Callable[_T, _U]:
    """
    Wrap callable so that gets called only on not None values.

    Shorthand for func(x) if x is not None else None

    *New in 0.5.0*
    """
    @wraps(func)
    def wrapper(x):
        if x is None:
            return x
        return func(x, *args, **kwargs)
    return wrapper

__all__ = (
    'deprecated', 'not_implemented', 'timed_cache', 'none_pass', 'alru_cache'
)