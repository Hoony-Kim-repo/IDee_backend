# This file is responsible for all Firestore CRUD processes
from datetime import datetime, timezone

from fastapi.concurrency import run_in_threadpool

from firebase.schemas.users import UserCreate, UserInDB

from ..firebase_conn import db


async def getUserByGoogle(uid: SyntaxWarning):
    """
    Firestore get user by Google UID
    """
    users_ref = db.collection("users").document(uid)

    def _inner():
        doc = users_ref.get()
        return doc.to_dict() if doc.exists else None

    raw = await run_in_threadpool(_inner)
    return UserInDB(**raw) if raw else None


async def SigupUserByGoogle(data: UserCreate):
    """
    Firestore create user by Google
    """
    print("Signning up by Google UID")
    users_ref = db.collection("users").document(data.uid)

    if users_ref.get().exists:
        return None  # User already exists

    def _inner():
        now = datetime.now(timezone.utc)
        new_user = {
            **data.model_dump(),
            "provider": "google",
            "createdAt": now,
        }

        users_ref.set(new_user)

        return new_user

    raw = await run_in_threadpool(_inner)
    return UserInDB(**raw)
