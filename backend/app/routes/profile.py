from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import UserProfile
from ..schemas.schemas import UserProfileCreate, UserProfileRes
from ..database.database import get_db

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

# POST → create a new user profile
@router.post("/", response_model=UserProfileRes)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_profile = db.query(UserProfile).filter(UserProfile.email == profile.email).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Convert lists to JSON-compatible strings if using SQLite
    db_profile = UserProfile(
        name=profile.name,
        email=profile.email,
        education=profile.education,
        skills=",".join(profile.skills),       # store as comma-separated string
        projects=",".join(profile.projects),   # store as comma-separated string
        interests=",".join(profile.interests)  # store as comma-separated string
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# GET → fetch a profile by ID
@router.get("/{profile_id}", response_model=UserProfileRes)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Convert stored CSV strings back to lists
    db_profile.skills = db_profile.skills.split(",") if db_profile.skills else []
    db_profile.projects = db_profile.projects.split(",") if db_profile.projects else []
    db_profile.interests = db_profile.interests.split(",") if db_profile.interests else []

    return db_profile