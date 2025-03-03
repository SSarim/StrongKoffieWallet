from logging import raiseExceptions

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

ALGORITHM = "HS256"



# In-memory user
fake_users_db = {
    "peer1": {
        "username": "peer1",
        "full_name": "Peer One",
        "hashed_password": "$2b$12$tZYu2anTvNrCVCtPQMInOeYom8MWzR3LoKeqW1hDgJAd4rLbuGsM6",  # hash for "password1"
    },
    "peer2": {
        "username": "peer2",
        "full_name": "Peer Two",
        "hashed_password": "$2b$12$WarY/YdUliC8wsvtOeJxHOO51hF1vuMvHIFAoiXdUJi/jQSmIYxZK",  # hash for "password2"
    },
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        return db[username]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"},
        )



def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(fake_users_db, credentials.username)
    if user is None or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
