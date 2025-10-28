"""
JWT Creation / Verification
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any
import jwt
import time
from fastapi import HTTPException

load_dotenv()

# JWT Creation
JWT_SECRET = os.getenv("JWT_KEY")
JWT_ALGORITHM = os.getenv("FIREBASE_ALGORITHM")
JWT_EXPIRE_MINUTE = 60 * 60 * 24  # 1 day


def create_jwt(payload: Dict[str, Any], exp_seconds: int = None) -> str:
    now = int(time.time())
    exp = now + (exp_seconds if exp_seconds is not None else JWT_EXPIRE_MINUTE)
    to_encode = {"iat": now, "exp": exp, **payload}
    
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token

def verify_jwt(token: str) -> Dict[str, Any]:
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT")

# FastAPI Dependency: Read from cookies first, if no token found in cookies, check Bearer Token from Authorization header
from fastapi import Depends, Request

async def get_token_from_request(request:Request) -> str | None:
    # If access_token is in cookie, use it
    token = request.cookies.get('access_token')
    if token:
        return token
    
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(" ", 1)[1]
    
    return None

async def get_current_user(token: str = Depends(get_token_from_request)):
    if not token:
        raise HTTPException(status_code=401, detila="Not authenticated")
    return verify_jwt(token)