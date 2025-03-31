from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import User

# In-memory user store (same as before)
# fake_users_db = {
#     "peer1": {
#         "username": "peer1",
#         "full_name": "Peer One",
#         "hashed_password": "$2b$12$tZYu2anTvNrCVCtPQMInOeYom8MWzR3LoKeqW1hDgJAd4rLbuGsM6",  # hash for "password1"
#     },
#     "peer2": {
#         "username": "peer2",
#         "full_name": "Peer Two",
#         "hashed_password": "$2b$12$WarY/YdUliC8wsvtOeJxHOO51hF1vuMvHIFAoiXdUJi/jQSmIYxZK",  # hash for "password2"
#     },
# }


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

async def login_user(request: Request, username: str, password: str):
    db = SessionLocal()
    try:
        user = get_user(db, username)
    # user = get_user(fake_users_db, username)
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        # Set the user in the session (stored in a signed cookie)
        request.session["user"] = user.username
        return {"message": "Logged in successfully"}
    finally:
        db.close()
async def register_user(request: Request, username: str, full_name: str, password: str):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )
        hashed_password = pwd_context.hash(password)
        new_user = User(username=username, full_name=full_name, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully"}
    finally:
        db.close()

def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return {"username": user}

 # Token Login system as a fallback if program does not work
# from datetime import datetime, timedelta
# from typing import Optional
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
# import jwt
#
# SECRET_KEY = "your-very-secret-key"  # Change this in production!
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# fake_users_db = {
#     "peer1": {
#         "username": "peer1",
#         "full_name": "Peer One",
#         "hashed_password": "$2b$12$tZYu2anTvNrCVCtPQMInOeYom8MWzR3LoKeqW1hDgJAd4rLbuGsM6",  # hash for "password1"
#     },
#     "peer2": {
#         "username": "peer2",
#         "full_name": "Peer Two",
#         "hashed_password": "$2b$12$WarY/YdUliC8wsvtOeJxHOO51hF1vuMvHIFAoiXdUJi/jQSmIYxZK",  # hash for "password2"
#     },
# }
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_user(db, username: str):
#     return db.get(username)
#
#
# def authenticate_user(db, username: str, password: str):
#     user = get_user(db, username)
#     if not user or not verify_password(password, user["hashed_password"]):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except jwt.PyJWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username)
#     if user is None:
#         raise credentials_exception
#     return user