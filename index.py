

from fastapi import APIRouter
from fastapi import status

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home_page_resource(request: Request):
    data = [{"name": "Blade"},
            {"name": "Pulp"}]
    context = {"request": request, "data": data}
    return templates.TemplateResponse("index.html", context=context, status_code=status.HTTP_200_OK)
