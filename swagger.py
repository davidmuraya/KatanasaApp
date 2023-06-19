from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html

import authentication
router = APIRouter()


# Apply the authentication dependency to the route serving the Swagger UI
@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(current_user: authentication.User = Depends(authentication.get_current_app_user)):

    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API documentation",
        swagger_favicon_url="https://yourdomain.com/favicon.ico",
    )

