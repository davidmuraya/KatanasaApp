from fastapi import APIRouter
from typing import Optional
from fastapi import Request, Depends, status, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.users import add_user

from fastapi.templating import Jinja2Templates

from app.backend.user.users import get_all_users, check_for_duplicate_username
from app.backend.user.user_models import User

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()


router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


# Function to render the HTML page:
@router.get("/create-user", response_class=HTMLResponse, include_in_schema=False)
async def create_user_page_html_resource(request: Request, current_user: User = Depends(get_current_app_user)):
    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("create-user.html", context=context)


# Function to create a user:
@router.post("/create-user", response_class=JSONResponse, include_in_schema=False)
async def create_user_json_resource(current_user: User = Depends(get_current_app_user),
                                    username: str = Form(...),
                                    password: str = Form(...),
                                    are_you_sure: bool = Form(False),
                                    read_only: bool = Form(False)):
    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    # prevent read-only accounts from creating accounts:
    if current_user.read_only:
        error = "This account cannot create users."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # ensure are you sure was ticked:
    if not are_you_sure:
        error = "Tick that you are sure above."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # check if the user already exists to prevent duplicates:
    duplicate_check_response = check_for_duplicate_username(username=username)
    if duplicate_check_response:
        error = "Duplicate username."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # create the user:
    user = User(username=username, password=password, read_only=read_only)

    create_user_response = add_user(user=user)

    content = {"message": f"User created successfully. username: {username}, password: {password}", "doc_id": create_user_response}

    return JSONResponse(content=content)
