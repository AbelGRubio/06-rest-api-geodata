"""
    Definicion de los routes de la api

"""

from .v1_routes import v1_router
from .api_routes import api_router
from .streaming_routes import ws_router
from .web_routes import wb_router

__all__ = [
    v1_router,
    api_router,
    ws_router,
    wb_router
]
