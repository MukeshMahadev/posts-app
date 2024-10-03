from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.blogsdb

# Collection for users and posts
user_collection = db["users"]
post_collection = db["posts"]

async def get_db():
    return db