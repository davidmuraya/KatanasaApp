from fastapi import APIRouter

from fastapi import Request, Response, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette_session import SessionMiddleware

from fastapi.templating import Jinja2Templates
import authentication

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/profile", response_class=HTMLResponse, include_in_schema=False)
async def profile_resource(request: Request, response: Response,
                           current_user: authentication.User = Depends(authentication.get_current_app_user)):

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request}
    return templates.TemplateResponse("profile-settings.html", context=context)