from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..configuration import DATABASE
from ..configuration import __version__

api_router = APIRouter()


@api_router.get("/health")
def health() -> JSONResponse:
    """
    Check if everything is working
    """
    status_code = 200
    return JSONResponse(
        content={'version': __version__},
        status_code=status_code
    )


@api_router.on_event("shutdown")
def close_db():
    if not DATABASE.is_closed():
        DATABASE.close()


