from datetime import datetime
from sqlalchemy import Column, Float, String, DateTime, Integer
from app.database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String(255), primary_key=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    balance = Column(Float, nullable=True)
    last_login = Column(DateTime, nullable=True)

class TransactionHistory(Base):
    __tablename__ = "transaction_history"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(255), index=True)
    receiver = Column(String(255), index=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)

