from fastapi import APIRouter

from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from app.backend.user.user_models import User
from app.backend.authentication.auth import get_current_app_user

from fastapi.templating import Jinja2Templates

from app.backend.user.users import get_all_users

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


# Function to render the HTML page:
@router.get("/users", response_class=HTMLResponse, include_in_schema=False)
async def users_page_html_resource(request: Request, current_user: User = Depends(get_current_app_user)):
    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("users.html", context=context)


# Function to get all user records:
@router.get("/users/json", response_class=JSONResponse, include_in_schema=False)
async def users_json_resource(current_user: User = Depends(get_current_app_user)):

    # prevent users that are not logged in from using the api
    if not current_user:
        error = "Invalid Session. Please log back in."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # prevent read-only accounts from viewing accounts:
    if current_user.read_only:
        error = "This account cannot view users."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # get the records for all users:
    get_users_response = get_all_users()

    # count the records:
    number_of_users = len(get_users_response)

    content = {"users": get_users_response, "number_of_users": number_of_users}

    return JSONResponse(content=content)
