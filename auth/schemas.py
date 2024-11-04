from typing import Optional
from datetime import datetime
from sqlalchemy import Column, String, TIMESTAMP
from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    email: str
    username: str
    registered_at: datetime
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    hashed_password: str
    registered_at: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
