
from fastapi import FastAPI

from helloworld import router as helloworldroutes

app = FastAPI(docs_url="/", title="Hello World",
              description= "This is a test application", redoc_url=None, version="1.0.0")
app.include_router(helloworldroutes)