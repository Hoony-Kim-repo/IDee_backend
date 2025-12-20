from fastapi import APIRouter, Form, UploadFile

from app.core.firebase import bucket

router = APIRouter(prefix="/profile", tags=["Profiles"])


@router.post("")
async def create_profile(
    fullName: str = Form(...),
    nickname: str = Form(None),
    phoneNumber: str = Form(None),
    dob: str = Form(None),
    bio: str = Form(None),
    profilePicture: UploadFile = None,
):
    return {
        "fullName": fullName,
        "nickname": nickname,
        "phoneNumber": phoneNumber,
        "dob": dob,
        "bio": bio,
        "profilePictureFileName": profilePicture.filename if profilePicture else None,
        "profilePictureFileType": (
            profilePicture.content_type if profilePicture else None
        ),
    }


@router.post("/test-upload")
async def test_upload(fullName: str = Form(...), profilePicture: UploadFile = None):
    print("Received fullName:", fullName)
    image_url = None

    if profilePicture:
        # Upload the file to Firebase Storage
        blob = bucket.blob(f"profile_images/{fullName}/{profilePicture.filename}")
        blob.upload_from_file(
            profilePicture.file, content_type=profilePicture.content_type
        )

        # Public URL
        blob.make_public()
        image_url = blob.public_url

    return {
        "fullName": fullName,
        "fileName": profilePicture.filename if profilePicture else None,
        "image_url": image_url,
    }
