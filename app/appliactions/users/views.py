from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from . import schemas, crud
from datetime import timedelta
from .utils import authenticate_user, create_token, token_info, refresh_token_info

router = APIRouter(prefix='/user')

oauth2_scheme = OAuth2PasswordBearer('/user/login')

@router.post('/create')
def create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_finded = crud.get_user_email_or_username(db, user.username, user.email)
    if user_finded:
        raise HTTPException(status_code=400, detail='Ya existe un usuario con ese username o email')
    return crud.create_user(db, user)

@router.get("/login")
def login_form():
    html_content = """
    <!DOCTYPE html>
    <html>
       <body>
          <form method="POST"  action="/user/login">
             <label for="username">Username:</label><br>
             <input type="text" id="username" name="username" value=""><br>
             <label for="password">Password:</label><br>
             <input type="password" id="password" name="password" value=""><br><br>
             <input type="submit" value="Submit">
          </form>
       </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_jwt = create_token(data={ 'sub': user.username })
    refresh_token = crud.create_refresh_token_data(db, user.username)
    return {
        'access_token': access_token_jwt,
        'refresh_token': refresh_token.jwt,
        'token_type': 'bearer'
    }
    

@router.get('/logout')
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = token_info(token)
    crud.remove_refresh_token(db, username)
    new_access_token = create_token(data={ 'sub': username }, time=timedelta(milliseconds=1))
    return {
        "access_token": new_access_token,
        "token_type": "Bearer",
        'msg': 'Se ha cerrado la sesión'
    }

@router.get('/refresh_token')
def refresh(token: str):
    username = refresh_token_info(token)

    new_access_token = create_token(data={ 'sub': username })
    return {
        "access_token": new_access_token,
        "token_type": 'bearer'
    }

@router.get('/info')
def data(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = token_info(token)
    user = crud.get_user(db, username)
    return schemas.UserBase(username=user.username, email=user.email).model_dump()