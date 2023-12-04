from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from app.backend.authentication.auth import get_current_app_user
from app.backend.user.user_models import User

router = APIRouter()


@router.get("/api-documentation", include_in_schema=False)
async def custom_swagger_ui_html(current_user: User = Depends(get_current_app_user)):
    if not current_user:
        response = RedirectResponse("/sign-in", status_code=status.HTTP_302_FOUND)
        return response

    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Katanasa",
        swagger_favicon_url="/frontend/static/favicon.ico",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )
