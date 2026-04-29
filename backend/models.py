from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str # "restaurant", "ngo", "student", "volunteer", "admin"
    license_no: Optional[str] = None
    ngo_location: Optional[str] = None
    ngo_lat: Optional[float] = None
    ngo_lng: Optional[float] = None
    is_nss: Optional[bool] = False
    is_verified: bool = False  # Admin verification status

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    points: int = 0
    meals_donated: int = 0
    badges: List[str] = []

class UserResponse(UserBase):
    id: str = Field(alias="_id")
    points: int
    meals_donated: int
    badges: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class DonationCreate(BaseModel):
    food_name: str
    quantity: str
    meals_provided: int = 15  # simple assumption based on portions
    category: str
    expiry_time: str
    date: str
    location: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    special_instructions: Optional[str] = None

class AdminAnalytics(BaseModel):
    total_users: int
    verified_restaurants: int
    verified_ngos: int
    verified_volunteers: int
    pending_verifications: int
    total_donations: int
    active_students: int
    total_meals_served: int
    user_breakdown: dict
    recent_activity: List[dict]

class DonationInDB(DonationCreate):
    id: str = Field(alias="_id")
    status: str = "pending" # pending, accepted, en_route, delivered
    created_by_id: str
    created_by_name: str
    ngo_id: Optional[str] = None
    ngo_name: Optional[str] = None
    drop_off_address: Optional[str] = None
    drop_off_lat: Optional[float] = None
    drop_off_lng: Optional[float] = None
    volunteer_id: Optional[str] = None
    volunteer_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
