from fastapi import FastAPI

from .auth import AuthMiddleware
from .configuration import __version__, DATABASE
from .routes import api_router, v1_router
from .models import ApiUser

APP = FastAPI(
    title="API Geo data",
    summary="API Geo data",
    version=__version__
)


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

# APP.add_middleware(AuthMiddleware)

DATABASE.connect()
DATABASE.create_tables([ApiUser])
