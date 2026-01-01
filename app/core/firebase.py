import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth, credentials, firestore, storage

load_dotenv()

cred_path = os.getenv("FIREBASE_CRED_PATH")
bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")


# ------------------- Firebase Initialization ------------------- #
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})


init_firebase()

# ------------------- Clients ------------------- #
db = firestore.client()
bucket = storage.bucket()
