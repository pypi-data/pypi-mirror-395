"""
ID (i.e. SIQ) utilities.

A SIQ is a 112-bit identifier whose bits are distributed like this:
    tttttttt tttttttt tttttttt tttttttt tttttttt uuuuuuuu uuuuuuuu
    ssssssss dddddddd dddddddd dddddddd dddddddd nnnnnnnn nnqqqqqq

    where:
    t = seconds since Jan 1, 1970, 00:00 UTC
    u = fraction seconds — accuracy down to 15 microseconds
    s = shard ID
    d = domain hash
    n = progressive number, implemented each time
    q = qualifier

Learn more: <https://yusur.moe/protocols/siq.html>

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
import base64
import binascii
import datetime
import enum
from functools import cached_property
import hashlib
from threading import Lock
import time
import os
from typing import Iterable, override
import warnings

from suou.calendar import want_timestamp

from .functools import deprecated
from .codecs import b32lencode, b64encode, cb32decode, cb32encode, want_str


class SiqType(enum.Enum):
    """
    Qualifiers for the SIQ.
    """
    # - leaves -
    # dead, non-structured content, like binary data or strings.
    # They are usually referenced from other classes.
    CONTENT     = 15  # xxx111
    # group member, array element, one-to-many
    MULTI       = 11  # xxx011
    # many-to-many relationship, hash array element
    MANYTOMANY  = 13  # xxx101
    # relationship with more than 3 foreign keys
    TERNARY     = 9   # xxx001
    # - non-leaves, may have children
    # tag for categorization or trending
    TAG         = 34  # x00010
    # anything allowing messages in it
    CHANNEL     = 42  # x01010
    #???        = 50  # x10010
    #???        = 58  # x11010
    # thread, forum post, page
    THREAD      = 22  # xx0110
    # single message or post
    MESSAGE     = 30  # xx1110
    # - non-leaves, may NOT have children
    # user account
    USER        = 32  # x00000
    # group of users (member group, role, etc)
    GROUP       = 36  # x00100
    # calendar event or task
    EVENT       = 40  # x01000
    # invite or join request
    INVITE      = 44  # x01100
    # server side application or client
    APPLICATION = 48  # x10000
    # user-created collection or algorithm-curated feed
    COLLECTION  = 52  # x10100
    # anything sold for a fee — product or subscription
    PREMIUM     = 56  # x11000
    #???        = 60  # x11100

    # - helpers -
    value: int
    @cached_property
    def n_bits(self) -> int:
        val, lsh = self.value, 0
        while val > 1:
            val, lsh = val >> 1, lsh + 1
        return lsh
    def prepend(self, other: int) -> int:
        return (other << self.n_bits) | (self.value % (1 << self.n_bits))
    @classmethod
    def from_str(cls, value) -> SiqType:
        return cls(int(value))

def make_domain_hash(domain: str, local_id: int | None = None) -> int:
    """
    Compute a domain hash for SIQ.
    If local_id ("datacenter/machine ID") is specified and nonzero, it replaces
    the leading byte with the passed value.
    Note: local_id must be nonzero and it may replace only exactly 8 bits.
    To get all of them zeroed out, pass a local_id of 256.
    """
    if not domain or domain == '0':
        return 0
    h = int.from_bytes(hashlib.sha256(domain.encode('ascii')).digest()[-4:], 'big')
    # a local_id of 256 is required to get 0.
    if local_id:
        h = ((local_id % 256) << 24) | (h % (1 << 24))
    return h

class SiqGen:
    """
    Implement a SIS-compliant SIQ generator.
    """
    __slots__ = ('domain_hash', 'last_gen_ts', 'counters', 'shard_id', '_test_cur_ts', '__weakref__')

    domain_hash: int
    last_gen_ts: int
    shard_id: int
    counters: dict[SiqType, int]
    _test_cur_timestamp: int | None

    def __init__(self, domain: str, last_siq: int = 0, local_id: int | None = None, shard_id: int | None = None):
        self.domain_hash = make_domain_hash(domain, local_id)
        self._test_cur_ts = None ## test only
        self.last_gen_ts = min(last_siq >> 56, self.cur_timestamp())
        self.counters = dict()
        self.shard_id = (shard_id or os.getpid()) % 256
    def cur_timestamp(self) -> int:
        if self._test_cur_ts is not None:
            return self._test_cur_ts
        return int(time.time() * (1 << 16))
    def set_cur_timestamp(self, value: datetime.datetime):
        """
        Intended to be used by tests only! Do not use in production!
        """
        self._test_cur_ts = int(want_timestamp(value) * 2 ** 16)
        self.last_gen_ts = int(want_timestamp(value) * 2 ** 16)
    def generate(self, /, typ: SiqType, n: int = 1) -> Iterable[int]:
        """
        Generate one or more SIQ's.
        The generated ids are returned as integers.
        Bulk generation is supported.

        Returns as an iterator, to allow generation “on the fly”.
        To get a scalar or a list, use .generate_one() or next(), or
        .generate_list() or list(.generate()), respectively.

        Warning: the function **may block**.
        """
        now = self.cur_timestamp()
        if now < self.last_gen_ts:
            time.sleep((self.last_gen_ts - now) / (1 << 16))
        elif now > self.last_gen_ts:
            self.counters[typ] = 0
        while n:
            idseq = typ.prepend(self.counters.setdefault(typ, 0))
            if idseq >= (1 << 16):
                while (now := self.cur_timestamp()) <= self.last_gen_ts:
                    time.sleep(1 / (1 << 16))
                with Lock():
                    self.counters[typ] %= 1 << (16 - typ.n_bits) 
            # XXX the lock is here "just in case", MULTITHREADED GENERATION IS NOT ADVISED!
            with Lock():
                siq = (
                    (now << 56) | 
                    ((self.shard_id % 256) << 48) |
                    ((self.domain_hash % (1 << 32)) << 16) |
                    (idseq % (1 << 16))
                ) 
                n -= 1
                self.counters[typ] += 1
            yield siq
    def generate_one(self, /, typ: SiqType) -> int:
        """
        Generate one SIQ, and return it as an integer.
        """
        return next(self.generate(typ, 1))
    def generate_list(self, /, typ: SiqType, n: int = 1) -> list[int]:
        """
        Syntactic sugar for list(.generate()).
        Return the generated SIQ's as a list.
        """
        return list(self.generate(typ, n))

class SiqFormatType(enum.Enum):
    BASE64 = 'b'
    CROCKFORD = 'c'
    DECIMAL = 'd'
    OCTAL = 'o'
    URI = 'u'
    HEX = 'x'

class SiqCache:
    """
    Caching single-type bulk ID generator.
    Useful for database settings.
    """
    __slots__ = ('generator', 'size', 'max_age', 'typ', '_cache', '__weakref__')

    generator: SiqGen
    typ: SiqType
    size: int
    max_age: int
    _cache: list[int]
    @property
    def last_gen_ts(self) -> int:
        return self.generator.last_gen_ts
    def cur_timestamp(self):
        return self.generator.cur_timestamp()
    def __init__(self, generator: SiqGen | str, typ: SiqType, size: int = 64, max_age: int = 1024):
        if isinstance(generator, str):
            generator = SiqGen(generator)
        self.generator = generator
        self.typ = typ
        self.size = size
        self.max_age = max_age
        self._cache = []
    def generate(self) -> int:
        if self.last_gen_ts + self.max_age < self.cur_timestamp():
            self._cache.clear()
        if len(self._cache) == 0:
            self._cache.extend(self.generator.generate(self.typ, self.size))
        return self._cache.pop(0)

class Siq(int):
    """
    Representation of a SIQ as an integer.
    """

    def to_bytes(self, length: int = 14, byteorder = 'big', *, signed: bool = False) -> bytes:
        return super().to_bytes(length, byteorder, signed=signed)
    @classmethod
    def from_bytes(cls, b: bytes, byteorder = 'big', *, signed: bool = False) -> Siq:
        if len(b) < 14:
            warnings.warn('trying to deserialize a bytestring shorter than 14 bytes', BytesWarning)
        return super().from_bytes(b, byteorder, signed=signed)

    def to_base64(self, length: int = 15, *, strip: bool = True) -> str:
        return b64encode(self.to_bytes(length), strip=strip)
    def to_cb32(self) -> str:
        return cb32encode(self.to_bytes(15, 'big')).lstrip('0')
    to_crockford = to_cb32
    def to_hex(self) -> str:
        return f'{self:x}'
    def to_oct(self) -> str:
        return f'{self:o}'
    def to_b32l(self) -> str:
        """
        This is NOT the URI serializer!
        """
        return b32lencode(self.to_bytes(15, 'big'))
    def __str__(self) -> str:
        return int.__str__(self)
    to_dec = deprecated('use str() instead')(__str__)
    
    @override
    def __format__(self, opt: str, /) -> str:
        try:
            return self.format(opt)
        except ValueError:
            return super().__format__(opt)
    def format(self, opt: str, /) -> str:
        match opt:
            case 'b':
                return self.to_base64()
            case 'c':
                return self.to_cb32()
            case '0c':
                return '0' + self.to_cb32()
            case 'd' | '':
                return int.__repr__(self)
            case 'l':
                return self.to_b32l()
            case 'o' | 'x':
                return int.__format__(self, opt)
            case 'u':
                b = self.to_bytes()
                cs = binascii.crc32(b).to_bytes(6, 'big', signed=False)
                return b32lencode(cs + b)[3:]
            case _:
                raise ValueError(f'unknown format: {opt!r}')

    def to_did(self) -> str:
        return f'did:siq:{self:u}'
    did = to_did
    uri = deprecated('use .did() instead')(did)
    to_uri = deprecated('shortened to .did()')(did)
    @classmethod
    def from_did(cls, did: str, /) -> Siq:
        b = base64.b32decode('AAA' + did.removeprefix('did:siq:').upper())
        cs, b = int.from_bytes(b[:6], 'big'), b[6:]
        if binascii.crc32(b) != cs:
            raise ValueError('checksum mismatch')
        return cls(int.from_bytes(b, 'big'))

    @classmethod
    def from_cb32(cls, val: str | bytes):
        return cls.from_bytes(cb32decode(want_str(val).zfill(24)))

    def to_mastodon(self, /, domain: str | None = None):
        return f'@{self:u}{"@" if domain else ""}{domain}'
    def to_matrix(self, /, domain: str):
        return f'@{self:u}:{domain}'

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    # convenience methods
    def timestamp(self):
        return (self >> 56) / (1 << 16)

    def shard_id(self):
        return (self >> 48) % 256

    def domain_name(self):
        return (self >> 16) % 0xffffffff

__all__ = (
    'Siq', 'SiqCache', 'SiqType', 'SiqGen'
)