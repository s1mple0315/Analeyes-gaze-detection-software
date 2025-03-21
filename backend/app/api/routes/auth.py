from fastapi import APIRouter, HTTPException
from app.models.schemas import User
from app.db.mongo import users_collection
from app.core.auth import hash_password, verify_password, create_token

router = APIRouter()


@router.post("/login")
async def login(user: User):
    stored_user = await users_collection.find_one(
        {"$or": [{"email": user.email}, {"username": user.username}]}
    )
    if stored_user and verify_password(user.password, stored_user["password"]):
        token = create_token(str(stored_user["_id"]))
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/register")
async def register(user: User):
    if await users_collection.find_one(
        {"$or": [{"email": user.email}, {"username": user.username}]}
    ):
        raise HTTPException(status_code=400, detail="User already registered")
    hashed_password = hash_password(user.password)
    result = await users_collection.insert_one(
        {"username": user.username, "email": user.email, "password": hashed_password}
    )
    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
    }
