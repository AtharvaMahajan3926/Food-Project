import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL") or os.getenv("MONGODB_URI") or "mongodb://localhost:27017"
_clients = {}

def get_database():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    
    if loop not in _clients or _clients[loop] is None:
        _clients[loop] = AsyncIOMotorClient(MONGO_URL)
    
    return _clients[loop].foodshare_db

