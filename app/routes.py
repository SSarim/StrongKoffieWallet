from app.models import TransactionModel
from app.blockchain import Transaction, Blockchain

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    get_current_user,
    fake_users_db
)

router = APIRouter()

# Global blockchain instance
blockchain = Blockchain()


@router.post("/token")
async def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub" : user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
# NEED TO FIX SO I CAN SEE IN LOCAL HOST DOCS



@router.post("/transaction/")
async def create_transaction(tx: TransactionModel, current_user: dict = Depends(get_current_user)):
#checking if the sender is the current user which is logged in
    if tx.sender != current_user["username"]:
        raise HTTPException(status_code=403, detail = "Unauthorized, please login to your own personal account!")


    # Edge case: Sender fund check before adding the transaction
    sender_balance = blockchain.get_balance(tx.sender)
    if sender_balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    transaction = Transaction(tx.sender, tx.receiver, tx.amount)
    blockchain.add_transaction(transaction)
    return {"message": "Transaction added", "transaction": transaction.to_dict()}

@router.post("/mine/")
async def mine_transactions(miner_address: str, current_user: dict = Depends(get_current_user)):
    block = blockchain.mine_pending_transactions(miner_address)
    # Testing: need to check in login required
    if block is None:
        raise HTTPException(status_code=400, detail="No transactions to mine")
    return {"message": "Block mined", "block": block.__dict__}

@router.get("/balance/{address}")
async def get_balance(address: str, current_user: dict = Depends(get_current_user)):
    balance = blockchain.get_balance(address)
    return {"address": address, "balance": balance}

@router.get("/transactions/")
async def get_transaction_history():
    history = blockchain.get_transaction_history()
    return {"transactions": history}
# need to see if I should have transactions available for public viewing or only auth users who are logged in.
# current_user : dict = Depends(get_current_user)