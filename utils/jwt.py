from fastapi import status, Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Union
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

import service
from config import Settings
from database import get_db

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(
        data: dict, expires_delta: Union[timedelta, None] = settings.access_token_expire_minutes
):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Cookie(default=None, alias="access_token"), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        id: int = payload.get("id")

        if id is None:

            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = service.get_user_by_id(db, id)

    if user is None:
        raise credentials_exception
    return user
