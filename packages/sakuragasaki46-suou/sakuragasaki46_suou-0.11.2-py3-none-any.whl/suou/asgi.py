"""
ASGI stuff

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from typing import Any, Awaitable, Callable, MutableMapping, ParamSpec, Protocol


## TYPES ##

# all the following is copied from Starlette 
# available in starlette.types as of starlette==0.47.2
P = ParamSpec("P")

ASGIScope = MutableMapping[str, Any]
ASGIMessage = MutableMapping[str, Any]

ASGIReceive = Callable[[], Awaitable[ASGIMessage]]
ASGISend = Callable[[ASGIMessage], Awaitable[None]]
ASGIApp = Callable[[ASGIScope, ASGIReceive, ASGISend], Awaitable[None]]

class _MiddlewareFactory(Protocol[P]):
    def __call__(self, app: ASGIApp, /, *args: P.args, **kwargs: P.kwargs) -> ASGIApp: ... # pragma: no cover

## end TYPES ##

