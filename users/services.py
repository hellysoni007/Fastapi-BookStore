import json

from sqlalchemy.orm import Session

from users import schemas, models
from users.validations import validate_email


def create_user(db: Session, user_data: schemas.UserCreate):
    validate_email(db=db, user_data=user_data)
    user = models.User(last_name=user_data['last_name'], first_name=user_data['first_name'], email=user_data['email'],
                       password=user_data['password'])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_role(role: schemas.RoleIn, db: Session):
    roles = models.Roles(name=role['name'])
    db.add(roles)
    db.commit()
    db.refresh(roles)
    return roles


def get_role_by_id(db: Session, role_id: int):
    return db.query(models.Roles).filter(models.Roles.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(models.Roles).filter(models.Roles.name == name).first()


def get_all_roles(db: Session):
    return db.query(models.Roles).all()


def get_user(email: str, db: Session):
    if user := db.query(models.User).filter(models.User.email == email).first():
        return user


def update_user_password(new_password: str, email: str, db: Session):
    if user := db.query(models.User).filter(models.User.email == email).first():
        user.password = new_password
        db.commit()
        db.refresh(user)
        return user
