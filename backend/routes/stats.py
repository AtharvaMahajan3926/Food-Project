from fastapi import APIRouter, Depends
from typing import Dict, List
from backend.database import get_database
from backend.models import UserInDB, UserResponse
from backend.routes.auth import get_current_user
from bson import ObjectId

router = APIRouter()

@router.get("/overview")
async def get_overview_stats(current_user: UserInDB = Depends(get_current_user)):
    db = get_database()
    
    # Calculate live current stats
    if current_user.role == "restaurant":
        pipeline = [
            {"$match": {"created_by_id": str(current_user.id), "status": "delivered"}},
            {"$group": {"_id": None, "total_meals": {"$sum": "$meals_provided"}}}
        ]
        res = await db.donations.aggregate(pipeline).to_list(length=1)
        meals = res[0]["total_meals"] if res else 0
        
        counts = await db.donations.count_documents({"created_by_id": str(current_user.id)})
        return {
            "total_donations": counts,
            "points": current_user.points,
            "meals_saved": meals,
            "rank": "Top 10%" if current_user.points > 100 else "New"
        }
    
    elif current_user.role == "volunteer":
        counts = await db.donations.count_documents({"volunteer_id": str(current_user.id), "status": "delivered"})
        hours = counts * 2 # 2 hours simulated per delivery
        return {
            "deliveries": counts,
            "hours": hours,
            "rank": "Top 15%" if counts > 10 else "New",
            "certificates": 1 if hours >= 50 else 0
        }
        
    elif current_user.role == "ngo":
        counts = await db.donations.count_documents({"ngo_id": str(current_user.id), "status": "delivered"})
        beneficiaries = counts * 15 # rough estimate
        pending = await db.donations.count_documents({"status": "pending"})
        active = await db.donations.count_documents({"ngo_id": str(current_user.id), "status": "en_route"})
        return {
            "pending": pending,
            "active": active,
            "meals": counts * 15,
            "beneficiaries": beneficiaries
        }
    
    else:
        # student
        return {
            "discounts": 8,
            "saved": 640
        }

import time

_leaderboard_cache = {"data": None, "timestamp": 0}

@router.get("/leaderboard", response_model=List[dict])
async def get_leaderboard():
    global _leaderboard_cache
    if _leaderboard_cache["data"] and time.time() - _leaderboard_cache["timestamp"] < 15:
        return _leaderboard_cache["data"]

    db = get_database()
    # Rank all restaurants by points
    cursor = db.users.find({"role": "restaurant"}).sort("points", -1).limit(10)
    users = await cursor.to_list(length=10)
    
    leaderboard = []
    for i, u in enumerate(users):
        rank_sym = str(i+1)
        if i == 0: rank_sym = "🥇"
        elif i == 1: rank_sym = "🥈"
        elif i == 2: rank_sym = "🥉"
        
        leaderboard.append({
            "rank": rank_sym,
            "name": u["name"],
            "meals": (u.get("points", 0) // 10) * 15, # approximate
            "pts": u.get("points", 0),
            "user_id": str(u["_id"])
        })
        
    _leaderboard_cache["data"] = leaderboard
    _leaderboard_cache["timestamp"] = time.time()
    return leaderboard

_impact_cache = {"data": None, "timestamp": 0}

@router.get("/impact")
async def get_impact():
    global _impact_cache
    if _impact_cache["data"] and time.time() - _impact_cache["timestamp"] < 5:
        return _impact_cache["data"]

    db = get_database()
    pipeline = [
        {"$match": {"status": "delivered"}},
        {"$group": {"_id": None, "total": {"$sum": "$meals_provided"}}}
    ]
    res = await db.donations.aggregate(pipeline).to_list(length=1)
    meals = res[0]["total"] if res else 0
    
    data = {
        "meals_donated": meals,
        "kg_saved": meals * 0.4, # ~400g per meal
        "people_helped": meals, # 1 meal = 1 person roughly
        "co2_prevented": meals * 0.8
    }
    
    _impact_cache["data"] = data
    _impact_cache["timestamp"] = time.time()
    return data
