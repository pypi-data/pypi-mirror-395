"""
Tools for migrating to SIS and SIQ.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""


from abc import abstractmethod
from typing import override

from .functools import not_implemented
from .iding import SiqType, make_domain_hash

from .bits import mask_shift, count_ones

class SiqMigrator:
    """
    Base class for SIQ migrators.

    Every migrator has a .to_siq() function,
    taking orig_id and target_type parameters.
    """
    def __init__(self, domain: str) -> None:
        self.domain_hash = make_domain_hash(domain)

    @abstractmethod
    def to_siq(self, orig_id, target_type: SiqType) -> int:
        pass

class SnowflakeSiqMigrator(SiqMigrator):
    """
    Migrate from Snowflake ID's (i.e. the ones in use at Twitter / Discord).

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

    There should be a 1-on-1 correspondence from snowflakes and SIQs.
    """
    def __init__(self, domain: str, epoch: int, *, 
            ts_stop: int = 22, ts_accuracy: int = 1000,
            shard_mask: int = 255 << 12, shard_ts_mask: int = 3 << 20,
            serial_mask: int = 4095):
        super().__init__(domain)
        self.epoch = epoch
        self.ts_stop = ts_stop
        self.ts_accuracy = ts_accuracy
        self.shard_mask = shard_mask
        self.shard_ts_mask = shard_ts_mask
        self.serial_mask = serial_mask

    @override
    def to_siq(self, orig_id: int, target_type: SiqType) -> int:
        ts_ms = (orig_id >> self.ts_stop) + self.epoch
        ts = int(ts_ms / self.ts_accuracy * (1 << 16))
        shard = mask_shift(orig_id, self.shard_mask)
        shard_hi = 0
        if self.shard_ts_mask:
            shard_hi += mask_shift(orig_id, self.shard_ts_mask)
        ser = mask_shift(orig_id, self.serial_mask)
        ser_bits = 16 - target_type.n_bits
        orig_ser_bits = count_ones(self.serial_mask)
        if ser_bits < orig_ser_bits:
            ser, ser_hi = ser % (1 << ser_bits), ser >> ser_bits
            shard_hi <<= orig_ser_bits - ser_bits
            shard_hi += ser_hi
        ts += shard_hi
        return (
            (ts << 56)|
            ((shard % 256) << 48)|
            ((self.domain_hash % 0xffffffff)<< 16)|
            (target_type.prepend(ser) % 0xffff)
        )
        

class UlidSiqMigrator(SiqMigrator):
    '''
    Migrate from ULID's to SIQ.

    ULIDs are 128-bit identifiers with 48 timestamp bits (expressed in milliseconds) and 80 random bits.

    Structure (simplified):
    tttttttt tttttttt tttttttt tttttttt tttttttt tttttttt
    rrrrrrrr rrrrrrrr rrrrrrrr rrrrrrrr rrrrrrrr rrrrrrrr
    rrrrrrrr rrrrrrrr rrrrrrrr rrrrrrrr

    For obvious reasons, this makes 1-on-1 correspondence impossible. (Yes, the 16 spare bits.)

    It means that, of the 80 random bits, only 24 to 27 bits are preserved:
    - 6 bits summed to the timestamp.
    - 8 bits as shard ID.
    - 10 to 13 bits in the progressive counter.
    - The rest is *just discarded*.
    '''

    @override
    def to_siq(self, orig_id, target_type: SiqType) -> int:
        ts_seq   = mask_shift(orig_id, 0xfc000000000000000000)
        shard    = mask_shift(orig_id,  0x3fc0000000000000000)
        seq      = mask_shift(orig_id,    0x3fffc000000000000)

        ts = ((orig_id >> 80) << 16) // 1000 + ts_seq
        return (
            (ts << 56)|
            ((shard % 256) << 48)|
            ((self.domain_hash % 0xffffffff) << 16)|
            (((seq & ~((1 << target_type.n_bits) - 1)) | target_type.prepend(0)) % 0xffff)
        )


__all__ = (
    'SnowflakeSiqMigrator', 'UlidSiqMigrator'
)