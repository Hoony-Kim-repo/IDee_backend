from fastapi import APIRouter

from .google.user_requests import router as google_router
from .userEmailPassword.user_reqeusts import router as email_password_router

router = APIRouter()

router.include_router(google_router, prefix="/api")
router.include_router(email_password_router, prefix="/api")
