from app.models import TransactionModel
from app.blockchain import Transaction, Blockchain

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.auth import (
    get_current_user,
    fake_users_db
)

router = APIRouter()

# Global blockchain instance
blockchain = Blockchain()


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
    # new_block = blockchain.add_transaction(transaction)
    # return {"message": "Transaction Accpeted", "block": new_block.__dict__}
    return {"message": "Transaction recorded"}

@router.get("/balance/")
async def get_balance(current_user: dict = Depends(get_current_user)):
    if current_user["username"] in fake_users_db != current_user["username"]:
    # if current_user != current_user["username"]:
        raise HTTPException(status_code=400, detail = "Unauthorized, please login to your own personal account!")
    username = current_user["username"]
    balance = blockchain.get_balance(username)
    return {"address": username, "balance": balance}


@router.get("/transactions/")
async def get_transaction_history():
    history = blockchain.get_transaction_history()
    return {"transactions": history}
# need to see if I should have transactions available for public viewing or only auth users who are logged in.
# current_user : dict = Depends(get_current_user)