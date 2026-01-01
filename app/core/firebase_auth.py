from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth


def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    """
    Verify Firebase ID token and return decoded payload.
    """
    token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase token")
