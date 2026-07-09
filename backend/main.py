from fastapi import FastAPI, HTTPException, Depends, status
from database import engine,SessionLocal
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
import re
import models
from auth import router, get_current_user
from models import Account, Transaction

description = '''
    ## welcome
'''

app = FastAPI(title='BANKING SYSTEM', description=description, summary='login - register')
models.Base.metadata.create_all(bind=engine)
app.include_router(router)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Deposit(BaseModel):
    amount:float
class Withdraw(BaseModel):
    amount:float

@app.post('/deposit', status_code=status.HTTP_200_OK)
async def deposit(deposit:Deposit, db:db_dependency, current_user:user_dependency):
    if deposit.amount <= 0:
        raise HTTPException(status_code=400, detail='amount must be positive')
    account = db.query(Account).filter(Account.account_number==current_user['account_number']).first()
    if account is None:
        raise HTTPException(status_code=404, detail='account not found')
    account.balance+= deposit.amount
    transaction_data = Transaction(
        account_number= account.account_number,
        transaction_type = 'deposit', 
        amount = deposit.amount
    )
    db.add(transaction_data)
    db.commit()
    return{'message': 'amount deposited successfully', 'current_balance': account.balance}

@app.post('/withdraw', status_code=status.HTTP_200_OK)
async def withdraw(withdraw:Withdraw, db:db_dependency, current_user:user_dependency):
    if withdraw.amount <= 0:
        raise HTTPException(status_code=400, detail='amount must be positive')
    account = db.query(Account).filter(Account.account_number==current_user['account_number']).first()
    if account is None:
        raise HTTPException(status_code=404, detail='account not found')
    if withdraw.amount>account.balance:
        raise HTTPException(status_code=400, detail='not enough funds')
    account.balance-=withdraw.amount
    transaction_data = Transaction(
        account_number= account.account_number,
        transaction_type = 'withdraw', 
        amount = withdraw.amount
    )
    db.add(transaction_data)
    db.commit()
    return{'message': 'amount withdrawn successfully', 'current_balance': account.balance}
        
    
@app.get('/balance')
async def check_balance(db:db_dependency,current_user:user_dependency):
        account = db.query(Account).filter(Account.account_number==current_user['account_number']).first()
        if account is None:
            raise HTTPException(status_code=404, detail='account not found')
        return {
            'account_number': account.account_number,
            'holder_name': account.holder_name,
            'account_type': account.account_type,
            'balance': account.balance
            }
        
@app.get('/transaction')
async def transaction_history(db:db_dependency, current_user:user_dependency):
        account = db.query(Account).filter(Account.account_number==current_user['account_number']).first()
        if account is None:
            raise HTTPException(status_code=400, detail='account not found')
        transactions = db.query(Transaction).filter(Transaction.account_number==account.account_number).all()
        return transactions
    
@app.get('/benefits')
async def benefits(db:db_dependency,current_user:user_dependency):
        account = db.query(Account).filter(Account.account_number==current_user['account_number']).first()
        if account is None:
            raise HTTPException(status_code=400, detail='account not found')
        if account.account_type.lower() == 'savings':
            interest = account.balance * 0.01
            return {'interest':interest}
        else:
            return {'message': 'account type - current - no benefits are there for current account'}