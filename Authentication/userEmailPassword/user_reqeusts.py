import bcrypt
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr

from firebase.firebase_requests import validate_user_email
from firebase.schemas.users import UserCreate

from .helpers import send_verification_email, verify_email_code

router = APIRouter()


class EmailRequest(BaseModel):
    email: EmailStr


class EmailVerifyRequest(BaseModel):
    email: EmailStr
    code: str


@router.post("/send-email-code")
async def sendEmailVerificationCode(payload: EmailRequest):
    """
    Send a 4-digit token to user's email for verification
    """
    try:
        send_verification_email(payload.email)
        return {
            "success": True,
            "message": f"Verification code sent to {payload.email}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare-email-code")
async def compareEmailVerificationCode(payload: EmailVerifyRequest):
    """
    Compare user input code with stored code.
    """
    return verify_email_code(payload.email, payload.code)


@router.post("/email-signup")
async def emailSignup(payload: UserCreate):
    """
    1. Check if user already exists
    2. if user doesn't exist, create user in Firestore
    3. Return {success: Boolean}
    """
    if payload.provider != "password":
        raise HTTPException(
            status_code=400,
            detail="email-signup endpoint only supports provider='password'.",
        )

    if not validate_user_email(payload.email):
        return {
            "success": False,
            "message": "User already exists",
        }

    # Hash Password
    hashed_pw = bcrypt.hashpw(payload.password.encode("utf-8"), bcrypt.gensalt())
    hashed_pw_str = hashed_pw.decode("utf-8")

    user_data = UserCreate(
        uid=uid,
        email=email,
        name=name,
        provider="google",
    )
