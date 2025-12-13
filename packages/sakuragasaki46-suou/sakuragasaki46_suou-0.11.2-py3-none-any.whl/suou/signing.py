"""
Utilities for signing/integrity, on top of ItsDangerous.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from abc import ABC
from typing import Any, Callable, Sequence
import warnings
from itsdangerous import TimestampSigner

from itsdangerous import Signer as _Signer
from itsdangerous.encoding import int_to_bytes as _int_to_bytes

from suou.dei import dei_args
from suou.itertools import rtuple

from .functools import not_implemented
from .codecs import jsondecode, jsonencode, rb64decode, want_bytes, want_str, b64decode, b64encode
from .iding import Siq
from .classtools import MISSING

class UserSigner(TimestampSigner):
    """
    itsdangerous.TimestampSigner() instanced from a user ID, with token generation and validation capabilities.
    """
    user_id: int
    @dei_args(primary_secret='master_secret')
    def __init__(self, master_secret: bytes, user_id: int, user_secret: bytes, **kwargs):
        super().__init__(master_secret + user_secret, salt=Siq(user_id).to_bytes(), **kwargs)
        self.user_id = user_id
    def token(self, *, test_timestamp=MISSING) -> str:
        payload = Siq(self.user_id).to_base64()
        ## The following is not intended for general use
        if test_timestamp is not MISSING:
            warnings.warn('timestamp= parameter is intended for testing only!\n\x1b[31mDO NOT use it in production or you might get consequences\x1b[0m, just saying', UserWarning)
            ts_payload = b64encode(_int_to_bytes(test_timestamp))
            payload = want_bytes(payload) + want_bytes(self.sep) + want_bytes(ts_payload)
            return want_str(_Signer.sign(self, payload))
        ## END the following is not intended for general use
        
        return want_str(self.sign(payload))
    @classmethod
    def split_token(cls, /, token: str | bytes) :
        a, b, c = want_str(token).rsplit('.', 2)
        return b64decode(a), int.from_bytes(b64decode(b), 'big'), b64decode(c)
    def sign_object(self, obj: dict, /, *, encoder=jsonencode, **kwargs):
        """
        Return a signed JSON payload of an object.

        MUST be passed as a dict: ser/deser it's not the signer's job.
        """
        return self.sign(encoder(obj), **kwargs)
    def unsign_object(self, payload: str | bytes, /, *, decoder=jsondecode, **kwargs):
        """
        Unsign and parse a JSON object signed payload. Returns a dict.
        """
        return decoder(self.unsign(payload, **kwargs))
    def split_signed(self, payload: str | bytes) -> Sequence[bytes]:
        return rtuple(want_bytes(payload).rsplit(b'.', 2), 3, b'')

class HasSigner(ABC):
    '''
    Abstract base class for INTERNAL USE.
    '''
    signer: Callable[Any, UserSigner]

    @classmethod
    def __instancehook__(cls, obj) -> bool:
        return callable(getattr(obj, 'signer', None))


__all__ = ('UserSigner', )