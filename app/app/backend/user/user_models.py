from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    read_only: Optional[bool] = True
    creation_date: Optional[str] = None

