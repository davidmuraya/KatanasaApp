from fastapi import APIRouter, Response, status
from typing import Optional

from fastapi import APIRouter
from pydantic.main import BaseModel

router = APIRouter()


class StatusModel(BaseModel):
    success: Optional[bool] = False
    detail: Optional[str]


apisummary = "Hello World"
apidescription = "This API displays Hello World."


@router.get("/status", response_model=StatusModel, tags=["Status"], summary=apisummary, description=apidescription)
async def status_resource(response: Response):
    status_model = StatusModel()

    response.status_code = status.HTTP_200_OK
    status_model.detail = "Hello World"
    status_model.success = True

    return _statusModel
