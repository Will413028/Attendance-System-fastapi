from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas


def create_user(db: Session, user: schemas.UserCreateInput):
    db_user = models.User(**user.dict())

    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User create failed')
    return db_user

