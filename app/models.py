from pydantic import BaseModel

class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float

from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    full_name = Column(String, index = True)
    hashed_password = Column(String)