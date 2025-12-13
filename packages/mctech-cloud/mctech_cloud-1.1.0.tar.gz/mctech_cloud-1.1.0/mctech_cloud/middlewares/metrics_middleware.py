from datetime import datetime
from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send, Message
from starlette.routing import Router, Match, Route
from typing import Optional

from mctech_core.context import get_async_context
from ..metrics import add_rpc_client_metric
from ..metrics import InvokeInfo


class MetricsMiddleware:
    _app: ASGIApp

    def __init__(self, app: ASGIApp, localHost: str, k8s: bool):
        self._localHost = localHost
        self._k8s = k8s

        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        error = None
        start = datetime.now()
        req = Request(scope)
        client_name = self._resolve_client_name(req)
        status = None

        async def send_wrapper(msg: Message):
            nonlocal status
            status = msg["status"]
            await send(msg)
        try:
            ctx = get_async_context()
            return await ctx.run(self._app, scope, receive, send_wrapper)
        except Exception as err:
            error = err
            raise err
        finally:
            router: Router = scope["app"].router
            route_match: Optional[Route] = None
            # 模拟路由匹配过程
            for route in router.routes:
                if not isinstance(route, Route):
                    continue
                match, _ = route.matches(scope)
                # Match.PARTIAL, only method not match
                if match == Match.FULL:
                    route_match = route
                    break
            if route_match:
                api_key = req.method + '::' + route_match.path
                add_rpc_client_metric(api_key, client_name, InvokeInfo(
                    start=start,
                    end=datetime.now(),
                    status=status,
                    success=error is None,
                    error=error)
                )

    def _resolve_client_name(self, req: Request):
        # 经验证，在容器中运行的时候，如果请求来自容器外部
        client_name = req.headers.get('i-rpc-client')
        if not client_name:
            client_name = req.client.host if req.client and req.headers['host'] == self._localHost and self._k8s else '<unknown>'
        req.scope['i-rpc-client'] = client_name

        product_line = req.headers.get('i-rpc-product-line')
        if not product_line:
            product_line = '<unknown>'
        req.scope['i-rpc-product-line'] = product_line
        return f"{client_name}.{product_line}"
