from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel

from backend.database import get_database
from backend.models import DonationCreate, DonationInDB
from backend.routes.auth import get_current_user, UserInDB

router = APIRouter()

class AcceptBody(BaseModel):
    drop_off_address: str
    drop_off_lat: Optional[float] = None
    drop_off_lng: Optional[float] = None

@router.post("/", response_model=DonationInDB)
async def create_donation(donation: DonationCreate, current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "restaurant":
        raise HTTPException(status_code=403, detail="Only restaurants can create donations")
    
    if not current_user.is_verified:
        raise HTTPException(status_code=403, detail="Your account is pending admin verification. Please wait for approval.")

    db = get_database()
    donation_dict = donation.dict()
    donation_dict["status"] = "pending"
    donation_dict["created_by_id"] = str(current_user.id)
    donation_dict["created_by_name"] = current_user.name
    
    import datetime
    donation_dict["created_at"] = datetime.datetime.utcnow()

    new_donation = await db.donations.insert_one(donation_dict)
    created_donation = await db.donations.find_one({"_id": new_donation.inserted_id})
    created_donation["_id"] = str(created_donation["_id"])
    
    # Award points to the restaurant
    await db.users.update_one({"_id": ObjectId(current_user.id)}, {"$inc": {"points": 10}})

    return DonationInDB(**created_donation)

@router.get("/", response_model=List[DonationInDB])
async def get_donations(current_user: UserInDB = Depends(get_current_user)):
    db = get_database()
    query = {}
    
    if current_user.role == "restaurant":
        query = {"created_by_id": str(current_user.id)}
    elif current_user.role == "ngo":
        query = {"$or": [{"status": "pending"}, {"ngo_id": str(current_user.id)}]}
    elif current_user.role == "volunteer":
        query = {"$or": [{"status": "accepted"}, {"volunteer_id": str(current_user.id)}]}
        
    cursor = db.donations.find(query).sort("created_at", -1)
    donations = await cursor.to_list(length=100)
    
    for doc in donations:
        doc["_id"] = str(doc["_id"])
        
    return [DonationInDB(**doc) for doc in donations]

@router.put("/{donation_id}/accept")
async def accept_donation(donation_id: str, body: AcceptBody, current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "ngo":
        raise HTTPException(status_code=403, detail="Only NGOs can accept donations")

    db = get_database()
    result = await db.donations.update_one(
        {"_id": ObjectId(donation_id), "status": "pending"},
        {"$set": {
            "status": "accepted",
            "ngo_id": str(current_user.id),
            "ngo_name": current_user.name,
            "drop_off_address": body.drop_off_address,
            "drop_off_lat": body.drop_off_lat,
            "drop_off_lng": body.drop_off_lng,
        }}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Donation not found or already accepted")
        
    return {"message": "Donation accepted", "drop_off_address": body.drop_off_address}

@router.put("/{donation_id}/claim")
async def claim_donation(donation_id: str, current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "volunteer":
        raise HTTPException(status_code=403, detail="Only volunteers can claim deliveries")

    db = get_database()
    result = await db.donations.update_one(
        {"_id": ObjectId(donation_id), "status": "accepted"},
        {"$set": {"status": "en_route", "volunteer_id": str(current_user.id), "volunteer_name": current_user.name}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Donation not found or not ready for pickup")
        
    return {"message": "Donation claimed"}

@router.put("/{donation_id}/deliver")
async def deliver_donation(donation_id: str, current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "volunteer":
        raise HTTPException(status_code=403, detail="Only volunteers can claim deliveries")

    db = get_database()
    result = await db.donations.update_one(
        {"_id": ObjectId(donation_id), "status": "en_route", "volunteer_id": str(current_user.id)},
        {"$set": {"status": "delivered"}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Donation not found or not assigned to you")
        
    # Award points/hours to volunteer
    await db.users.update_one({"_id": ObjectId(current_user.id)}, {"$inc": {"points": 2}})
        
    return {"message": "Donation delivered"}
