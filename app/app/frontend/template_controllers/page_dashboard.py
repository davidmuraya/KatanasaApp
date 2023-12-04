from fastapi import APIRouter

from fastapi import Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User

from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()


router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


# Function to render the HTML page:
@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard_html_page_resource(request: Request, current_user: User = Depends(get_current_app_user)):

    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("dashboard.html", context=context)
