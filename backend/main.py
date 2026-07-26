import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.routes import auth, donations, stats
from backend.database import get_database
import pymongo
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
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
    except Exception as e:
        print(f"Warning: Database index initialization skipped or failed: {e}")
    yield

app = FastAPI(title="FoodShare Mumbai API", lifespan=lifespan)

import os

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

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in origins:
    origins.append(frontend_url)
    origins.append(frontend_url.rstrip("/"))

from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
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

