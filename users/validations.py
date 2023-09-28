from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from users import schemas, services


def validate_email(db: Session, user_data: schemas.UserCreate):
    if services.get_user_by_email(db=db, email=user_data['email']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email already exists')
