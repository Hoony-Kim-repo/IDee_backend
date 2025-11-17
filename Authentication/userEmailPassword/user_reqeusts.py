from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr

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
            # "email": payload.email,
            # "verification_code": verification_code,  # For testing purposes only
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare-email-code")
async def compareEmailVerificationCode(payload: EmailVerifyRequest):
    """
    Compare user input code with stored code.
    """
    if verify_email_code(payload.email, payload.code):
        return {"success": True, "message": "Email verified successfully."}
    else:
        return {"success": False, "message": "Invalid or expired verification code."}


@router.post("/emailSignup")
async def emailSignup(response: Response):
    """
    1. Validate Email format
    2. Validate Password format
    3. Check if user already exists
    4. if user doesn't exist, create user in Firestore
    5. Create Server JWT and set cookie
    """

    print(response.body)
