# models.py

# Just the shape. we have no logic in this file

# Imports
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4

# USERS
# FILES

class USER(SQLModel, table=True):
    user_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True) # user ID never changes even if the user decides to change their username
    username: str = Field(unique=True, index=True)
    password_hash: str # we dont want to store raw passwords
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FILE(SQLModel, table=True):
    file_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True) # ID that will never change regardless of the file name
    owner_id: str = Field(foreign_key="user.user_id", index=True) # Index this out # Foreign key -> USER.user_id
    original_filename: str
    storage_path: str
    content_type: str
    file_hash: str
    size_bytes: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class SESSION(SQLModel, table=True):
    session_id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.user_id", index=True) # Index this out # Foreign key -> USER.user_id
    created_session_time: datetime = Field(default_factory=datetime.utcnow)
