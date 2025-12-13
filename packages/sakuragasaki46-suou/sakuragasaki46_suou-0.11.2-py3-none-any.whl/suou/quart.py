"""
Utilities for Quart, asynchronous successor of Flask

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

from quart import current_app, Quart, request, g
from quart_schema import QuartSchema

from suou.http import WantsContentType

from .i18n import I18n
from .itertools import makelist

def add_i18n(app: Quart, i18n: I18n, var_name: str = 'T', *,
        query_arg: str = 'lang', default_lang = 'en'):
    '''
    Integrate a I18n() object with a Quart application:
    - set g.lang
    - add T() to Jinja templates

    XXX UNTESTED
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


def add_rest(app: Quart, *bases: str, **kwargs) -> QuartSchema:
    """
    Construct a REST ...

    The rest of ...
    """

    schema = QuartSchema(app, **kwargs)
    app.config['REST_PATHS'] = makelist(bases, wrap=False)
    return schema


__all__ = ('add_i18n', 'negotiate', 'add_rest')