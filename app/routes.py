# routes.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from datetime import datetime
from app.models import TransactionModel
from app.auth import login_user, get_current_user, register_user
from app.security import hash_address
from app.store import store

router = APIRouter()


@router.post("/register", operation_id="register_user")
async def register(username: str = Form(...), full_name: str = Form(...), password: str = Form(...)):
    return await register_user(username, full_name, password)


@router.post("/login", operation_id="login_user")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    return await login_user(request, username, password)


@router.post("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return {"message": "Logged out successfully"}


@router.post("/transaction/")
async def create_transaction(tx: TransactionModel, current_user: dict = Depends(get_current_user)):
    if tx.sender != current_user["username"]:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized: You can only send from your own account!"
        )

    sender = store["users"].get(tx.sender)
    receiver = store["users"].get(tx.receiver)

    if sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")
    if sender["balance"] < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Update balances
    sender["balance"] -= tx.amount
    receiver["balance"] += tx.amount

    # Record transaction
    new_tx = {
        "sender": hash_address(tx.sender),
        "receiver": hash_address(tx.receiver),
        "amount": tx.amount,
        "timestamp": datetime.now().isoformat()
    }
    store["transactions"].append(new_tx)
    return {"message": f"Transaction recorded, Amount sent: {tx.amount}"}


@router.get("/balance/")
async def get_balance(current_user: dict = Depends(get_current_user)):
    user = store["users"].get(current_user["username"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["username"], "balance": user["balance"]}


@router.get("/transactions/")
async def get_transaction(current_user: dict = Depends(get_current_user)):
    user_hash = hash_address(current_user["username"])
    # Filter transactions
    user_transactions = [
        {
            "sender": tx["sender"],
            "receiver": tx["receiver"],
            "amount": tx["amount"],
            "timestamp": tx["timestamp"]
        }
        for tx in store["transactions"]
        if tx["sender"] == user_hash or tx["receiver"] == user_hash
    ]
    return {"transactions": user_transactions}


@router.get("/transactions_network/")
async def get_transaction_history():
    return {"transactions": store["transactions"]}








# COULDNT DEPLOY WITH DB
# from fastapi import APIRouter, Depends, HTTPException, Request, Form
# from sqlalchemy import or_
# from app.database import SessionLocal
# from app.models import TransactionModel
# from app.blockchain import User, TransactionHistory
# from app.auth import login_user, get_current_user, register_user
# from app.security import hash_address
#
# router = APIRouter()
#
#
# @router.post("/register", operation_id="register_user")
# async def register(username: str = Form(...), full_name: str = Form(...), password: str = Form(...)):
#     return await register_user(username, full_name, password)
#
#
# @router.post("/login", operation_id="login_user")
# async def login(request: Request, username: str = Form(...), password: str = Form(...)):
#     return await login_user(request, username, password)
#
#
# @router.post("/logout")
# async def logout(request: Request):
#     request.session.pop("user", None)
#     return {"message": "Logged out successfully"}
#
#
# @router.post("/transaction/")
# async def create_transaction(
#         tx: TransactionModel,
#         current_user: dict = Depends(get_current_user)
# ):
#     # Ensure that the logged-in user is sending from their own account.
#     if tx.sender != current_user["username"]:
#         raise HTTPException(
#             status_code=403,
#             detail="Unauthorized: You can only send from your own account!"
#         )
#     db = SessionLocal()
#     try:
#         sender = db.query(User).filter(User.username == tx.sender).first()
#         receiver = db.query(User).filter(User.username == tx.receiver).first()
#         if sender is None:
#             raise HTTPException(status_code=404, detail="Sender not found")
#         if receiver is None:
#             raise HTTPException(status_code=404, detail="Receiver not found")
#         if sender.balance < tx.amount:
#             raise HTTPException(status_code=400, detail="Insufficient funds")
#         sender.balance -= tx.amount
#         receiver.balance += tx.amount
#
#         new_tx = TransactionHistory(sender=hash_address(tx.sender),
#                                     receiver=hash_address(tx.receiver),
#                                     amount=tx.amount)
#         db.add(new_tx)
#         db.commit()
#         db.refresh(new_tx)
#         return {"message": "Transaction recorded, Amount sent: " + str(tx.amount)}
#     finally:
#         db.close()
#
#
# @router.get("/balance/")
# async def get_balance(current_user: dict = Depends(get_current_user)):
#     db = SessionLocal()
#     try:
#         user = db.query(User).filter(User.username == current_user["username"]).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return {"username": user.username, "balance": user.balance}
#     finally:
#         db.close()
#
#
# @router.get("/transactions/")
# async def get_transaction(current_user: dict = Depends(get_current_user)):
#     db = SessionLocal()
#     try:
#         user_hash = hash_address(current_user["username"])
#         transactions = db.query(TransactionHistory).filter(
#             or_(
#                 TransactionHistory.sender == user_hash,
#                 TransactionHistory.receiver == user_hash
#             )
#         ).all()
#         users = db.query(User).all()
#         hash_to_name = {hash_address(user.username): user.username for user in users}
#         tx_list = []
#         for tx in transactions:
#             plaintext_sender = hash_to_name.get(tx.sender, tx.sender)
#             plaintext_receiver = hash_to_name.get(tx.receiver, tx.receiver)
#             tx_list.append({
#                 "sender": plaintext_sender,
#                 "receiver": plaintext_receiver,
#                 "amount": tx.amount,
#                 "timestamp": tx.timestamp.isoformat()
#             })
#         return {"transactions": tx_list}
#     finally:
#         db.close()
#
#
# @router.get("/transactions_network/")
# async def get_transaction_history():
#     db = SessionLocal()
#     try:
#         transactions = db.query(TransactionHistory).all()
#         tx_network_list = []
#         for tx in transactions:
#             tx_network_list.append({
#                 "sender": tx.sender,
#                 "receiver": tx.receiver,
#                 "amount": tx.amount,
#                 "timestamp": tx.timestamp.isoformat()
#             })
#         return {"transactions": tx_network_list}
#     finally:
#         db.close()
