import re
from pydantic import BaseModel, field_validator


class CreateUserRequest(BaseModel):
    username: str
    password: str
    account_type: str

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
        if not re.fullmatch(
            r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}",
            value,
        ):
            raise ValueError(
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
            )
        return value

    @field_validator("account_type")
    @classmethod
    def validate_account_type(cls, value):
        if value.lower() not in ["savings", "current"]:
            raise ValueError("account type must be savings or current")
        return value


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    account_number: str


class Deposit(BaseModel):
    amount: float


class Withdraw(BaseModel):
    amount: float