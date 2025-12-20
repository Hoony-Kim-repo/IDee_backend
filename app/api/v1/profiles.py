from fastapi import APIRouter, Form, UploadFile
from firebase_admin import firestore

from app.core.firebase import bucket, db

router = APIRouter(prefix="/profile", tags=["Profiles"])


@router.post("")
async def create_profile(
    uid: str = Form(...),
    fullName: str = Form(...),
    nickname: str = Form(None),
    phoneNumber: str = Form(None),
    dob: str = Form(None),
    bio: str = Form(None),
    profilePicture: UploadFile = None,
):
    image_url = None
    image_path = None

    if profilePicture:
        image_path = f"profile_images/{uid}/{profilePicture.filename}"
        blob = bucket.blob(image_path)
        blob.upload_from_file(
            profilePicture.file, content_type=profilePicture.content_type
        )
        blob.make_public()
        image_url = blob.public_url

    profile_data = {
        "uid": uid,
        "fullName": fullName,
        "nickname": nickname,
        "phoneNumber": phoneNumber,
        "dob": dob,
        "bio": bio,
        "profileImage": {
            "url": image_url,
            "path": image_path,
        },
        "createdAt": firestore.SERVER_TIMESTAMP,
        "updatedAt": firestore.SERVER_TIMESTAMP,
    }

    try:
        db.collection("profiles").document(uid).set(profile_data)
    except Exception as e:
        return {
            "status": 500,
            "data": {"message": "Failed to create profile", "detail": str(e)},
        }

    return {"status": 200, "data": profile_data}
