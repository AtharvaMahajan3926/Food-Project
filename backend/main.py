import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.routes import auth, donations, stats

app = FastAPI(title="FoodShare Mumbai API")

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    # Allow local file protocol during dev
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(donations.router, prefix="/api/donations", tags=["Donations"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])

@app.get("/api/")
def read_root():
    return {"message": "Welcome to FoodShare Mumbai API"}

from backend.database import get_database
import pymongo

@app.on_event("startup")
async def startup_db_client():
    db = get_database()
    
    # Optimize Queries: Create indexes for fast lookups on donations
    await db.donations.create_index([("status", pymongo.ASCENDING)])
    await db.donations.create_index([("created_by_id", pymongo.ASCENDING)])
    await db.donations.create_index([("ngo_id", pymongo.ASCENDING)])
    await db.donations.create_index([("volunteer_id", pymongo.ASCENDING)])
    await db.donations.create_index([("created_at", pymongo.DESCENDING)])
    
    # Optimize Queries: Create indexes for users collection
    await db.users.create_index([("email", pymongo.ASCENDING)], unique=True)
    await db.users.create_index([("role", pymongo.ASCENDING)])
    await db.users.create_index([("points", pymongo.DESCENDING)])
