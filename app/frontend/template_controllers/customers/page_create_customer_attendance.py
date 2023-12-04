
from fastapi import APIRouter
from fastapi import Request, Depends, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from datetime import datetime

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User
from app.backend.customer.customer_models import Attendance
from app.backend.customer.customers import add_customer_attendance, check_for_duplicate_attendance_entry, get_attendance_entries_by_customer

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/create-attendance", response_class=HTMLResponse, include_in_schema=False)
async def create_attendance_html_page_resource(request: Request, current_user: User = Depends(get_current_app_user)):

    date_today = (datetime.today()).strftime('%Y-%m-%d')
    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "date_today": date_today, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("create-attendance.html", context=context)


@router.post("/create-customer-attendance", response_class=JSONResponse, include_in_schema=False)
async def create_attendance_json_resource(current_user: User = Depends(get_current_app_user),
                                          attendance_date: str = Form(...),
                                          customer_id: str = Form(...),
                                          customer_name: Optional[str] = Form(None),
                                          are_you_sure: bool = Form(False)):

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    # prevent read-only accounts from creating customer attendance records:
    if current_user.read_only:
        error = "This account cannot create customer attendance records."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # ensure are you sure was ticked:
    if not are_you_sure:
        error = "Tick that you are sure above."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # check if the customer exists first:

    # check if the attendance for this day already exists to prevent duplicates:
    duplicate_check_response = check_for_duplicate_attendance_entry(customer_id=customer_id, attendance_date=attendance_date)
    if duplicate_check_response:
        error = "Duplicate customer attendance entry."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # create the attendance:
    attendance = Attendance(customer_id=customer_id, attendance_date=attendance_date,
                            added_by=current_user.username, customer_name=customer_name)

    create_attendance_response = add_customer_attendance(attendance=attendance)

    content = {"message": "Customer Attendance created successfully", "doc_id": create_attendance_response}

    return JSONResponse(content=content)


# Function to get records for a customer:
@router.get("/customers/attendance/json", response_class=JSONResponse, include_in_schema=False)
async def customers_attendance_json_resource(customer_id: str, current_user: User = Depends(get_current_app_user)):
    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    # get the records for this customer:
    get_customer_attendance_response = get_attendance_entries_by_customer(customer_id=customer_id)

    # count the records:
    number_of_records = len(get_customer_attendance_response)

    content = {"entries": get_customer_attendance_response, "number_of_records": number_of_records}

    return JSONResponse(content=content)


