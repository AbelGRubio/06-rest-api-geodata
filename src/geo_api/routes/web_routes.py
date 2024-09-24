from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="static")


wb_router = APIRouter()


@wb_router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        "ws.html",
        {"request": request, "title": "FastAPI con Jinja2"})
