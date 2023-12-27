from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from datetime import timedelta
from . import schemas, models
from .utils import hash_password, create_refresh_token

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    secure_pass = hash_password(user.password)
    user_data = user.model_copy()
    user_data.password = secure_pass

    db_user = models.User(**user_data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_refresh_token_data(db: Session, username: str) -> models.Tokens:
    refresh_token_check = db.query(models.Tokens).filter(models.Tokens.username == username)
    if refresh_token_check.first():
        refresh_token_check.delete()
        db.commit()
    refresh_token = create_refresh_token(data={ 'sub': username })
    token = schemas.TokenBase(username=username, jwt=refresh_token)
    db_token = models.Tokens(**token.model_dump())
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def remove_refresh_token(db: Session, username: str):
    refresh_token = db.query(models.Tokens).filter(models.Tokens.username == username)
    if refresh_token.first():
        refresh_token.delete()
        db.commit()

def get_user_email_or_username(db: Session, username: str, email: str) -> models.User:
    return db.query(models.User).filter(or_(models.User.username == username, models.User.email == email)).first()

def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

