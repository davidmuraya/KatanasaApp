from datetime import datetime, timedelta

import jose
from fastapi import APIRouter
from fastapi import Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import parse_obj_as

from app.backend.user.user_models import User
from app.backend.database.firestore import users

router = APIRouter()

SECRET_KEY = "super.secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Authentication used by the HTML App:
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
        except jose.exceptions.JWTError as e:
            # Signature verification failed.
            return None

    return user


# Function to retrieve a user by username from the 'users' collection
def get_user(username: str) -> User:
    # Construct a query to find documents in the 'users' collection where the 'username' field matches the provided username
    query = users.where('username', '==', username).limit(1)

    # Execute the query and retrieve the documents
    docs = query.get()

    # Iterate through the documents (limit is set to 1, so there should be at most one document)
    for doc in docs:
        # Convert the document data to a dictionary
        doc_dict = doc.to_dict()

        # Parse the dictionary data into a User object using the parse_obj_as function
        user_obj = parse_obj_as(User, doc_dict)

        # Return the User object
        return user_obj


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
