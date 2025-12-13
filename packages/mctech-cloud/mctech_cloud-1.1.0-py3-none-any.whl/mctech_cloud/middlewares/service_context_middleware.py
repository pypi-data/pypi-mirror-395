from __future__ import absolute_import
import re
import math

from typing import Callable, Any, Dict, Mapping, ClassVar, Optional
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send
from mctech_core.context import get_async_context, WebContext, \
    header_filter as filter

__HEADER_PATTERN = re.compile('-([a-z])', re.IGNORECASE)


def try_convert_number(val: str):
    ret = int(val)
    return val if math.isnan(ret)else ret


class ServiceContextMiddleware:
    __CONVERTERS: ClassVar[Mapping[str, Callable[[str], Any]]] = {
        'x-tenant-id': try_convert_number,
        'x-user-id': try_convert_number,
        'x-id': try_convert_number,
        'x-org-id': try_convert_number
    }
    _app: ASGIApp
    _converters: Dict[str, Callable[[str], Any]]

    def __init__(self,
                 app: ASGIApp,
                 converters: Optional[Mapping[str, Callable[[str], Any]]] = None):
        self._app = app
        self._converters = dict(ServiceContextMiddleware.__CONVERTERS)
        if converters:
            self._converters.update(converters)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        headers = Headers(scope=scope)
        header_names = headers.keys()
        processingHeaders = filter.process(header_names)
        ctx = get_async_context()
        tracing = {}
        for header_name in processingHeaders['tracingHeaders']:
            tracing[header_name] = headers[header_name]
        scope['tracing'] = tracing
        ctx.tracing = tracing

        extras = {}
        for header_name in processingHeaders['extrasHeaders']:
            self._resolve_extras_value(extras, headers, header_name)
        scope['extras'] = extras
        ctx.web_context = WebContext({}, extras)

        return await ctx.run(self._app, scope, receive, send)

    def _resolve_extras_value(self, extras: dict, headers: Headers, name: str):
        key = __HEADER_PATTERN.sub(lambda m: m.group(1).upper(), name.replace('x-', ''))
        converter = self._converters.get(name)
        value = headers[name]
        if converter:
            value = converter(value)
        extras[key] = value
