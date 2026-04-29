import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId

from backend.database import get_database
from backend.models import UserCreate, UserResponse, UserInDB, Token, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key_for_foodshare_mumbai")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=payload.get("role"))
    except JWTError:
        raise credentials_exception

    db = get_database()
    user_doc = await db.users.find_one({"email": token_data.email})
    if user_doc is None:
        raise credentials_exception
    
    # Map _id objectId to string representation
    user_doc["_id"] = str(user_doc["_id"])
    return UserInDB(**user_doc)

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    db = get_database()
    normalized_email = user.email.strip().lower()
    existing_user = await db.users.find_one({"email": normalized_email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict.pop("password")
    user_dict["email"] = normalized_email
    user_dict["hashed_password"] = hashed_password
    user_dict["points"] = 0
    user_dict["meals_donated"] = 0
    user_dict["badges"] = []
    
    # Auto-verify admin users, others need verification
    if user_dict["role"] == "admin":
        user_dict["is_verified"] = True
    else:
        user_dict["is_verified"] = False
    
    if user_dict["role"] == "volunteer" and user_dict.get("is_nss"):
        user_dict["badges"].append("NSS Helper")
    
    new_user = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": new_user.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    return UserResponse(**created_user)

from fastapi import Form

@router.post("/token", response_model=Token)
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...)
):
    db = get_database()
    normalized_email = username.strip().lower()
    user = await db.users.find_one({"email": normalized_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not registered. Please create an account.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user.get("role")}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return UserResponse(**current_user.dict(by_alias=True))

# Admin-only endpoints
async def get_current_admin(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/admin/analytics")
async def get_admin_analytics(admin: UserInDB = Depends(get_current_admin)):
    db = get_database()
    
    # Get user statistics
    total_users = await db.users.count_documents({})
    verified_restaurants = await db.users.count_documents({"role": "restaurant", "is_verified": True})
    verified_ngos = await db.users.count_documents({"role": "ngo", "is_verified": True})
    verified_volunteers = await db.users.count_documents({"role": "volunteer", "is_verified": True})
    pending_verifications = await db.users.count_documents({"is_verified": False, "role": {"$ne": "admin"}})
    
    # Get donation statistics
    total_donations = await db.donations.count_documents({}) if hasattr(db, 'donations') else 0
    active_students = await db.users.count_documents({"role": "student"})
    
    # Calculate total meals served (simplified)
    total_meals_served = total_donations * 15  # Assuming 15 meals per donation
    
    # User breakdown by role
    user_breakdown = {}
    roles = ["restaurant", "ngo", "student", "volunteer", "admin"]
    for role in roles:
        verified = await db.users.count_documents({"role": role, "is_verified": True})
        unverified = await db.users.count_documents({"role": role, "is_verified": False})
        user_breakdown[role] = {"verified": verified, "unverified": unverified, "total": verified + unverified}
    
    # Recent activity (simplified - last 10 registrations)
    recent_users = await db.users.find({}, {"_id": 0, "hashed_password": 0}).sort("_id", -1).limit(10).to_list(length=None)
    
    return {
        "total_users": total_users,
        "verified_restaurants": verified_restaurants,
        "verified_ngos": verified_ngos,
        "verified_volunteers": verified_volunteers,
        "pending_verifications": pending_verifications,
        "total_donations": total_donations,
        "active_students": active_students,
        "total_meals_served": total_meals_served,
        "user_breakdown": user_breakdown,
        "recent_activity": recent_users
    }

@router.get("/admin/pending-verifications")
async def get_pending_verifications(admin: UserInDB = Depends(get_current_admin)):
    db = get_database()
    pending_users = await db.users.find(
        {"is_verified": False, "role": {"$ne": "admin"}}, 
        {"_id": 1, "name": 1, "email": 1, "role": 1, "license_no": 1, "ngo_location": 1}
    ).to_list(length=None)
    
    for user in pending_users:
        user["_id"] = str(user["_id"])
    
    return pending_users

@router.post("/admin/verify-user/{user_id}")
async def verify_user(user_id: str, admin: UserInDB = Depends(get_current_admin)):
    db = get_database()
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_verified": True}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User verified successfully"}

@router.delete("/admin/reject-user/{user_id}")
async def reject_user(user_id: str, admin: UserInDB = Depends(get_current_admin)):
    db = get_database()
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User rejected and removed"}
