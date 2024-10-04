from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="static")


wb_router = APIRouter()


@wb_router.get("/ws/{id_user}", response_class=HTMLResponse)
async def read_item(request: Request, id_user: str):
    return templates.TemplateResponse(
        "ws.html",
        {"request": request, "title": "FastAPI con Jinja2",
         "id_user": id_user})


@wb_router.get("/chat/{id_user}", response_class=HTMLResponse)
async def read_item(request: Request, id_user: str):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "title": "FastAPI con Jinja2",
         "id_user": id_user})


@wb_router.get("/upload", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        "upload.html", {"request": request})

