from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import settings
from src.database import SessionLocal
from src.models import Account
from src.schemas import CreateUserRequest, LoginRequest, Token
from src.security import (
    authenticate_user,
    bcrypt_context,
    create_access_token,
    generate_account_number,
    get_current_user,
)
from src.logger import logger

router = APIRouter(prefix="/auth", tags=["authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = db.query(Account).filter(
        Account.username == create_user_request.username
    ).first()
    if existing_user:
        logger.warning(f"username already exists: {create_user_request.username}")
        raise HTTPException(status_code=400, detail="username already exists.")

    create_user_model = Account(
        account_number=generate_account_number(db),
        username=create_user_request.username,
        password=bcrypt_context.hash(create_user_request.password),
        holder_name=create_user_request.username,
        account_type=create_user_request.account_type,
        balance=0,
    )
    db.add(create_user_model)
    db.commit()
    logger.info(f"User registered successfully: {create_user_request.username}")
    return {"message": "user registered successfully"}


@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest, db: db_dependency):
    user = authenticate_user(login_request.username, login_request.password, db)
    if not user:
        logger.warning(f"login attempt failed : {login_request.username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(
        user.username,
        user.account_number,
        timedelta(minutes=settings.access_token_expire_minutes),
    )
    logger.info(f"user logged in successfully :{user.username}")
    return {
        "access_token": token,
        "token_type": "Bearer",
        "account_number": user.account_number,
    }


@router.get("/me")
async def read_current_user(current_user: Annotated[dict, Depends(get_current_user)]):
    logger.info(f"accessed by : {current_user['account_number']}")
    return current_user