"""
Utilities for Snowflake-like identifiers.

Here for applications who benefit from their use. I (sakuragasaki46)
recommend using SIQ (.iding) when applicable; there also utilities to
convert snowflakes into SIQ's in .migrate.

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
from binascii import unhexlify
import os
from threading import Lock
import time
from typing import override
import warnings

from .migrate import SnowflakeSiqMigrator
from .iding import SiqType
from .codecs import b32ldecode, b32lencode, b64encode, b64decode, cb32encode, cb32decode
from .functools import deprecated


class SnowflakeGen:
    """
    Implements a generator Snowflake ID's (i.e. the ones in use at Twitter / Discord).

    Discord snowflakes are in this format:
    tttttttt tttttttt tttttttt tttttttt
    tttttttt ttddddds sssspppp pppppppp

    where:
    t: timestamp (in milliseconds) — 42 bits
    d: local ID — 5 bits
    s: shard ID — 5 bits
    p: progressive counter — 10 bits

    Converter takes local ID and shard ID as one; latter 8 bits are taken for
    the shard ID, while the former 2 are added to timestamp, taking advantage of
    more precision — along with up to 2 most significant bits of progressive co

    The constructor takes an epoch argument, since snowflakes, due to
    optimization requirements, are based on a different epoch (e.g.
    Jan 1, 2015 for Discord); epoch is wanted as seconds since Unix epoch 
    (i.e. midnight of Jan 1, 1970).
    """
    epoch: int
    local_id: int
    shard_id: int
    counter: int
    last_gen_ts: int

    TS_ACCURACY = 1000


    def __init__(self, epoch: int, local_id: int = 0, shard_id: int | None = None, 
        last_id: int = 0
    ):
        self.epoch = epoch
        self.local_id = local_id
        self.shard_id = (shard_id or os.getpid()) % 32
        self.counter = 0
        self.last_gen_ts = min(last_id >> 22, self.cur_timestamp())
    def cur_timestamp(self) -> int:
        return int((time.time() - self.epoch) * self.TS_ACCURACY)
    def generate(self, /, n: int = 1):
        """
        Generate one or more snowflakes.
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
            self.counter = 0
        while n:
            if self.counter >= 4096:
                while (now := self.cur_timestamp()) <= self.last_gen_ts:
                    time.sleep(1 / (1 << 16))
                with Lock():
                    self.counter %= 1 << 16
            # XXX the lock is here "just in case", MULTITHREADED GENERATION IS NOT ADVISED!
            with Lock():
                siq = (
                    (now << 22) | 
                    ((self.local_id % 32) << 17) |
                    ((self.shard_id % 32) << 12) |
                    (self.counter % (1 << 12))
                ) 
                n -= 1
                self.counter += 1
            yield siq
    def generate_one(self, /) -> int:
        return next(self.generate(1))
    def generate_list(self, /, n: int = 1) -> list[int]:
        return list(self.generate(n))


class Snowflake(int):
    """
    Representation of a Snowflake as an integer.
    """
    
    def to_bytes(self, length: int = 14, byteorder = "big", *, signed: bool = False) -> bytes:
        return super().to_bytes(length, byteorder, signed=signed)
    @classmethod
    def from_bytes(cls, b: bytes, byteorder = 'big', *, signed: bool = False) -> Snowflake:
        if len(b) not in (8, 10):
            warnings.warn('Snowflakes are exactly 8 bytes long', BytesWarning)
        return super().from_bytes(b, byteorder, signed=signed)
    
    def to_base64(self, length: int = 9, *, strip: bool = True) -> str:
        return b64encode(self.to_bytes(length), strip=strip)
    @classmethod
    def from_base64(cls, val:str) -> Snowflake:
        return Snowflake.from_bytes(b64decode(val))
    
    def to_cb32(self)-> str:
        return cb32encode(self.to_bytes(8, 'big'))
    to_crockford = to_cb32
    @classmethod
    def from_cb32(cls, val:str) -> Snowflake:
        return Snowflake.from_bytes(cb32decode(val))

    def to_hex(self) -> str:
        return f'{self:x}'
    @classmethod
    def from_hex(cls, val:str) -> Snowflake:
        if val.startswith('_'):
            return -cls.from_hex(val.lstrip('_'))
        return Snowflake.from_bytes(unhexlify(val))

    def to_oct(self) -> str:
        return f'{self:o}'
    @classmethod
    def from_oct(cls, val:str) -> Snowflake:
        if val.startswith('_'):
            return -cls.from_hex(val.lstrip('_'))
        return Snowflake(int(val, base=8))

    def to_b32l(self) -> str:
        # PSA Snowflake Base32 representations are padded to 10 bytes!
        if self < 0:
            return '_' + Snowflake.to_b32l(-self)
        return b32lencode(self.to_bytes(10, 'big')).lstrip('a')
    @classmethod
    def from_b32l(cls, val: str) -> Snowflake:
        if val.startswith('_'):
            ## support for negative Snowflakes
            return -cls.from_b32l(val.lstrip('_'))
        return Snowflake.from_bytes(b32ldecode(val.rjust(16, 'a')))

    def to_siq(self, domain: str, epoch: int, target_type: SiqType, **kwargs):
        """
        Convenience method for conversion to SIQ.

        (!) This does not check for existence! Always do the check yourself.
        """
        return SnowflakeSiqMigrator(domain, epoch, **kwargs).to_siq(self, target_type)

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
            case _:
                raise ValueError(f'unknown format: {opt!r}')
    
    def __str__(self) -> str:
        return int.__str__(self)
    to_dec = deprecated('use str() instead')(__str__)

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'


__all__ = (
    'Snowflake', 'SnowflakeGen'
)