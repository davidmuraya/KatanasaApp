import logging
import time
from datetime import datetime, timedelta
from typing import Optional, List, Union

from pydantic import BaseModel

import jose
from fastapi import APIRouter, Header
from fastapi import Depends, HTTPException, status, BackgroundTasks, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

router = APIRouter()

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


class User(BaseModel):
    username: str
    password: str
    admin: bool


def get_current_app_user(access_token: str = Cookie(None)):
    if not access_token:
        return None
    else:
        scheme, _, param = access_token.partition(" ")
        try:

            payload = jwt.decode(param, SECRET_KEY, algorithms=ALGORITHM)
            username = payload.get("sub")
            user = get_user(username=username)
        except jose.ExpiredSignatureError as e:
            # print(e)
            return None

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(username: str):
    db = {"username": "dm",
          "password": "password",
          "admin": True}

    return db

