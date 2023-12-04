from app.backend.customer.customers import get_customer_by_name, get_all_customers, add_customer
from app.backend.customer.customer_models import Customer
from app.backend.user.user_models import User
from app.backend.authentication.auth import get_current_app_user

from fastapi import APIRouter

from fastapi import Depends, Response, HTTPException, status

router = APIRouter(prefix="/api")

api_summary = "Customers"
api_description = "This API xyz"


@router.get("/customers", tags=["Customers"], summary=api_summary, description=api_description)
async def get_customer_data_resource(response: Response):
    data = get_all_customers()

    return data


@router.post("/customers/customer", tags=["Customers"], summary=api_summary, description=api_description)
async def create_customer_resource(response: Response, customer: Customer):

    doc_ref_id = add_customer(customer=customer)

    return doc_ref_id
