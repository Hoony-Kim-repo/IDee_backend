from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    uid: str


class UserInDB(UserBase):
    uid: str
    createdAt: datetime
    updatedAt: datetime
