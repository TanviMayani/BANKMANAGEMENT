import random
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.config import settings
from src.models import Account

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
scheme = HTTPBearer(auto_error=False)


def authenticate_user(username: str, password: str, db):
    user = db.query(Account).filter(Account.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, account_number: int, expires_delta: timedelta):
    encode = {"sub": username, "account_number": account_number}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)


def generate_account_number(db):
    while True:
        account_number = str(random.randint(1000000000, 9999999999))
        existing_account = db.query(Account).filter(
            Account.account_number == account_number
        ).first()
        if not existing_account:
            return account_number


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(scheme)]
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        account_number = payload.get("account_number")
        if username is None or account_number is None:
            raise HTTPException(status_code=401, detail="Authentication failed")
        return {"username": username, "account_number": account_number}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")