from fastapi import APIRouter
from fastapi import status

from fastapi import FastAPI, Request, Form, Header
from fastapi.responses import HTMLResponse
from typing import Optional

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/sign-in", response_class=HTMLResponse, include_in_schema=False)
async def sign_in_page_resource(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("sign-in.html", context=context)


@router.post("/sign-in", response_class=HTMLResponse, include_in_schema=False)
async def sign_in(request: Request, email: str = Form(...), password: str = Form(...), hx_request: Optional[str] = Header(None)):

    message = "Login unsuccessful"
    success = False

    if email == "dm@salmonbusinesssolutions.com":
        message = "Login successful"
        success = True

    print("email:{}, password:{}, success:{}".format(email, password, success))
    context = {"request": request, "message": message, "success": success}

    return templates.TemplateResponse("sign-in.html", context=context)
