
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from helloworld import router as hello_world_routes
from index import router as index_routes
from sign_in import router as sign_in_routes

app = FastAPI(docs_url="/documentation", title="Hello World", description="This is a test application", redoc_url=None, version="1.0.0")
app.mount("/app", StaticFiles(directory="app"), name="app")
app.include_router(hello_world_routes)
app.include_router(index_routes)
app.include_router(sign_in_routes)