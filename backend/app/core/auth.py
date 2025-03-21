from jwt import encode, decode, PyJWTError  
from bcrypt import hashpw, checkpw, gensalt
from fastapi import HTTPException

SECRET_KEY = "some-secret-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_token(user_id: str) -> str:
    return encode({"sub": user_id}, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")