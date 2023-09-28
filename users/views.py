from datetime import timedelta
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from database import get_db
from users import schemas, services
from users.authentication import (ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user, get_current_user,
                                  check_admin_user)
from users.hashing import get_password_hash

router = APIRouter(prefix='/users', tags=["users"])
roles_router = APIRouter(prefix='/roles', tags=["roles"])


# Admin users endpoints
@router.post("/register", response_model=schemas.User)
def signup(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """add new user"""
    request_data = jsonable_encoder(user_data)
    password = get_password_hash(request_data['password'])
    request_data['password'] = password
    signedup_user = services.create_user(db, request_data)
    return signedup_user


@router.get("/all/", response_model=List[schemas.User])
def get_all_users_data(current_user: Annotated[schemas.User, Depends(check_admin_user)],
                       db: Session = Depends(get_db)):
    users = services.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def get_user_data(current_user: Annotated[schemas.User, Depends(check_admin_user)], user_id: int,
                  db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, user_id)
    return user


# Logged in users endpoints
@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """add new user"""
    logged_in = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/profile/change-password/", response_model=schemas.User)
def get_user_data(request: schemas.ChangePassWord, current_user: Annotated[schemas.User, Depends(get_current_user)],
                  db: Session = Depends(get_db)):
    if authenticate_user(db, current_user.email, request.password):
        if request.new_password == request.confirm_password:
            new_password = get_password_hash(request.new_password)
            user = services.update_user_password(new_password=new_password, email=current_user.email, db=db)
        else:
            raise HTTPException(status_code=400, detail='New password and confirm password does not match')
    else:
        raise HTTPException(status_code=400, detail='Invalid old password')
    return user


@router.get("/profile/", response_model=schemas.User)
def get_user_data(current_user: Annotated[schemas.User, Depends(get_current_user)],
                  db: Session = Depends(get_db)):
    user = services.get_user_by_id(db, current_user.id)
    return user


# Admin users endpoints for roles CRUD
@roles_router.post('/', response_model=schemas.RoleOut)
def add_role(current_user: Annotated[schemas.User, Depends(check_admin_user)], role: schemas.RoleIn,
             db: Session = Depends(get_db)):
    role = jsonable_encoder(role)
    role = services.create_role(role=role, db=db)
    return role


@roles_router.get('/{role_id}/', response_model=schemas.RoleOut)
def get_role(current_user: Annotated[schemas.User, Depends(check_admin_user)], role_id: int,
             db: Session = Depends(get_db)):
    role = services.get_role_by_id(role_id=role_id, db=db)
    return role


@roles_router.get('/', response_model=List[schemas.RoleOut])
def list_role(current_user: Annotated[schemas.User, Depends(check_admin_user)],
              db: Session = Depends(get_db)):
    roles = services.get_all_roles(db=db)
    return roles
