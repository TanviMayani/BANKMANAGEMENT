from typing import Annotated
from datetime import datetime,timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel,field_validator
from sqlalchemy.orm import Session 
from passlib.context import CryptContext
from jose import jwt, JWTError
from database import SessionLocal
from models import Account
from starlette import status
import re
import os
from dotenv import load_dotenv
import random


router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

scheme = HTTPBearer(auto_error=False)

from pydantic import BaseModel, field_validator
import re

class CreateUserRequest(BaseModel):
    username: str
    password: str
    account_type :str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_]{4,20}", value):
            raise ValueError(
                "Username must be 4-20 characters long and contain only letters, numbers, and underscores."
            )
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}",value,):
            raise ValueError("Password must be at least 8 characters and include uppercase, lowercase, number, and special character.")
        return value
    
    @field_validator("account_type")
    @classmethod
    def validate_account_type(cls,value):
        if value.lower() not in['savings','current']:
            raise ValueError('account type must be savings or current')
        return value
    
class LoginRequest(BaseModel):
    username: str
    password: str    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    account_number : str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
    
    existing_user = db.query(Account).filter(Account.username==create_user_request.username).first()
    if existing_user:
        raise HTTPException(status_code=400,detail='username already exists.')
    create_user_model = Account(
        account_number = generate_account_number(db),
        username = create_user_request.username,
        password = bcrypt_context.hash(create_user_request.password),
        holder_name= create_user_request.username,
        account_type=create_user_request.account_type,
        balance=0
    )       
    db.add(create_user_model)
    db.commit()
    return{'message': 'user registered successfully'}

@router.post('/login', response_model=Token)
async def login(login_request: LoginRequest, db: db_dependency):

    user = authenticate_user(login_request.username,login_request.password,db)
    if not user:
         raise HTTPException(status_code=401,detail="Invalid username or password" )

    token = create_access_token(user.username,user.account_number,timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "access_token": token,
        "token_type": "Bearer",
        "account_number":user.account_number
    }

def authenticate_user(username : str , password: str, db):
    user = db.query(Account).filter(Account.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user    
    
def create_access_token(username:str, account_number:int, expires_delta:timedelta):
    encode={
        'sub':username,
        'account_number': account_number
    }
    expires = datetime.utcnow() +expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
def generate_account_number(db):
    while True:
        account_number=str(random.randint(1000000000,9999999999))
        existing_account=db.query(Account).filter(Account.account_number==account_number).first()
        if not existing_account:
            return account_number

async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(scheme)]):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials 

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        account_number = payload.get("account_number")

        if username is None or account_number is None:
            raise HTTPException(status_code=401, detail="Authentication failed")

        return {
            "username": username,
            "account_number": account_number
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get('/me')
async def read_current_user(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user