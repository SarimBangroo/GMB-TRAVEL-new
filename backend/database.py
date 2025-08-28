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
        
        # Create indexes for team members
        await db.team_members.create_index([("username", 1)], unique=True)
        await db.team_members.create_index([("email", 1)], unique=True)
        await db.team_members.create_index([("role", 1)])
        await db.team_members.create_index([("isActive", 1)])
        await db.team_members.create_index([("createdAt", -1)])
        
        # Create indexes for popups
        await db.popups.create_index([("isActive", 1)])
        await db.popups.create_index([("startDate", 1)])
        await db.popups.create_index([("endDate", 1)])
        await db.popups.create_index([("createdAt", -1)])
        
        # Create indexes for site settings
        await db.site_settings.create_index([("isActive", 1)])
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")

# Collection helper functions
def get_collection(collection_name: str):
    """Get a specific collection from database."""
    return Database.db[collection_name]

# Initialize default admin and team members if not exist
async def create_default_admin():
    """Create default admin user if not exists."""
    from auth import AuthManager
    
    try:
        db = Database.db
        admin_collection = db.admins
        
        # Check if admin already exists
        existing_admin = await admin_collection.find_one({"username": "admin"})
        
        if not existing_admin:
            from models import Admin
            
            default_admin = Admin(
                username="admin",
                passwordHash=AuthManager.get_password_hash("admin123"),
                email="admin@gmbtravelskashmir.com"
            )
            
            await admin_collection.insert_one(default_admin.dict(by_alias=True))
            logger.info("Default admin user created successfully")
        
        # Create default team members
        team_collection = db.team_members
        
        existing_team_members = await team_collection.count_documents({})
        
        if existing_team_members == 0:
            from models import TeamMember, UserRole
            from datetime import datetime
            
            default_team_members = [
                TeamMember(
                    fullName="Rajesh Kumar",
                    email="rajesh.manager@gmbtravelskashmir.com", 
                    phone="+91 87654 32109",
                    username="rajesh_manager",
                    passwordHash=AuthManager.get_password_hash("manager123"),
                    role=UserRole.manager,
                    department="Operations",
                    joiningDate=datetime(2024, 2, 15),
                    packagesCreated=12,
                    clientsManaged=38
                ),
                TeamMember(
                    fullName="Priya Sharma",
                    email="priya.agent@gmbtravelskashmir.com",
                    phone="+91 76543 21098", 
                    username="priya_agent",
                    passwordHash=AuthManager.get_password_hash("agent123"),
                    role=UserRole.agent,
                    department="Sales",
                    joiningDate=datetime(2024, 3, 10),
                    packagesCreated=8,
                    clientsManaged=28
                ),
                TeamMember(
                    fullName="Amit Patel",
                    email="amit.agent@gmbtravelskashmir.com",
                    phone="+91 65432 10987",
                    username="amit_agent", 
                    passwordHash=AuthManager.get_password_hash("agent123"),
                    role=UserRole.agent,
                    department="Customer Support",
                    joiningDate=datetime(2024, 4, 5),
                    packagesCreated=5,
                    clientsManaged=15,
                    isActive=False
                )
            ]
            
            for team_member in default_team_members:
                await team_collection.insert_one(team_member.dict(by_alias=True))
            
            logger.info("Default team members created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create default admin and team members: {e}")