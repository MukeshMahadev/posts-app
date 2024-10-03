from bson import ObjectId
from app.database import post_collection, user_collection
from app.models import Post, User
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create a new user
async def create_user(user_data):
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_admin=False
    )
    result = await user_collection.insert_one(user.__dict__)
    return str(result.inserted_id)


# Get user by email
async def get_user_by_email(email: str):
    user = await user_collection.find_one({"email": email})
    return user


# Create a new post
async def create_post(post_data, author_id: str):
    post = Post(title=post_data.title, content=post_data.content, author_id=author_id)
    result = await post_collection.insert_one(post.__dict__)
    return str(result.inserted_id)


# Get a post by ID
async def get_post_by_id(post_id: str):
    return await post_collection.find_one({"_id": ObjectId(post_id)})


# Get posts with optional filtering
async def get_posts(skip: int = 0, limit: int = 10, author_id: str = None):
    query = {"author_id": author_id} if author_id else {}
    posts = await post_collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    # Convert _id to string for each post
    for post in posts:
        post["_id"] = str(post["_id"])
    return posts


# Update a post
async def update_post(post_id: str, post_data):
    result = await post_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": post_data}
    )
    return result.modified_count


# Delete a post
async def delete_post(post_id: str):
    result = await post_collection.delete_one({"_id": ObjectId(post_id)})
    return result.deleted_count


# Get a post by ID
async def get_post_by_id(post_id: str):
    post = await post_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
        return post
    return None


# Get posts by author
async def get_posts_by_author_id(author_id: str):
    posts = await post_collection.find({"author_id": author_id}).to_list(length=None)
    # Convert _id to string for each post
    for post in posts:
        post["_id"] = str(post["_id"])

    return posts


# Get posts between a date range
async def get_posts_by_date_range(start_date: datetime, end_date: datetime):
    posts = await post_collection.find({
        "creation_date": {
            "$gte": start_date,
            "$lte": end_date
        }
    }).to_list(length=None)
    # Convert _id to string for each post
    for post in posts:
        post["_id"] = str(post["_id"])
    return posts
