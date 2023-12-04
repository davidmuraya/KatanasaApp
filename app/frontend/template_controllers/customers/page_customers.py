from fastapi import APIRouter
from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User
from app.backend.customer.customers import get_all_customers, get_all_attendance_entries
from app.backend.customer.customer_models import CustomerOverview
from app.backend.transactions.sales import get_all_sales

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


# Function to render the customers html page:
@router.get("/customers", response_class=HTMLResponse, include_in_schema=False)
async def customers_html_page_resource(request: Request, current_user: User = Depends(get_current_app_user)):

    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("customers.html", context=context)


# Function to get all customers in json:
@router.get("/customers/json", response_class=JSONResponse, include_in_schema=False)
async def customers_json_resource(current_user: User = Depends(get_current_app_user)):
    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    # get all the customers
    get_all_customers_response = get_all_customers()
    number_of_customers = len(get_all_customers_response)

    content = {"customers": get_all_customers_response, "number_of_customers": number_of_customers}

    return JSONResponse(content=content)


# Function to get list of customers and their balances for the Customers page, in json:
@router.get("/customers-overview/json", response_class=JSONResponse, include_in_schema=False)
async def customers_overview_json_resource(current_user: User = Depends(get_current_app_user)):
    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    list_of_all_customers = []

    # get all the customers:
    get_all_customers_response = get_all_customers()
    number_of_customers = len(get_all_customers_response)

    # get all the transactions or sales:
    get_all_sales_response = get_all_sales()

    # get all the attendance records:
    get_all_attendance_records_response = get_all_attendance_entries()

    # calculate the total amount received and the unearned amount, by customer:
    for customer in get_all_customers_response:

        sum_amount_received = 0.00
        # current loop customer_id:
        customer_data = customer["customer_data"]
        customer_id = customer["customer_id"]

        first_name = customer_data["first_name"]
        last_name = customer_data["last_name"]
        gender = customer_data["gender"]
        phone = customer_data["phone"]
        email = customer_data["email"]
        city = customer_data["city"]
        source = customer_data["source"]
        creation_date = customer_data["creation_date"]

        customer_overview = CustomerOverview(customer_id=customer_id, first_name=first_name, last_name=last_name,
                                             gender=gender, phone=phone, email=email, city=city, source=source,
                                             creation_date=creation_date)

        # calculating the total amount received from this customer:
        # loop through all the sales transactions:
        for transaction in get_all_sales_response:
            transaction_data = transaction["transaction_data"]

            # check if there are transactions for this customer:
            if customer_id == transaction_data["customer_id"]:
                # amount received from this customer:
                amount_received = transaction_data["amount_received"]

                # sum the amounts received from this customer:
                sum_amount_received += amount_received

        # update the customer_overview object:
        customer_overview.total_amount_received = sum_amount_received

        # calculate the unearned amount:
        sum_earned = 0.00
        for attendance in get_all_attendance_records_response:

            # check if there are attendance records for this customer:
            attendance_data = attendance["entry_data"]

            if customer_id == attendance_data["customer_id"]:
                # todo re-do this calculation properly:
                sum_earned = sum_earned + 500

        # deduct the sum earned from the total amount received and update the object:
        customer_overview.total_unearned_amount = customer_overview.total_amount_received - sum_earned

        # update the list of all customers:
        list_of_all_customers.append(customer_overview.dict())

    content = {"customers": list_of_all_customers, "number_of_customers": number_of_customers}

    return JSONResponse(content=content)
