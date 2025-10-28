import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer

from firebase.firebase_requests import verify_token_and_signup

router = APIRouter()
security = HTTPBearer()  # Authorization: Bearer <idToken>

load_dotenv()

# JWT Creation
JWT_SECRET = os.getenv("JWT_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTE = 60 * 24  # 1 day


def create_jwt(payload: dict):
    expire = datetime.now() + timedelta(minutes=JWT_EXPIRE_MINUTE)
    payload.update({"exp": expire})
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


@router.post("/api/googleLogin")
async def signup_or_login(response: Response, token=Depends(security)):
    try:
        decoded_token = verify_token_and_signup(token.credentials)
        uid = decoded_token["uid"]
        email = decoded_token.get("email")

        # JWT Payload
        jwt_payload = {"uid": uid, "email": email}
        jwt_token = create_jwt(jwt_payload)

        # Set up HttpOnly Cookies
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            secure=False,  # True when deployed
            samesite="lax",
            max_age=JWT_EXPIRE_MINUTE * 60 * 15,
            path="/",
        )

        return {"message": "Login Successful", "uid": uid, "email": email}

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")


@router.get("/api/isLoggedIn")
async def isLoggedIn(request: Request):
    token = request.cookies.get("access_token")

    print(request.cookies)

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"uid": payload["uid"], "email": payload["email"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
