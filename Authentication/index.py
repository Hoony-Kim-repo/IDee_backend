from fastapi import APIRouter, Depends

from firebase.auth_utils import get_current_user

from .google.user_requests import router as google_router
from .userEmailPassword.user_reqeusts import router as email_password_router

router = APIRouter()

router.include_router(google_router, prefix="/api")
router.include_router(email_password_router, prefix="/api")


@router.get("/api/isLoggedIn")
async def isLoggedIn(current_user=Depends(get_current_user)):
    # Return user info from JWT
    if not current_user:
        return {"isLoggedIn": False, "user": None}
    return current_user
