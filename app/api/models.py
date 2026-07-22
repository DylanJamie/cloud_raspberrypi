# models.py

# Just the shape. we have no logic in this file

# USERS
# FILES

class USER:
    user_id: str # user ID never changes even if the user decides to change their username
    usename: str
    password_hash: str # we dont want to store raw passwords
    created_at: datetime

class FILE:
    file_id: str # ID that will never change regardless of the file name
    owner_id: str # Foreign key -> USER.user_id
    original_filename: str
    storage_path: str
    content_type: str
    file_hash: str
    size_bytes: int
    upploaded_at: datetime
    
