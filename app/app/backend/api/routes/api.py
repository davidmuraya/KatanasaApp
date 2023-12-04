from fastapi import APIRouter

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

router = APIRouter()


# add the routers:
# documentation:
router.include_router(swagger_ui_routes)
router.include_router(index_routes)
router.include_router(sign_in_routes)
router.include_router(sign_out_routes)
router.include_router(create_user_routes)
router.include_router(users_routes)

# transactions
router.include_router(transaction_routes)
router.include_router(mpesa_validation_routes)
router.include_router(mpesa_confirmation_routes)
router.include_router(mpesa_transactions_routes)

router.include_router(create_customer_routes)
router.include_router(create_attendance_routes)
router.include_router(create_sale_routes)
router.include_router(get_customers_routes)
router.include_router(customers_routes)
router.include_router(dashboard_routes)
router.include_router(booking_routes)
router.include_router(page_not_found_routes)


