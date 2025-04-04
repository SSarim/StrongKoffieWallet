# auth.py
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime
from app.store import store  # import the in‑memory store

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def register_user(username: str, full_name: str, password: str):
    if username in store["users"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    hashed_password = pwd_context.hash(password)
    # Save user data in the global store
    store["users"][username] = {
        "username": username,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "balance": 100.0,
        "last_login": None
    }
    return {"message": "User created successfully", "balance": 100.0}

async def login_user(request: Request, username: str, password: str):
    user = store["users"].get(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    # Update last login time
    user["last_login"] = datetime.now()
    # Save username in the session
    request.session["user"] = username
    return {"message": "Logged in successfully", "Last Login": user["last_login"].isoformat()}

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return {"username": user}





# from fastapi import Request, HTTPException, status
# from passlib.context import CryptContext
# from app.database import SessionLocal
# import datetime
# from app.blockchain import User
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
# def get_user(db, username: str):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return user
#
# async def login_user(request: Request, username: str, password: str):
#     db = SessionLocal()
#     try:
#         user = get_user(db, username)
#         if not verify_password(password, user.hashed_password):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect username or password"
#             )
#         # Find under in DB
#         user.last_login = datetime.datetime.now()
#         db.commit()
#         db.refresh(user)
#         request.session["user"] = user.username
#         return {"message": "Logged in successfully", "Last Login": user.last_login.isoformat()}
#     finally:
#         db.close()
#
# async def register_user(username: str, full_name: str, password: str):
#     db = SessionLocal()
#     try:
#         existing_user = db.query(User).filter(User.username == username).first()
#         if existing_user:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="User already exists"
#             )
#         hashed_password = pwd_context.hash(password)
#         new_user = User(username=username, full_name=full_name, hashed_password=hashed_password, balance=100)
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#         return {"message": "User created successfully", "balance": new_user.balance}
#     finally:
#         db.close()
#
# def get_current_user(request: Request):
#     user = request.session.get("user")
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )
#     return {"username": user}
