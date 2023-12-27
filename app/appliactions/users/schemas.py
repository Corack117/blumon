from pydantic import BaseModel, field_validator
from fastapi import HTTPException

class UserBase(BaseModel):
    username: str
    email: str

    @field_validator('*')
    def never_empty(cls, v: str) -> str:
        if not v:
            raise HTTPException(status_code=400, detail='Los campos no pueden ser vacío')
        return v

class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

class TokenBase(BaseModel):
    username: str
    jwt: str