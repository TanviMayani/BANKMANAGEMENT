from sqlalchemy import Column, String, Float, ForeignKey, Integer
from src.database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_number = Column(String, primary_key=True, unique=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    holder_name = Column(String)
    account_type = Column(String)
    balance = Column(Float, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(String)
    amount = Column(Float)
    account_number = Column(String, ForeignKey("accounts.account_number"))