import json
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from firebase_admin import firestore

from app.core.firebase import bucket, db
from app.core.firebase_auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Profiles"])


@router.post("")
async def create_profile(
    current_user=Depends(get_current_user),
    fullName: str = Form(...),
    nickname: str = Form(None),
    phoneNumber: str = Form(None),
    dob: str = Form(None),
    bio: str = Form(None),
    profilePicture: UploadFile | None = File(None),
    tags: str = Form("[]"),
):
    print("Post create profile")
    try:
        uid = current_user["uid"]

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

        try:
            tags_list = json.loads(tags)

        except Exception:
            tags_list = []

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
            "tags": tags_list,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
        }

        db.collection("profiles").document(uid).set(profile_data)

        response_data = {
            "fullName": fullName,
            "nickname": nickname,
            "phoneNumber": phoneNumber,
            "dob": dob,
            "bio": bio,
            "profileImage": {
                "url": image_url,
                "path": image_path,
            },
            "tags": tags_list,
        }

        return {"status_code": 200, "data": response_data}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": "Failed to create profile", "detail": str(e)},
        )


@router.put("/me")
async def update_profile(
    current_user=Depends(get_current_user),
    fullName: str = Form(None),
    nickname: str = Form(None),
    phoneNumber: str = Form(None),
    dob: str = Form(None),
    bio: str = Form(None),
    profilePicture: UploadFile | None = File(None),
):
    """
    Update a user's profile.
    If a new profile picture is provided, the old one will be deleted.
    """
    uid = current_user["uid"]

    try:
        doc_ref = db.collection("profiles").document(uid)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="Profile not found")

        existing_data = doc.to_dict()

        update_data = {"updatedAt": firestore.SERVER_TIMESTAMP}

        if fullName is not None:
            update_data["fullName"] = fullName
        if nickname is not None:
            update_data["nickname"] = nickname
        if phoneNumber is not None:
            update_data["phoneNumber"] = phoneNumber
        if dob is not None:
            update_data["dob"] = dob
        if bio is not None:
            update_data["bio"] = bio

        if profilePicture:
            # Delete old image if exists
            old_image_path = existing_data.get("profileImage", {}).get("path")

            if old_image_path:
                old_blob = bucket.blob(old_image_path)
                if old_blob.exists():
                    old_blob.delete()

            # Upload new image
            filename = f"{uuid.uuid4()}_{profilePicture.filename}"
            new_image_path = f"profile_images/{uid}/{filename}"
            new_blob = bucket.blob(new_image_path)
            new_blob.upload_from_file(
                profilePicture.file, content_type=profilePicture.content_type
            )
            new_blob.make_public()
            new_image_url = new_blob.public_url

            update_data["profileImage"] = {
                "url": new_image_url,
                "path": new_image_path,
            }

        doc_ref.update(update_data)

        updated_doc = doc_ref.get()

        return {
            "message": "Profile updated successfully",
            "updated_profile": updated_doc.to_dict(),
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": "Failed to update profile", "detail": str(e)},
        )
