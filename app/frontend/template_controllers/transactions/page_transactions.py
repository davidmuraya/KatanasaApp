
from fastapi import APIRouter
from fastapi import Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User
from app.backend.transactions.sales import get_all_sales

from dotenv import load_dotenv
import os

# Load the stored environment variables
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates/pages")


@router.get("/transactions", response_class=HTMLResponse, include_in_schema=False)
async def transactions_html_page_resource(request: Request, current_user: User = Depends(get_current_app_user)):
    environment = os.getenv("ENVIRONMENT")

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    context = {"request": request, "environment": environment, "username": current_user.username}
    return templates.TemplateResponse("transactions.html", context=context)


# Function to get all sales records:
@router.get("/transactions/customers/json", response_class=JSONResponse, include_in_schema=False)
async def customers_transactions_json_resource(current_user: User = Depends(get_current_app_user)):

    if not current_user:
        error = "Invalid Session. Please log back in."
        return JSONResponse(content={"error": error, "success": False},
                            status_code=status.HTTP_400_BAD_REQUEST)

    # get the records for all sales:
    get_transactions_response = get_all_sales()

    # count the records:
    number_of_records = len(get_transactions_response)

    content = {"transactions": get_transactions_response, "number_of_records": number_of_records}

    return JSONResponse(content=content)
