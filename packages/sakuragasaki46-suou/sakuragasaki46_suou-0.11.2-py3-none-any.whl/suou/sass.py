"""

"""


import datetime
import logging
import os
from typing import Callable, Mapping
from sass import CompileError
from sassutils.builder import Manifest
from importlib.metadata import version as _get_version

from .codecs import quote_css_string, want_bytes, want_bytes
from .validators import must_be
from .asgi import _MiddlewareFactory, ASGIApp, ASGIReceive, ASGIScope, ASGISend
from . import __version__ as _suou_version

from pkg_resources import resource_filename

logger = logging.getLogger(__name__)

## NOTE Python/PSF recommends use of importlib.metadata for version checks.
_libsass_version = _get_version('libsass')

class SassAsyncMiddleware(_MiddlewareFactory):
    """
    ASGI middleware for development purpose.
    Every time a CSS file has requested it finds a matched
    Sass/SCSS source file andm then compiled it into CSS.
    
    Eventual syntax errors are displayed in three ways:
    - heading CSS comment (i.e. `/* Error: invalid pro*/`) 
    - **red text** in `body::before` (in most cases very evident, since every other
      style fails to render!)
    - server-side logging (level is *error*, remember to enable logging!)
    
    app = ASGI application to wrap
    manifests = a Mapping of build settings, see sass_manifests= option 
    in `setup.py`

    Shamelessly adapted from libsass==0.23.0 with modifications

    XXX experimental and untested!
    """

    def __init__(
        self, app: ASGIApp, manifests: Mapping, package_dir = {},
        error_status = '200 OK'
    ):
        self.app = must_be(app, Callable, 'app must be a ASGI-compliant callable')
        self.manifests = Manifest.normalize_manifests(manifests)
        self.package_dir = dict(must_be(package_dir, Mapping, 'package_dir must be a mapping'))
        ## ???
        self.error_status = error_status
        for package_name in self.manifests:
            if package_name in self.package_dir:
                continue
            self.package_dir[package_name] = resource_filename(package_name, '')
        self.paths: list[tuple[str, str, Manifest]] = []
        for pkgname, manifest in self.manifests.items():
            ## WSGI path — is it valid for ASGI as well??
            asgi_path = f'/{manifest.wsgi_path.strip('/')}/'
            pkg_dir = self.package_dir[pkgname]
            self.paths.append((asgi_path, pkg_dir, manifest))
    
    async def __call__(self, /, scope: ASGIScope, receive: ASGIReceive, send: ASGISend):
        path: str = scope.get('path')
        if path.endswith('.css'):
            for prefix, package_dir, manifest in self.paths:
                if not path.startswith(prefix):
                    continue
                css_filename = path[len(prefix):]
                sass_filename = manifest.unresolve_filename(package_dir, css_filename)
                try:
                    ## TODO consider async??
                    result = manifest.build_one(
                        package_dir,
                        sass_filename,
                        source_map=True
                    )
                except OSError:
                    break
                except CompileError as e:
                    logger.error(str(e))
                    resp_body = '\n'.join([
                        '/*',
                        str(e),
                        '***',
                        f'libsass {_libsass_version} + suou {_suou_version} {datetime.datetime.now().isoformat()}',
                        '*/',
                        '',
                        'body::before {',
                        f'  content: {quote_css_string(str(e))};',
                        '  color: maroon;',
                        '  background-color: white;',
                        '  white-space: pre-wrap;',
                        '  display: block;',
                        '  font-family: monospace;',
                        '  user-select: text;'
                        '}'
                    ]).encode('utf-8')

                    await send({
                        'type': 'http.response.start',
                        'status': self.error_status,
                        'headers': [
                            (b'Content-Type', b'text/css; charset=utf-8'),
                            (b'Content-Length', want_bytes(f'{len(resp_body)}'))
                        ]
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': resp_body
                    })

                    return

                async def _read_file(path):
                    with open(path, 'rb') as f:
                        while True:
                            chunk = f.read(4096)
                            if chunk:
                                yield chunk
                            else:
                                break
                
                file_path = os.path.join(package_dir, result)

                await send({
                    'type': 'http.response.start',
                    'status': 200,
                    'headers': [
                        (b'Content-Type', b'text/css; charset=utf-8'),
                        (b'Content-Length', want_bytes(f'{os.path.getsize(file_path)}'))
                    ]
                })

                resp_body = b''
                async for chunk in _read_file(file_path):
                    resp_body += chunk
                    
                await send({
                    'type': 'http.response.body',
                    'body': resp_body
                })

                return

        await self.app(scope, receive, send)
        

