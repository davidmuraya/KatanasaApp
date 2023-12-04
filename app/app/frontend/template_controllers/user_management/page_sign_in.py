from fastapi import APIRouter

from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.templating import Jinja2Templates
from app.backend.authentication.auth import create_access_token
from app.backend.user.users import get_user_by_username

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/sign-in", response_class=HTMLResponse, include_in_schema=False)
async def sign_in_page_html_resource(request: Request):
    environment = os.getenv("ENVIRONMENT")

    context = {"request": request, "environment": environment}

    return templates.TemplateResponse("login.html", context=context)


@router.post("/sign-in", response_class=JSONResponse, include_in_schema=False)
async def sign_in(data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user sign-in.

    Parameters:
    - data: OAuth2PasswordRequestForm containing username and password.

    Returns:
    - JSONResponse: Success response with access token and cookie set, or error response.
    """

    # form data:
    username = data.username
    password = data.password

    get_user_by_username_response = get_user_by_username(username)

    if get_user_by_username_response is not None:
        user_data = get_user_by_username_response.get("user_data")
        db_username = user_data.username
        db_password = user_data.password

        # Authenticate the user:
        if username == db_username and password == db_password:

            access_token = create_access_token(data={"sub": username})
            response = JSONResponse(content={"success": True, "path": "/dashboard"})
            response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

        else:
            error = "Credentials Error. Incorrect username or password."
            return JSONResponse(content={"error": error, "success": False},
                                status_code=status.HTTP_400_BAD_REQUEST)
    else:
        error = "Credentials Error. Invalid User."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    return response
