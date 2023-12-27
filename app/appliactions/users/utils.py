from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from . import crud
from app.config import variables as const
from jose import jwt, JWTError

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
    verified = verify_password(password=password, hash_password=user.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
    user.is_active = True
    db.commit()
    db.flush()
    return user

def create_token(data: dict, time: timedelta = timedelta(minutes=5)) -> str:
    data_copy = data.copy()
    expires = datetime.utcnow() + time
    data_copy.update({'exp': expires})
    token_jwt = jwt.encode(data_copy, key=const.SECRET_KEY, algorithm=const.ALGORITHM)
    return token_jwt

def create_refresh_token(data: dict, time: timedelta = timedelta(minutes=30)) -> str:
    data_copy = data.copy()
    expires = datetime.utcnow() + time
    data_copy.update({'exp': expires})
    token_jwt = jwt.encode(data_copy, key=const.REFRESH_SECRET_KEY, algorithm=const.ALGORITHM)
    return token_jwt

def refresh_token(token: str) -> dict:
    return 

def token_info(token: str) -> str:
    try:
        token_decode = jwt.decode(token, key=const.SECRET_KEY, algorithms=[const.ALGORITHM])
        username = token_decode.get('sub', None)
        if not username:
            raise HTTPException(status_code=400, detail='No se han podido validar las credenciales')
    except JWTError:
        raise HTTPException(status_code=400, detail='No se han podido validar las credenciales')
    return username

def refresh_token_info(token: str) -> str:
    try:
        token_decode = jwt.decode(token, key=const.REFRESH_SECRET_KEY, algorithms=[const.ALGORITHM])
        username = token_decode.get('sub', None)
        if not username:
            raise HTTPException(status_code=400, detail='No se han podido validar las credenciales')
    except JWTError:
        raise HTTPException(status_code=400, detail='No se han podido validar las credenciales')
    return username

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hash_password) -> bool:
    return pbkdf2_sha256.verify(password, hash_password)