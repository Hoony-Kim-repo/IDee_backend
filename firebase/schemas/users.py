from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

PROVIDER_ALLOWED = {"google", "password"}


class UserBase(BaseModel):
    email: EmailStr
    provider: str = Field(
        ...,
        description="Authentication provider, e.g., 'google', 'password', etc.",
    )

    @field_validator("provider")
    def validate_provider(cls, v):
        if v not in PROVIDER_ALLOWED:
            raise ValueError(f"Provider '{v}' is not supported.")
        return v


class UserCreate(UserBase):
    """
    Input model when creating a user.
    Usually from google or password signup.
    """

    uid: str
    name: Optional[str] = None


class UserInDB(UserBase):
    """
    Model for storing user in DB
    """

    uid: str
    name: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserRead(UserInDB):
    """
    API response model.
    Could be identical to UserInDB for now.
    """

    pass
