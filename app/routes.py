from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_
from app.database import SessionLocal
from app.models import TransactionModel
from app.blockchain import User, TransactionHistory
from app.auth import login_user, get_current_user, register_user
from app.security import hash_address
router = APIRouter()

@router.post("/register", operation_id="register_user")
async def register(username: str, full_name: str, password: str):
    return await register_user(username, full_name, password)

@router.post("/login", operation_id="login_user")
async def login(request: Request, username: str, password: str):
    return await login_user(request, username, password)

@router.post("/logout")
async def logout(request: Request):
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

        new_tx = TransactionHistory(sender=hash_address(tx.sender),
                                    receiver=hash_address(tx.receiver),
                                    amount=tx.amount)
        db.add(new_tx)
        db.commit()
        db.refresh(new_tx)
        return {"message": "Transaction recorded, Amount sent: " + str(tx.amount)}
    finally:
        db.close()

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
async def get_transaction_history():
    db = SessionLocal()
    try:
        transactions = db.query(TransactionHistory).all()
        tx_network_list = []
        for tx in transactions:
            tx_network_list.append({
                "sender": tx.sender,
                "receiver": tx.receiver,
                "amount": tx.amount,
                "timestamp": tx.timestamp.isoformat()
            })
        return {"transactions": tx_network_list}
    finally:
        db.close()
