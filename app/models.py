from pydantic import BaseModel
from app.blockchain import User, TransactionHistory
# Pydantic model
class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float
