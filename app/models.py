from datetime import datetime
from bson import ObjectId

class Post:
    def __init__(self, title: str, content: str, author_id: str):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.creation_date = datetime.utcnow()

class User:
    def __init__(self, name: str, email: str, hashed_password: str, is_admin: bool = False):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_admin = is_admin
