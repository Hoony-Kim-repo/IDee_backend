# This file is responsible for all Firestore CRUD processes
from datetime import datetime, timezone
from fastapi.concurrency import run_in_threadpool
from firebase.schemas.users import UserCreate, UserInDB
from ..firebase_conn import db


async def get_or_create_user(data: UserCreate):
    """
    Firestore user create/get
    """

    users_ref = db.collection("users").document(data.uid)

    def _inner():
        doc = users_ref.get()

        now = datetime.now(timezone.utc)
        if not doc.exists:
            new_user = {
                **data.model_dump(),
                "createdAt": now,
                "updatedAt": now,
            }

            users_ref.set(new_user)

            return new_user

        users_ref.update({"updatedAt": now})

        stored_user = doc.to_dict()
        stored_user["updatedAt"] = now

        return stored_user

    raw = await run_in_threadpool(_inner)

    return UserInDB(**raw)
