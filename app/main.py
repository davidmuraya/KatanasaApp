
import uvicorn

from fastapi.staticfiles import StaticFiles

from app.backend.http_utils.http_client import on_start_up, on_shutdown

# HTML App:
from app.frontend.template_controllers.page_index import router as index_routes
from app.frontend.template_controllers.page_not_found import router as page_not_found_routes

# Users
from app.frontend.template_controllers.user_management.page_sign_in import router as sign_in_routes
from app.frontend.template_controllers.user_management.page_sign_out import router as sign_out_routes
from app.frontend.template_controllers.user_management.page_users import router as users_routes
from app.frontend.template_controllers.user_management.page_create_user import router as create_user_routes

# Transactions
from app.frontend.template_controllers.transactions.page_transactions import router as transaction_routes
from app.frontend.template_controllers.transactions.page_create_sale import router as create_sale_routes
from app.frontend.template_controllers.customers.page_create_customer import router as create_customer_routes
from app.frontend.template_controllers.customers.page_customers import router as customers_routes
from app.frontend.template_controllers.transactions.page_mpesa_transactions import router as mpesa_transactions_routes

# #M-pesa
from app.backend.transactions.mpesa.mpesa_confirmation_routes import router as mpesa_confirmation_routes
from app.backend.transactions.mpesa.mpesa_validation_routes import router as mpesa_validation_routes

# Customers
from app.frontend.template_controllers.customers.page_create_customer_attendance import router as create_attendance_routes
from app.frontend.template_controllers.customers.page_booking import router as booking_routes
from app.frontend.template_controllers.page_dashboard import router as dashboard_routes
from app.frontend.swagger.swagger_ui import router as swagger_ui_routes


# APIs
from app.backend.customer.customer_routes import router as get_customers_routes


from fastapi import FastAPI


api_description = """
Katanasa.
Application to monitor clients payments.
To include M-Pesa payments in future.
"""

app = FastAPI(docs_url=None, on_startup=[on_start_up], on_shutdown=[on_shutdown], title="Katanasa App",
              description=api_description, version="23.11.22", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

# Mount the folders: Add your files when creating jinja2 templates
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static",)


# add the routers:
# documentation:
app.include_router(swagger_ui_routes)
app.include_router(index_routes)
app.include_router(sign_in_routes)
app.include_router(sign_out_routes)
app.include_router(create_user_routes)
app.include_router(users_routes)

# transactions
app.include_router(transaction_routes)
app.include_router(mpesa_validation_routes)
app.include_router(mpesa_confirmation_routes)
app.include_router(mpesa_transactions_routes)

app.include_router(create_customer_routes)
app.include_router(create_attendance_routes)
app.include_router(create_sale_routes)
app.include_router(get_customers_routes)
app.include_router(customers_routes)
app.include_router(dashboard_routes)
app.include_router(booking_routes)
app.include_router(page_not_found_routes)


# Page not found exception handler
# @app.exception_handler(404)
# async def custom_404_handler(_, __):
#     return RedirectResponse("app/not-found")


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000)
