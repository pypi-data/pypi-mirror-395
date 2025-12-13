"""
Utilities for Flask

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

from typing import Any
from flask import Flask, abort, current_app, g, request

from suou.http import WantsContentType
from .i18n import I18n
from .configparse import ConfigOptions
from .dorks import SENSITIVE_ENDPOINTS


def add_context_from_config(app: Flask, config: ConfigOptions) -> Flask:
    '''
    Add a ConfigOptions() object's public properties into a Flask app's context
    (i.e. variables available in templates).
    '''
    @app.context_processor
    def _add_context():
        return config.to_dict()
    return app

def add_i18n(app: Flask, i18n: I18n, var_name: str = 'T', *,
        query_arg: str = 'lang', default_lang = 'en'):
    '''
    Integrate a I18n() object with a Flask application:
    - set g.lang
    - add T() to Jinja templates
    '''
    def _get_lang():
        lang = request.args.get(query_arg)
        if not lang:
            for lp in request.headers.get('accept-language', 'en').split(','):
                l = lp.split(';')[0]
                lang = l
                break
            else:
                lang = default_lang
        return lang
    
    @app.context_processor
    def _add_i18n():
        return {var_name: i18n.lang(_get_lang()).t}

    @app.before_request
    def _add_language_code():
        g.lang = _get_lang()

    return app

def get_flask_conf(key: str, default = None, *, app: Flask | None = None) -> Any:
    '''
    Get a Flask configuration value
    '''
    if not app:
        app = current_app
    return app.config.get(key, default)

def harden(app: Flask):
    """
    Make common "dork" endpoints unavailable

    XXX UNTESTED!
    """
    i = 1
    for ep in SENSITIVE_ENDPOINTS:
        @app.route(f'{ep}<path:rest>', name=f'unavailable_{i}')
        def unavailable(rest):
            abort(403)
        i += 1
    
    return app

def negotiate() -> WantsContentType:
    """
    Return an appropriate MIME type for the sake of content negotiation.
    """
    if any(request.path.startswith(f'/{p.strip('/')}/') for p in current_app.config.get('REST_PATHS', [])):
        return WantsContentType.JSON
    elif request.user_agent.string.startswith('Mozilla/'):
        return WantsContentType.HTML
    else:
        return request.accept_mimetypes.best_match([WantsContentType.PLAIN, WantsContentType.JSON, WantsContentType.HTML])


# Optional dependency: do not import into __init__.py
__all__ = ('add_context_from_config', 'add_i18n', 'get_flask_conf', 'harden', 'negotiate')


