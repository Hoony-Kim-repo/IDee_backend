from typing import Optional

from pydantic import BaseModel


class ProfileCreate(BaseModel):
    fullName: str
    nickname: Optional[str] = None
    phoneNumber: Optional[str] = None
    dob: Optional[str] = None
    bio: Optional[str] = None
