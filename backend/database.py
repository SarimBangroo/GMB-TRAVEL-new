from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

# Initialize database connection
def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    return Database.db

async def connect_to_mongo():
    """Create database connection."""
    try:
        mongo_url = os.environ.get('MONGO_URL')
        if not mongo_url:
            raise ValueError("MONGO_URL environment variable not set")
        
        Database.client = AsyncIOMotorClient(mongo_url)
        Database.db = Database.client[os.environ.get('DB_NAME', 'gmb_travels')]
        
        # Test the connection
        await Database.client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection."""
    if Database.client:
        Database.client.close()
        logger.info("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for better performance."""
    try:
        db = Database.db
        
        # Create indexes for packages
        await db.packages.create_index([("title", 1)])
        await db.packages.create_index([("status", 1)])
        await db.packages.create_index([("createdAt", -1)])
        
        # Create indexes for bookings
        await db.bookings.create_index([("email", 1)])
        await db.bookings.create_index([("status", 1)])
        await db.bookings.create_index([("createdAt", -1)])
        
        # Create indexes for testimonials
        await db.testimonials.create_index([("status", 1)])
        await db.testimonials.create_index([("rating", -1)])
        
        # Create indexes for cab bookings
        await db.cab_bookings.create_index([("email", 1)])
        await db.cab_bookings.create_index([("status", 1)])
        await db.cab_bookings.create_index([("pickupDate", 1)])
        
        # Create indexes for contact inquiries
        await db.contact_inquiries.create_index([("status", 1)])
        await db.contact_inquiries.create_index([("createdAt", -1)])
        
        # Create indexes for gallery images
        await db.gallery_images.create_index([("category", 1)])
        await db.gallery_images.create_index([("isActive", 1)])
        
        # Create unique index for admin usernames
        await db.admins.create_index([("username", 1)], unique=True)
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")

# Collection helper functions
def get_collection(collection_name: str):
    """Get a specific collection from database."""
    return Database.db[collection_name]

# Initialize default admin if not exists
async def create_default_admin():
    """Create default admin user if not exists."""
    from .auth import AuthManager
    
    try:
        db = Database.db
        admin_collection = db.admins
        
        # Check if admin already exists
        existing_admin = await admin_collection.find_one({"username": "admin"})
        
        if not existing_admin:
            from .models import Admin
            
            default_admin = Admin(
                username="admin",
                passwordHash=AuthManager.get_password_hash("admin123"),
                email="admin@gmbtravelskashmir.com"
            )
            
            await admin_collection.insert_one(default_admin.dict(by_alias=True))
            logger.info("Default admin user created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create default admin: {e}")