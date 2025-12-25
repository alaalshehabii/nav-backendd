from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import UserModel
from serializers.user import UserSignUp, UserSignIn
from schemas.user import UserUpdate
from dependencies.get_current_user import get_current_user

router = APIRouter()

# AUTH

@router.post("/users/signup")
def sign_up(user: UserSignUp, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Admin rule 
    is_admin = user.email == "admin@gmail.com"

    # Create new user
    new_user = UserModel(
        username=user.username,
        email=user.email,
        is_admin=is_admin
    )

    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = new_user.generate_token()
    return {"token": token}


@router.post("/users/signin")
def sign_in(credentials: UserSignIn, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        UserModel.email == credentials.email
    ).first()

    if not user or not user.verify_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = user.generate_token()
    return {"token": token}


# USER PROFILE CRUD


@router.put("/users/me")
def update_profile(
    updated_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Prevent admin email change
    if current_user.is_admin and updated_user.email != "admin@gmail.com":
        raise HTTPException(
            status_code=400,
            detail="Admin email cannot be changed"
        )

    current_user.username = updated_user.username
    current_user.email = updated_user.email

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin
    }


@router.delete("/users/me")
def delete_account(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Prevent admin deletion
    if current_user.is_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin account cannot be deleted"
        )

    db.delete(current_user)
    db.commit()

    return {"message": "Account deleted successfully"}
