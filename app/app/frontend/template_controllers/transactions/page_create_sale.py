from fastapi import APIRouter, Form
from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from typing import Optional
from datetime import datetime

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User
from app.backend.transactions.sales import (check_for_duplicate_sale_entry, check_for_duplicate_sale_entry_by_transaction_ref,
                                            get_sales_by_customer)
from app.backend.transactions.sales_models import SaleTransaction
from app.backend.transactions.sales import add_transaction_sale

from app.backend.customer.customers import add_customer_attendance
from app.backend.customer.customer_models import Attendance

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/create-sale", response_class=HTMLResponse, include_in_schema=False)
async def transactions_html_page_resource(request: Request, current_user: User = Depends(get_current_app_user)):
    date_today = (datetime.today()).strftime('%Y-%m-%d')
    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "date_today": date_today, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("create-sale.html", context=context)


# Function to create sales transactions:
@router.post("/transactions/transaction", response_class=JSONResponse, include_in_schema=False)
async def create_sale_transaction_json_resource(current_user: User = Depends(get_current_app_user),
                                                sale_date: str = Form(...),
                                                customer_id: str = Form(...),
                                                customer_name: Optional[str] = Form(None),
                                                payment_method: str = Form(...),
                                                transaction_ref: str = Form(None),
                                                plan: str = Form(...),
                                                discount_applied: str = Form(...),
                                                amount_received: float = Form(None),
                                                are_you_sure: bool = Form(False),
                                                create_attendance_record: bool = Form(True)):
    # prevent users that are not logged in from using the api
    if not current_user:
        error = "Invalid Session. Please log back in."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # prevent read-only accounts from creating sale transactions:
    if current_user.read_only:
        error = "This account cannot create sale transactions."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # ensure are you sure was ticked:
    if not are_you_sure:
        error = "Tick that you are sure above."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # check if the customer exists first:

    # check if the sale for this day already exists to prevent duplicates:
    if payment_method == "M-Pesa":
        duplicate_check_response = check_for_duplicate_sale_entry_by_transaction_ref(customer_id=customer_id,
                                                                                     sale_date=sale_date,
                                                                                     transaction_ref=transaction_ref)
    else:

        duplicate_check_response = check_for_duplicate_sale_entry(customer_id=customer_id,
                                                                  sale_date=sale_date,
                                                                  amount_received=amount_received)
    if duplicate_check_response:
        error = "Duplicate sale entry."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # create the sale:
    # check if it was an m-pesa transaction or cash:
    if payment_method == "M-Pesa":

        if transaction_ref is not None:
            # check if the selected transaction has a sale transaction already allocated:
            pass
        else:
            error = "Payment method: M-pesa selected, but a valid transaction was not selected."
            return JSONResponse(content={"error": error, "success": False},
                                status_code=status.HTTP_400_BAD_REQUEST)

    # create the transaction:
    sale_transaction = SaleTransaction(customer_id=customer_id, customer_name=customer_name, sales_date=sale_date,
                                       discount=discount_applied, amount_received=amount_received,
                                       transaction_ref=transaction_ref,
                                       added_by=current_user.username, payment_method=payment_method, plan=plan)

    create_sale_response = add_transaction_sale(sale_transaction=sale_transaction)

    # Was create_attendance_record checked on the web-form?
    if create_attendance_record:
        attendance_record = Attendance(customer_id=customer_id, customer_name=customer_name, attendance_date=sale_date,
                                       added_by=current_user.username)
        add_customer_attendance_response = add_customer_attendance(attendance_record)

        if add_customer_attendance_response is None:
            attendance_ref = "Duplicate attendance record."
        else:
            attendance_ref = add_customer_attendance_response

        content = {"message": f"Sale transaction created successfully. Attendance Record added successfully too",
                   "doc_id": f"receipt ref {create_sale_response}, attendance ref {attendance_ref}"}
    else:

        content = {"message": "Sale transaction created successfully", "doc_id": create_sale_response}

    return JSONResponse(content=content)


# Function to get records for a customer:
@router.get("/transactions/customer/json", response_class=JSONResponse, include_in_schema=False)
async def customer_transactions_json_resource(customer_id: str, current_user: User = Depends(get_current_app_user)):
    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    # get the records for this customer:
    get_customer_transactions_response = get_sales_by_customer(customer_id=customer_id)

    # count the records:
    number_of_records = len(get_customer_transactions_response)

    content = {"transactions": get_customer_transactions_response, "number_of_records": number_of_records}

    return JSONResponse(content=content)
