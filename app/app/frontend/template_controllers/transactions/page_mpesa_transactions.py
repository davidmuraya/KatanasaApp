
from fastapi import APIRouter
from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User
from app.backend.transactions.sales import get_all_m_pesa_transactions, get_all_m_pesa_transactions_by_date

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/m-pesa-transactions", response_class=HTMLResponse, include_in_schema=False)
async def mpesa_html_page_resource(request: Request, current_user: User = Depends(get_current_app_user)):
    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("m-pesa-transactions.html", context=context)


# Function to get all sales records:
@router.get("/m-pesa-transactions/json", response_class=JSONResponse, include_in_schema=False)
async def mpesa_transactions_json_resource(current_user: User = Depends(get_current_app_user)):

    if not current_user:
        error = "Invalid Session. Please log back in."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # get the records for all mpesa transactions:
    get_transactions_response = get_all_m_pesa_transactions()

    # count the records:
    number_of_records = len(get_transactions_response)

    content = {"transactions": get_transactions_response, "number_of_records": number_of_records}

    return JSONResponse(content=content)


# Function to get all sales records by date:
@router.get("/m-pesa-transactions/{transaction_date}/json", response_class=JSONResponse, include_in_schema=False)
async def mpesa_transactions_by_date_json_resource(transaction_date: str, current_user: User = Depends(get_current_app_user)):

    if not current_user:
        error = "Invalid Session. Please log back in."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # get the records for all mpesa transactions:
    get_transactions_by_date_response = get_all_m_pesa_transactions_by_date(transaction_date=transaction_date)

    # count the records:
    number_of_records = len(get_transactions_by_date_response)

    content = {"transactions": get_transactions_by_date_response, "number_of_records": number_of_records}

    return JSONResponse(content=content)
