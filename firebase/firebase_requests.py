from .firebase_conn import db
from firebase_admin import auth
from fastapi.security import HTTPBearer
from fastapi import HTTPException

security = HTTPBearer()

def verify_token_and_signup(token):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        email = decoded_token.get("email")
        
        # Firestore users collection reference
        users_ref = db.collection("users")
        user_doc = users_ref.document(uid).get()
        
        if not user_doc.exists:
            users_ref.document(uid).set({"email": email})
            print(f"New user signed up: {email}")
        else :
            print(f"Existing user login: {email}")
            
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")