from __future__ import absolute_import
import os
from log4py import logging
from fastapi import FastAPI
from typing import Any, Callable, Mapping, Optional
from mctech_actuator import create_actuator_route
from mctech_discovery import get_discovery
from .service_context_middleware import ServiceContextMiddleware
from .metrics_middleware import MetricsMiddleware

log = logging.getLogger('python.cloud.middlewares')


def create_extras(app: FastAPI, converters: Optional[Mapping[str, Callable[[str], Any]]] = None):
    """创建构建extras的middleware
    """
    app.add_middleware(ServiceContextMiddleware, converters=converters)
    log.info('创建extras context middleware完成')


def create_actuator(configure, app: FastAPI):
    """创建用于Actuator服务治理相关api的router
    """

    # 设置actuator的router
    create_actuator_route(configure, app)
    log.info('创建actuator router完成')


def create_metrics(configure, app: FastAPI):
    """创建用于生成metrics统计信息的middleware
    """

    discovery = get_discovery()
    localInstance = discovery.local_instance
    localHost = f"{localInstance['ipAddr']}:{localInstance['port']}"
    k8s = os.environ.get('KUBERNETES_SERVICE_HOST', '') != ''

    app.add_middleware(MetricsMiddleware, localHost=localHost, k8s=k8s)
    log.info('创建metrics middleware完成')


__all__ = [
    "create_extras",
    "create_actuator",
    "create_metrics"
]
