from fastapi import FastAPI
import uvicorn

from app.routers import posts, users

app = FastAPI()

# Include users router
app.include_router(users.router, prefix="", tags=["Users"])

# Include posts router
app.include_router(posts.router, prefix="/posts", tags=["Posts"])


# Root route (for testing)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Blog API!"}

# This is the part where you set up app.listen() like functionality
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)