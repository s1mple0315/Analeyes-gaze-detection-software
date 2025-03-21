# backend/app/api/routes/auth.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import User
from app.db.mongo import users_collection
from app.core.auth import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/login")
async def login(username: str | None = None, email: str | None = None, password: str = None):
    if not password or (not username and not email):
        raise HTTPException(status_code=400, detail="Username or email and password are required")
    
    query = {}
    if username:
        query["username"] = username
    if email:
        query["email"] = email

    stored_user = await users_collection.find_one(query)
    if stored_user and verify_password(password, stored_user["password"]):
        token = create_token(str(stored_user["_id"]))
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register")
async def register(user: User):
    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = hash_password(user.password)
    result = await users_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    })
    return {"message": "User registered", "user_id": str(result.inserted_id)}