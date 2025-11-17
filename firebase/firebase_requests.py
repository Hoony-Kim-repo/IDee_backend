from fastapi import HTTPException
from fastapi.security import HTTPBearer
from firebase_admin import auth

from .firebase_conn import db

security = HTTPBearer()


def verify_firebase_token(token):
    """
    Verify Firebase ID token and return decoded payload.
    This module only handles Firebase Auth logic.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")


def validate_user_email(email: str):
    """
    Check duplicates in Firbase Auth + Firestore
    """

    # Firebase Auth duplicate check
    try:
        _ = auth.get_user_by_email(email)
        return False  # User already exists
    except auth.UserNotFoundError:
        pass  # User does not exist

    # Firestore duplicate check
    query = db.collection("users").where("email", "==", email).limit(1).get()
    if query:
        return False  # User already exists

    return True
