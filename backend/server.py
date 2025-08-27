from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging
from pathlib import Path
from typing import List, Optional
import shutil
import uuid
from datetime import datetime

# Import models and database
from models import *
from database import connect_to_mongo, close_mongo_connection, get_database, create_default_admin
from auth import AuthManager, admin_required

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# App lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    await create_default_admin()
    yield
    # Shutdown
    await close_mongo_connection()

# Create FastAPI app
app = FastAPI(title="G.M.B Travels Kashmir API", version="1.0.0", lifespan=lifespan)

# Create API router
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "G.M.B Travels Kashmir API is running"}

# Authentication endpoints
@api_router.post("/auth/login", response_model=TokenResponse)
async def admin_login(login_data: AdminLogin):
    """Admin login endpoint."""
    try:
        db = get_database()
        admin_collection = db.admins
        
        # Find admin by username
        admin = await admin_collection.find_one({"username": login_data.username})
        
        if not admin or not AuthManager.verify_password(login_data.password, admin["passwordHash"]):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        # Update last login
        await admin_collection.update_one(
            {"_id": admin["_id"]},
            {"$set": {"lastLogin": datetime.utcnow()}}
        )
        
        # Create access token
        access_token = AuthManager.create_access_token(
            data={"sub": admin["username"], "user_id": str(admin["_id"])}
        )
        
        return TokenResponse(access_token=access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/auth/verify")
async def verify_token(current_admin: dict = Depends(admin_required)):
    """Verify admin token."""
    return {"valid": True, "admin": current_admin["sub"]}

# Package endpoints
@api_router.get("/packages", response_model=List[Package])
async def get_packages():
    """Get all active packages (public)."""
    try:
        db = get_database()
        packages_collection = db.packages
        
        packages_cursor = packages_collection.find({"status": "active"}).sort("createdAt", -1)
        packages = await packages_cursor.to_list(length=100)
        
        return [Package(**package) for package in packages]
        
    except Exception as e:
        logger.error(f"Get packages error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch packages")

@api_router.get("/packages/{package_id}", response_model=Package)
async def get_package_by_id(package_id: str):
    """Get package by ID (public)."""
    try:
        db = get_database()
        packages_collection = db.packages
        
        package = await packages_collection.find_one({"_id": package_id, "status": "active"})
        
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        
        return Package(**package)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get package error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch package")

# Admin package endpoints
@api_router.get("/admin/packages", response_model=List[Package])
async def admin_get_packages(current_admin: dict = Depends(admin_required)):
    """Get all packages (admin)."""
    try:
        db = get_database()
        packages_collection = db.packages
        
        packages_cursor = packages_collection.find({}).sort("createdAt", -1)
        packages = await packages_cursor.to_list(length=1000)
        
        return [Package(**package) for package in packages]
        
    except Exception as e:
        logger.error(f"Admin get packages error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch packages")

@api_router.post("/admin/packages", response_model=Package)
async def create_package(package_data: PackageCreate, current_admin: dict = Depends(admin_required)):
    """Create new package (admin)."""
    try:
        db = get_database()
        packages_collection = db.packages
        
        package = Package(**package_data.dict())
        
        result = await packages_collection.insert_one(package.dict(by_alias=True))
        package.id = str(result.inserted_id)
        
        return package
        
    except Exception as e:
        logger.error(f"Create package error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create package")

@api_router.put("/admin/packages/{package_id}", response_model=Package)
async def update_package(package_id: str, package_data: PackageUpdate, current_admin: dict = Depends(admin_required)):
    """Update package (admin)."""
    try:
        db = get_database()
        packages_collection = db.packages
        
        # Check if package exists
        existing_package = await packages_collection.find_one({"_id": package_id})
        if not existing_package:
            raise HTTPException(status_code=404, detail="Package not found")
        
        # Update package
        update_data = {k: v for k, v in package_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await packages_collection.update_one(
            {"_id": package_id},
            {"$set": update_data}
        )
        
        # Return updated package
        updated_package = await packages_collection.find_one({"_id": package_id})
        return Package(**updated_package)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update package error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update package")

@api_router.delete("/admin/packages/{package_id}")
async def delete_package(package_id: str, current_admin: dict = Depends(admin_required)):
    """Delete package (admin)."""
    try:
        db = get_database()
        packages_collection = db.packages
        
        result = await packages_collection.delete_one({"_id": package_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Package not found")
        
        return {"message": "Package deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete package error: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete package")

# Booking endpoints
@api_router.post("/bookings", response_model=Booking)
async def create_booking(booking_data: BookingCreate):
    """Create new booking (public)."""
    try:
        db = get_database()
        bookings_collection = db.bookings
        
        booking = Booking(**booking_data.dict())
        
        result = await bookings_collection.insert_one(booking.dict(by_alias=True))
        booking.id = str(result.inserted_id)
        
        return booking
        
    except Exception as e:
        logger.error(f"Create booking error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create booking")

@api_router.get("/admin/bookings", response_model=List[Booking])
async def admin_get_bookings(current_admin: dict = Depends(admin_required)):
    """Get all bookings (admin)."""
    try:
        db = get_database()
        bookings_collection = db.bookings
        
        bookings_cursor = bookings_collection.find({}).sort("createdAt", -1)
        bookings = await bookings_cursor.to_list(length=1000)
        
        return [Booking(**booking) for booking in bookings]
        
    except Exception as e:
        logger.error(f"Admin get bookings error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch bookings")

# Testimonials endpoints
@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials():
    """Get approved testimonials (public)."""
    try:
        db = get_database()
        testimonials_collection = db.testimonials
        
        testimonials_cursor = testimonials_collection.find({"status": "approved"}).sort("createdAt", -1)
        testimonials = await testimonials_cursor.to_list(length=100)
        
        return [Testimonial(**testimonial) for testimonial in testimonials]
        
    except Exception as e:
        logger.error(f"Get testimonials error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch testimonials")

@api_router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial_data: TestimonialCreate):
    """Submit testimonial (public)."""
    try:
        db = get_database()
        testimonials_collection = db.testimonials
        
        testimonial = Testimonial(**testimonial_data.dict())
        
        result = await testimonials_collection.insert_one(testimonial.dict(by_alias=True))
        testimonial.id = str(result.inserted_id)
        
        return testimonial
        
    except Exception as e:
        logger.error(f"Create testimonial error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create testimonial")

# Cab booking endpoints
@api_router.post("/cab-bookings", response_model=CabBooking)
async def create_cab_booking(cab_booking_data: CabBookingCreate):
    """Create cab booking (public)."""
    try:
        db = get_database()
        cab_bookings_collection = db.cab_bookings
        
        cab_booking = CabBooking(**cab_booking_data.dict())
        
        result = await cab_bookings_collection.insert_one(cab_booking.dict(by_alias=True))
        cab_booking.id = str(result.inserted_id)
        
        return cab_booking
        
    except Exception as e:
        logger.error(f"Create cab booking error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create cab booking")

# Contact endpoints
@api_router.post("/contact", response_model=ContactInquiry)
async def create_contact_inquiry(contact_data: ContactCreate):
    """Submit contact inquiry (public)."""
    try:
        db = get_database()
        contact_collection = db.contact_inquiries
        
        inquiry = ContactInquiry(**contact_data.dict())
        
        result = await contact_collection.insert_one(inquiry.dict(by_alias=True))
        inquiry.id = str(result.inserted_id)
        
        return inquiry
        
    except Exception as e:
        logger.error(f"Create contact inquiry error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create inquiry")

# File upload endpoint
@api_router.post("/admin/upload")
async def upload_image(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    category: str = Form("gallery"),
    current_admin: dict = Depends(admin_required)
):
    """Upload image (admin)."""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique filename
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create database entry
        db = get_database()
        images_collection = db.gallery_images
        
        image = GalleryImage(
            title=title,
            description=description,
            imageUrl=f"/uploads/{unique_filename}",
            category=category
        )
        
        result = await images_collection.insert_one(image.dict(by_alias=True))
        
        return {
            "message": "Image uploaded successfully",
            "image_id": str(result.inserted_id),
            "image_url": f"/uploads/{unique_filename}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload image error: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")

# Dashboard stats endpoint
@api_router.get("/admin/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_admin: dict = Depends(admin_required)):
    """Get dashboard statistics (admin)."""
    try:
        db = get_database()
        
        # Get counts
        total_packages = await db.packages.count_documents({"status": "active"})
        active_bookings = await db.bookings.count_documents({"status": "confirmed"})
        cab_bookings = await db.cab_bookings.count_documents({})
        customer_reviews = await db.testimonials.count_documents({"status": "approved"})
        
        # Get recent bookings
        recent_bookings_cursor = db.bookings.find({}).sort("createdAt", -1).limit(5)
        recent_bookings = await recent_bookings_cursor.to_list(length=5)
        
        # Calculate monthly revenue (mock calculation)
        monthly_revenue = 125000.0  # This would be calculated based on confirmed bookings
        
        return DashboardStats(
            totalPackages=total_packages,
            activeBookings=active_bookings,
            cabBookings=cab_bookings,
            customerReviews=customer_reviews,
            monthlyRevenue=monthly_revenue,
            recentBookings=[
                {
                    "id": str(booking["_id"]),
                    "customer": booking["customerName"],
                    "package": booking["packageTitle"],
                    "date": booking["createdAt"].isoformat(),
                    "status": booking["status"]
                }
                for booking in recent_bookings
            ]
        )
        
    except Exception as e:
        logger.error(f"Get dashboard stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard stats")

# Include router in app
app.include_router(api_router)