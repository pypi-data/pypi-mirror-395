'''
Utilities for working with bits & handy arithmetics

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
'''

import math

def mask_shift(n: int, mask: int) -> int:
    '''
    Select the bits from n chosen by mask, least significant first.
    '''
    if mask == 0:
        return 0
    elif mask == -1:
        return n
    else:
        i = 0
        while mask & (1 << i) == 0:
            i += 1
        n >>= i
        mask >>= i
        o = 0
        while mask & (1 << o) == 1:
            o += 1
        return (n & ((1 << o) - 1)) | (mask_shift(n >> o, mask >> o) << o)

def count_ones(n: int) -> int:
    '''Count the number of one bits in a number.
    
    Negative numbers count the number of zeroes'''
    if n < 0:
        return ~count_ones(~n)
    ones = 0
    while n not in (-1, 0):
        ones += n & 1
        n >>= 1
    return ones

def split_bits(buf: bytes, nbits: int) -> list[int]:
    '''
    Split a bytestring into chunks of equal size, and interpret each chunk as an unsigned integer.
    '''
    mem = memoryview(buf)
    chunk_size = nbits // math.gcd(nbits, 8)
    est_len = math.ceil(len(buf) * 8 / nbits)
    mask_n = chunk_size * 8 // nbits
    numbers = []

    off = 0
    while off < len(buf):
        chunk = mem[off:off+chunk_size].tobytes()
        if len(chunk) < chunk_size:
            chunk = chunk + b'\0' * (chunk_size - len(chunk))
        num = int.from_bytes(chunk, 'big')
        for j in range(mask_n):
            numbers.append(mask_shift(num, ((1 << nbits) - 1) << ((mask_n - 1 - j) * nbits) ))
        off += chunk_size
    assert sum(numbers[est_len:]) == 0, str(f'{chunk_size=} {len(numbers)=} {est_len=} {numbers[est_len:]=}')
    return numbers[:est_len]


def join_bits(l: list[int], nbits: int) -> bytes:
    """
    Concatenate a list of integers into a bytestring.
    """
    chunk_size = nbits // math.gcd(nbits, 8)
    chunk = 0
    mask_n = chunk_size * 8 // nbits
    ou = b''
    
    chunk, j = 0, mask_n - 1
    for num in l:
        chunk |= num << nbits * j
        if j <= 0:
            ou += chunk.to_bytes(chunk_size, 'big')
            chunk, j = 0, mask_n - 1
        else:
            j -= 1
    else:
        if chunk != 0:
            ou += chunk.to_bytes(chunk_size, 'big')
    return ou


## arithmetics because yes

def mod_floor(x: int, y: int) -> int:
    """
    Greatest integer smaller than x and divisible by y
    """
    return x - x % y

def mod_ceil(x: int, y: int) -> int:
    """
    Smallest integer greater than x and divisible by y
    """
    return x + (y - x % y) % y


__all__ = ('count_ones', 'mask_shift', 'split_bits', 'join_bits', 'mod_floor', 'mod_ceil')
