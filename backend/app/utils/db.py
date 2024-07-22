from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.database_name]
users_collection = db["Users"]  # Cambia esto a "Users" con U mayúscula