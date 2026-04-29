import asyncio
import datetime
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient

# Setup DB connection
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.foodshare_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    print("Seeding database...")
    
    # 1. Clear existing collections to avoid duplicates if run multiple times
    await db.users.drop()
    await db.donations.drop()
    print("Cleared existing collections.")

    # 2. Create Users
    hashed_pwd = pwd_context.hash("password123")
    
    users = [
        {
            "name": "Admin User",
            "email": "admin@test.com",
            "role": "admin",
            "hashed_password": hashed_pwd,
            "points": 0,
            "badges": ["System Admin"],
            "is_verified": True
        },
        {
            "name": "Priya Restaurant",
            "email": "restaurant@test.com",
            "role": "restaurant",
            "hashed_password": hashed_pwd,
            "points": 2840,
            "badges": ["Bronze", "Silver"],
            "is_verified": True
        },
        {
            "name": "Akanksha Foundation",
            "email": "ngo@test.com",
            "role": "ngo",
            "hashed_password": hashed_pwd,
            "points": 0,
            "badges": [],
            "license_no": "NGO2024001",
            "ngo_lat": 19.0760,
            "ngo_lng": 72.8777,
            "is_verified": True
        },
        {
            "name": "Rahul Sharma",
            "email": "student@test.com",
            "role": "student",
            "hashed_password": hashed_pwd,
            "points": 150,
            "badges": ["Active"],
            "is_verified": True
        },
        {
            "name": "Anjali NSS",
            "email": "volunteer@test.com",
            "role": "volunteer",
            "hashed_password": hashed_pwd,
            "points": 50,
            "badges": ["NSS Helper"],
            "is_nss": True,
            "is_verified": True
        }
    ]
    
    # Insert users
    await db.users.insert_many(users)
    print("Inserted dummy users (Tables 'users' created).")
    
    # Fetch user IDs for relations
    rest_user = await db.users.find_one({"email": "restaurant@test.com"})
    ngo_user = await db.users.find_one({"email": "ngo@test.com"})
    vol_user = await db.users.find_one({"email": "volunteer@test.com"})

    # 3. Create Donations
    donations = [
        {
            "food_name": "Chicken Biryani",
            "quantity": "15 portions, 1.2kg",
            "category": "Cooked Meal",
            "expiry_time": "21:00",
            "date": "2026-04-04",
            "location": "Priya Restro, Bandra",
            "special_instructions": "Needs hot boxes",
            "status": "delivered",
            "created_by_id": str(rest_user["_id"]),
            "created_by_name": rest_user["name"],
            "ngo_id": str(ngo_user["_id"]),
            "ngo_name": ngo_user["name"],
            "volunteer_id": str(vol_user["_id"]),
            "volunteer_name": vol_user["name"],
            "created_at": datetime.datetime.utcnow() - datetime.timedelta(hours=5)
        },
        {
            "food_name": "Bread & Pastries",
            "quantity": "30 pieces",
            "category": "Bakery Items",
            "expiry_time": "20:30",
            "date": "2026-04-04",
            "location": "Priya Restro, Bandra",
            "status": "accepted",
            "created_by_id": str(rest_user["_id"]),
            "created_by_name": rest_user["name"],
            "ngo_id": str(ngo_user["_id"]),
            "ngo_name": ngo_user["name"],
            "volunteer_id": None,
            "volunteer_name": None,
            "created_at": datetime.datetime.utcnow() - datetime.timedelta(hours=2)
        },
        {
            "food_name": "Mixed Salads",
            "quantity": "10 portions",
            "category": "Raw Vegetables",
            "expiry_time": "19:45",
            "date": "2026-04-04",
            "location": "Priya Restro, Bandra",
            "status": "pending",
            "created_by_id": str(rest_user["_id"]),
            "created_by_name": rest_user["name"],
            "ngo_id": None,
            "ngo_name": None,
            "volunteer_id": None,
            "volunteer_name": None,
            "created_at": datetime.datetime.utcnow()
        }
    ]
    
    await db.donations.insert_many(donations)
    print("Inserted dummy donations (Tables 'donations' created).")
    print("Database `foodshare_db` setup complete!")

if __name__ == "__main__":
    asyncio.run(seed_database())
