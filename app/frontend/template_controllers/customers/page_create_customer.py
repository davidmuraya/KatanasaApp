from fastapi import APIRouter
from typing import Optional

from fastapi import Request, status, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User
from app.backend.customer.customer_models import Customer
from app.backend.customer.customers import add_customer, check_for_duplicate_phone_numbers, check_for_duplicate_email
from app.backend.system.utilities import is_valid_email

from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()


router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/create-customer", response_class=HTMLResponse, include_in_schema=False)
async def create_customer_html_page_resource(request: Request, current_user: User = Depends(get_current_app_user)):

    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("create-customer.html", context=context)


@router.post("/create-customer", response_class=JSONResponse, include_in_schema=False)
async def create_customer_json_resource(current_user: User = Depends(get_current_app_user),
                                        first_name: str = Form(...),
                                        last_name: str = Form(...),
                                        phone: str = Form(...),
                                        email: Optional[str] = Form(None),
                                        city: str = Form(...),
                                        source: str = Form(...),
                                        gender: str = Form(...)):
    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    # prevent read-only accounts from creating customers:
    if current_user.read_only:
        error = "This account cannot create customers."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # check if customer exists by phone number:
    check_for_duplicate_phone_numbers_response = check_for_duplicate_phone_numbers(phone)
    if check_for_duplicate_phone_numbers_response:
        error = "Duplicate Phone Number. Customer Exists"
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # check email:
    if email is not None:
        # check if email is valid:
        check_email_is_valid_response = is_valid_email(email=email)
        if not check_email_is_valid_response:
            error = "Invalid email format!"
            return JSONResponse(content={"error": error, "success": False},
                                status_code=status.HTTP_400_BAD_REQUEST)

        # check if customer exists by email:
        check_for_duplicate_email_response = check_for_duplicate_email(email=email)
        if check_for_duplicate_email_response:
            error = "Duplicate Email. Customer Exists."
            return JSONResponse(content={"error": error, "success": False},
                                status_code=status.HTTP_400_BAD_REQUEST)

    # Create the customer:
    customer = Customer(first_name=first_name, last_name=last_name, gender=gender, source=source, city=city, phone=phone, email=email)

    create_customer_response = add_customer(customer=customer)

    message = "Customer created successfully!"
    response = JSONResponse(content={"success": True, "doc_id": create_customer_response, "message": message})

    return response
