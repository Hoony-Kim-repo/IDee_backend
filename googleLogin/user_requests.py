from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer

from firebase.auth_utils import create_jwt, get_current_user
from firebase.firebase_requests import verify_firebase_token
from firebase.schemas.users import UserCreate
from firebase.service.user_service import get_or_create_user

router = APIRouter()
security = HTTPBearer()  # Authorization: Bearer <idToken>


@router.post("/api/googleLogin")
async def signup_or_login(response: Response, token=Depends(security)):
    """
    1. Validate Firebase ID Token
    2. Save user data into Firestore
    3. Create server JWT and set cookie
    """
    decoded = verify_firebase_token(token.credentials)
    
    uid = decoded["uid"]
    email = decoded.get("email")
    name = decoded.get("name")
    
    user_data = UserCreate(uid=uid, email=email, name=name)

    user_record = await get_or_create_user(user_data)

    jwt_token = create_jwt({"uid": uid, "email": email})

    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )

    return {"message": "Login Successful", "user": user_record}


@router.get("/api/isLoggedIn")
async def isLoggedIn(current_user=Depends(get_current_user)):
    # Return user info from JWT
    return current_user
