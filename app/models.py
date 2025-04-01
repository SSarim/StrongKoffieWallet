from pydantic import BaseModel
# Pydantic model
class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float
