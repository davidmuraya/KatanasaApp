from fastapi import APIRouter

from fastapi import Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home_page_resource(request: Request):
    response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
    return response

