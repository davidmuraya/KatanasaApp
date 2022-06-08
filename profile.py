from fastapi import APIRouter

from fastapi import Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/profile", response_class=HTMLResponse, include_in_schema=False)
async def profile_resource(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("profile-settings.html", context=context)