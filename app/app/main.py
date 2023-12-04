
import uvicorn

from fastapi.staticfiles import StaticFiles

from app.backend.http_utils.http_client import on_start_up, on_shutdown
from app.backend.api.routes.api import router as api_router


from fastapi import FastAPI


api_description = """
Katanasa.
Application to monitor clients payments.
"""

app = FastAPI(docs_url=None, on_startup=[on_start_up], on_shutdown=[on_shutdown], title="Katanasa App",
              description=api_description, version="23.12.04", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

# Mount the folders: Add your files when creating jinja2 templates
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static",)
app.include_router(api_router)

# Page not found exception handler
# @app.exception_handler(404)
# async def custom_404_handler(_, __):
#     return RedirectResponse("app/not-found")


if __name__ == '__main__':
    uvicorn.run("main:app", port=5000)
