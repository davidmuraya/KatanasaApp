from fastapi import APIRouter
from fastapi import status

from fastapi import FastAPI, Request, Form, Header, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from datetime import timedelta

from fastapi.templating import Jinja2Templates

import authentication

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/sign-in", response_class=HTMLResponse, include_in_schema=False)
async def sign_in_page_resource(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign-in.html", context=context)


@router.post("/sign-in", response_class=HTMLResponse, include_in_schema=False)
async def sign_in(request: Request, response: Response, email: str = Form(...), password: str = Form(...)):

    message = "Login unsuccessful"
    success = False

    # login logic
    if email == "dm@salmonbusinesssolutions.com":
        message = "Login successful"
        success = True

        access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = authentication.create_access_token(data={"sub": "dm@salmonbusinesssolutions.com"}, expires_delta=access_token_expires)

        response = RedirectResponse("/profile", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

        return response

    print("email:{}, password:{}, success:{}".format(email, password, success))
    context = {"request": request, "message": message, "success": success}

    return templates.TemplateResponse("sign-in.html", context=context)
