from fastapi import Depends, HTTPException, APIRouter
from app.auth import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas import UserCreate, Token
from app.crud import create_user, get_user_by_email
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

router = APIRouter()


@router.post("/signup/")
async def signup(user_data: UserCreate):
    try:
        # Check if a user with the given email already exists
        existing_user = await get_user_by_email(user_data.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already registered")

        # If not, proceed to create the new user
        user_id = await create_user(user_data)
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")


# Define the token endpoint
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")
