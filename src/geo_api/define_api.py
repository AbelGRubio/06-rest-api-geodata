from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .auth import AuthMiddleware
from .configuration import __version__, DATABASE
from .models import ApiUser, Message
from .routes import api_router, v1_router, ws_router, wb_router

APP = FastAPI(
    title="REST API WITH EXAMPLES",
    summary="REST API WITH EXAMPLES",
    version=__version__
)

APP.mount("/static", StaticFiles(directory="static"),
          name="static")


APP.include_router(
    router=api_router,
    prefix='/api',
    tags=["Service 1: API endpoints"]
)


APP.include_router(
    router=v1_router,
    prefix='/v1',
    tags=["Service 2: v1 endpoints"]
)

APP.include_router(
    router=ws_router,
    prefix='/ws',
    tags=["Service 3: web socket"]
)

APP.include_router(
    router=wb_router,
    prefix='/wb',
    tags=["Service 4: web "]
)

# APP.add_middleware(AuthMiddleware)

DATABASE.connect()
DATABASE.create_tables([ApiUser, Message])
