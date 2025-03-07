from fastapi import APIRouter, Depends, HTTPException, Request
from app.models import TransactionModel
from app.blockchain import Transaction, Blockchain
from app.auth import login_user, get_current_user

router = APIRouter()

# Global blockchain instance (state persists in memory)
blockchain = Blockchain()

@router.post("/login")
async def login(request: Request, username: str, password: str):
    """Login endpoint for users. It verifies the user's credentials and sets the session."""
    return await login_user(request, username, password)

@router.post("/transaction/")
async def create_transaction(
    tx: TransactionModel,
    current_user: dict = Depends(get_current_user)
):
    # Ensure that the logged-in user is sending from their own account.
    if tx.sender != current_user["username"]:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized: You can only send from your own account!"
        )
    # Check that the sender has enough funds.
    sender_balance = blockchain.get_balance(tx.sender)
    if sender_balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    # Record the transaction by creating a new block.
    transaction = Transaction(tx.sender, tx.receiver, tx.amount)
    blockchain.add_transaction(transaction)
    return {"message": "Transaction recorded. Amount sent: " + str(tx.amount)}

@router.get("/balance/")
async def get_balance(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    balance = blockchain.get_balance(username)
    return {"address": username, "balance": balance}

@router.get("/transactions/")
async def get_transaction_history(current_user: dict = Depends(get_current_user)):
    history = blockchain.get_transaction_history()
    return {"transactions": history}

# Token Login system as a fallback if program does not work
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models import TransactionModel
from app.blockchain import Transaction, Blockchain
from app.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user,
    fake_users_db
)

router = APIRouter()
blockchain = Blockchain()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/transaction/")
async def create_transaction(tx: TransactionModel, current_user: dict = Depends(get_current_user)):
    # Ensure the logged-in user is the sender.
    if tx.sender != current_user["username"]:
        raise HTTPException(status_code=403, detail="Unauthorized: You can only send from your own account!")
    sender_balance = blockchain.get_balance(tx.sender)
    if sender_balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    transaction = Transaction(tx.sender, tx.receiver, tx.amount)
    blockchain.add_transaction(transaction)
    return {"message": "Transaction recorded"}

@router.get("/balance/")
async def get_balance(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    balance = blockchain.get_balance(username)
    return {"address": username, "balance": balance}

@router.get("/transactions/")
async def get_transaction_history(current_user: dict = Depends(get_current_user)):
    history = blockchain.get_transaction_history()
    return {"transactions": history}
"""