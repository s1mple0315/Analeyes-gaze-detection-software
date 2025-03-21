from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

client = AsyncIOMotorClient('mongodb://localhost:27017/')
db = client["gaze_tracker"]
users_collection = db["users"]
sessions_collection = db["sessions"]
fs = AsyncIOMotorGridFSBucket(db)

async def init_db():
    await users_collection.create_index("username", unique=True)
    await users_collection.create_index("email", unique=True)
    await sessions_collection.create_index("user_id", unique=True)