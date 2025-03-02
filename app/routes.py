from fastapi import APIRouter, HTTPException
from app.models import TransactionModel
from app.blockchain import Transaction, Blockchain

router = APIRouter()

# Global blockchain instance
blockchain = Blockchain()

@router.post("/transaction/")
async def create_transaction(tx: TransactionModel):
    # Edge case: Sender fund check before adding the transaction
    sender_balance = blockchain.get_balance(tx.sender)
    if sender_balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    transaction = Transaction(tx.sender, tx.receiver, tx.amount)
    blockchain.add_transaction(transaction)
    return {"message": "Transaction added", "transaction": transaction.to_dict()}

@router.post("/mine/")
async def mine_transactions(miner_address: str):
    block = blockchain.mine_pending_transactions(miner_address)
    if block is None:
        raise HTTPException(status_code=400, detail="No transactions to mine")
    return {"message": "Block mined", "block": block.__dict__}

@router.get("/balance/{address}")
async def get_balance(address: str):
    balance = blockchain.get_balance(address)
    return {"address": address, "balance": balance}

@router.get("/transactions/")
async def get_transaction_history():
    history = blockchain.get_transaction_history()
    return {"transactions": history}
