from datetime import datetime
from pydantic import BaseModel

class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float

from sqlalchemy import Column, Float, String, DateTime, Integer
from app.database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    full_name = Column(String, index = True)
    hashed_password = Column(String)
    balance = Column(Float, default=0)
    last_login = Column(DateTime, nullable=True)

class TransactionHistory(Base):
    __tablename__ = "transaction_history"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    receiver = Column(String, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)

