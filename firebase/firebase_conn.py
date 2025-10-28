import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

cred_path = os.getenv("FIREBASE_CRED_PATH")

# Firebase Admin SDK Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_app = firebase_admin.initialize_app(cred)
    
db = firestore.client()