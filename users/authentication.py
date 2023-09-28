from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from users.hashing import verify_password
from users.schemas import TokenData
from users.services import get_user_by_email, get_user, get_role_by_name

SECRET_KEY = "9d3ed2cb6c225c88175770f3714d5cc99781fb4cb3353973d4236cfa5ed54847"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, email: str, password: str):
    if user := get_user_by_email(db=db, email=email):
        if verify_password(plain_password=password, hashed_password=user.password):
            return user
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email or password')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email or password')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    print(user)
    return user


async def check_admin_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    permission_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission not granted",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    if user.role_id != get_role_by_name(db=db, name='Admin').id:
        raise permission_exception
    return user
