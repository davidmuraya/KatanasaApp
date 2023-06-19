from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from helloworld import router as hello_world_routes
from index import router as index_routes
from sign_in import router as sign_in_routes
from not_found import router as not_found_route
from profile import router as profile_route
from swagger import router as swagger_routes

app = FastAPI(docs_url=None, title="Hello World", description="This is a test application",
              redoc_url=None, version="1.0.0")
app.mount("/app", StaticFiles(directory="app"), name="app")
app.include_router(hello_world_routes)
app.include_router(index_routes)
app.include_router(sign_in_routes)
app.include_router(not_found_route)
app.include_router(profile_route)
app.include_router(swagger_routes)


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/not-found")
