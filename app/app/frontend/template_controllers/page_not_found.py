
from fastapi import APIRouter
from fastapi import status

from fastapi import Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/not-found", response_class=HTMLResponse, include_in_schema=False)
async def not_found_page_resource(request: Request):
    return templates.TemplateResponse("404.html", context={"request": request},
                                      status_code=status.HTTP_404_NOT_FOUND)

