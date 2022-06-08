
from fastapi import APIRouter
from fastapi import status

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/sign-in", response_class=HTMLResponse)
async def sign_in_page_resource(request: Request):
    data = [{"name": "Blade"},
            {"name": "Pulp"}]
    context = {"request": request}
    return templates.TemplateResponse("sign-in.html", context=context, status_code=status.HTTP_200_OK)
