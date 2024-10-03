from fastapi import Depends, APIRouter
from app.auth import get_current_user, get_post_author_or_admin
from app.schemas import PostCreate, PostUpdate
from app.crud import create_post, get_posts, get_post_by_id, update_post, delete_post, get_posts_by_author_id,get_posts_by_date_range

router = APIRouter()

from fastapi import HTTPException, Query
from pydantic import ValidationError
from typing import Optional
from datetime import datetime, timedelta


# Create post
@router.post("/")
async def create_new_post(post_data: PostCreate, current_user: dict = Depends(get_current_user)):
    try:
        post_id = await create_post(post_data, author_id=str(current_user["_id"]))  # Use user_id
        return {"post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")


# Get post by ID
@router.get("/{post_id}")
async def get_single_post(post_id: str):
    try:
        post = await get_post_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except Exception as e:
        print(f"Error fetching post: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching post: {str(e)}")


# Filter posts by author
@router.get("/author/{author_id}")
async def get_posts_by_author(author_id: str):
    try:
        posts = await get_posts_by_author_id(author_id)  # Use author_id in the query
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching posts by author: {str(e)}")


# Get posts with optional filters
@router.get("/")
async def get_all_posts(page: int = 1, limit: int = 10, author_id: Optional[str] = None):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be greater than 0")

    try:
        skip = (page - 1) * limit  # Calculate skip based on the page and limit
        posts = await get_posts(skip=skip, limit=limit, author_id=author_id)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching posts: {str(e)}")


# Update post
@router.put("/{post_id}")
async def update_existing_post(post_id: str, post_data: PostUpdate, current_user: dict = Depends(get_current_user)):
    try:
        await get_post_author_or_admin(post_id, current_user)
        updated_count = await update_post(post_id, post_data.dict(exclude_unset=True))
        if updated_count:
            return {"msg": "Post updated"}
        raise HTTPException(status_code=404, detail="Post not found")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating post: {str(e)}")


# Delete post endpoint
@router.delete("/{post_id}")
async def delete_existing_post(post_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # Ensure the user is either the author of the post or an admin
        await get_post_author_or_admin(post_id, current_user)

        # Attempt to delete the post from the database
        deleted_count = await delete_post(post_id)

        # If the post was deleted, return a success message
        if deleted_count:
            return {"msg": "Post deleted successfully"}

        # If no posts were deleted (post ID not found), raise an error
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting post: {str(e)}")


# Filter posts by date range
@router.get("/date/")
async def get_posts_by_date_range_api(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    try:
        # Convert the start and end dates to datetime objects
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        # End date should include the end of the day
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1, seconds=-1)

        posts = await get_posts_by_date_range(start_date_obj, end_date_obj)
        return posts
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching posts by date range: {str(e)}")
