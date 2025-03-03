from logging import raiseExceptions

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
import secrets
# Secret key for encoding JWT tokens
# SECRET_KEY = "Bobby_Shmurda"  # Change this to a strong secret in production
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# In-memory user store for demonstration purposes
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
    # if plain_password in db:
        return pwd_context.verify(plain_password, hashed_password)
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="pass not found",
    #         headers={"WWW-Authenticate": "Basic"},
    #     )

def get_user(db, username: str):
    if username in db:
        return db[username]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"},
        )

# def authenticate_user(db, username: str, password: str):
#     user = get_user(db, username)
#     if not user or not verify_password(password, user["hashed_password"]):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now() + expires_delta
#     else:
#         expire = datetime.now() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user(fake_users_db, credentials.username)
    if user is None or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
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
