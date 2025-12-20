import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth, credentials, firestore, storage

load_dotenv()


# ------------------- Firebase Initialization ------------------- #
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("FIREBASE_CRED_PATH"))
        firebase_admin.initialize_app(
            cred, {"storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET")}
        )


init_firebase()

# ------------------- Clients ------------------- #
db = firestore.client()
bucket = storage.bucket()


# ------------------- Auth ------------------- #
def verify_firebase_token(token):
    """
    Verify Firebase ID token and return decoded payload.
    This module only handles Firebase Auth logic.
    """
    decoded_token = auth.verify_id_token(token)
    return auth.verify_id_token(token)
