
from fastapi import APIRouter
from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/booking", response_class=HTMLResponse, include_in_schema=False)
async def booking_html_page_resource(request: Request):

    context = {"request": request}
    return templates.TemplateResponse("booking.html", context=context)
