from Tools.demo.mcast import receiver
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from app.database import SessionLocal, engine, Base
from app.models import TransactionModel, User, TransactionHistory
# from app.blockchain import Transaction, Blockchain
from app.auth import login_user, get_current_user, register_user
from app.security import hash_address

router = APIRouter()

# Global blockchain instance (state persists in memory)
# blockchain = Blockchain()

@router.post("/register", operation_id="register_user")
async def register(request: Request, username: str, full_name: str, password: str):
    return await register_user(request, username, full_name, password)
@router.post("/login", operation_id="login_user")
async def login(request: Request, username: str, password: str):
    return await login_user(request, username, password)
@router.post("/logout")
async def logout(request: Request, current_user: dict = Depends(get_current_user)):
    request.session.pop("user", None)
    return {"message": "Logged out successfully"}

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
    db = SessionLocal()
    try:
        sender = db.query(User).filter(User.username == tx.sender).first()
        receiver = db.query(User).filter(User.username == tx.receiver).first()
        if sender is None:
            raise HTTPException(status_code=404, detail="Sender not found")
        if receiver is None:
            raise HTTPException(status_code=404, detail="Receiver not found")
        if sender.balance < tx.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        sender.balance -= tx.amount
        receiver.balance += tx.amount

        new_tx = TransactionHistory(sender=hash_address(tx.sender), receiver=hash_address(tx.receiver), amount=tx.amount)
        db.add(new_tx)
        db.commit()
        db.refresh(new_tx)
        return {"message": "Transaction recorded, Amount sent: " + str(tx.amount)}
    finally:
        db.close()

    # # Check that the sender has enough funds.
    # sender_balance = blockchain.get_balance(tx.sender)
    # if sender_balance < tx.amount:
    #     raise HTTPException(status_code=400, detail="Insufficient funds")
    # # Record the transaction by creating a new block.
    # transaction = Transaction(tx.sender, tx.receiver, tx.amount)
    # blockchain.add_transaction(transaction)
    # return {"message": "Transaction recorded. Amount sent: " + str(tx.amount)}

@router.get("/balance/")
async def get_balance(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": user.username, "balance": user.balance}
    finally:
        db.close()
    # username = current_user["username"]
    # balance = blockchain.get_balance(username)
    # return {"address": username, "balance": balance}

@router.get("/transactions/")
async def get_transaction(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        user_hash = hash_address(current_user["username"])
        transactions = db.query(TransactionHistory).filter(
            or_(
                TransactionHistory.sender == user_hash,
                TransactionHistory.receiver == user_hash
            )
        ).all()
        tx_list = []
        for tx in transactions:
            tx_list.append({
                # "id": tx.id,
                "sender": tx.sender,
                "receiver": tx.receiver,
                "amount": tx.amount,
                "timestamp": tx.timestamp.isoformat()
            })
        return {"transactions": tx_list}
    finally:
        db.close()

@router.get("/transactions_Network/")
async def get_transaction_history(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    try:
        transactions = db.query(TransactionHistory).all()
        tx_network_list = []
        for tx in transactions:
            tx_network_list.append({
                # "id": tx.id,
                "sender": tx.sender,
                "receiver": tx.receiver,
                "amount": tx.amount,
                "timestamp": tx.timestamp.isoformat()
            })
        return {"transactions": tx_network_list}
    finally:
        db.close()
    # history = blockchain.get_transaction_history()
    # # return {"transactions": history}

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