from fastapi import APIRouter, Depends

from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from app.backend.user.user_models import User
from app.backend.authentication.auth import get_current_app_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/sign-out", response_class=HTMLResponse, include_in_schema=False)
async def page_sign_out_resource(request: Request, response: Response, current_user: User = Depends(get_current_app_user)):

    logged_out_user = ""

    if current_user:
        logged_out_user = current_user.username

    # Delete cookie
    response = templates.TemplateResponse("logout.html", context={"request": request, "logged_out_user": logged_out_user})
    response.delete_cookie("access_token")

    return response
