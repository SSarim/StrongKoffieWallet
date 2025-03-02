from pydantic import BaseModel

class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float
