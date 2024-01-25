from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import models, schemas, utils, service
from database import get_db


def check_new_user(user: schemas.UserCreateInput, db: Session = Depends(get_db)) -> tuple[schemas.UserCreateInput, Session]:
    db_user = service.get_user_by_account(db, user.account)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

    return user, db


def authenticate_user(data: schemas.LoginInput, db: Session = Depends(get_db)) -> models.User:
    db_user = service.get_user_by_account(db, data.account)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not utils.verify_password(data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password or email')
    return db_user
