from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Enums for status fields
class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class TestimonialStatus(str, Enum):
    approved = "approved"
    pending = "pending"

class InquiryStatus(str, Enum):
    new = "new"
    replied = "replied"
    closed = "closed"

class PackageStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class TripType(str, Enum):
    oneway = "oneway"
    roundtrip = "roundtrip"
    local = "local"

# Package Models
class ItineraryDay(BaseModel):
    day: int
    title: str
    description: str
    activities: List[str]

class Package(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str
    description: str
    duration: str
    price: float
    groupSize: str
    image: str
    images: List[str] = []
    highlights: List[str] = []
    itinerary: List[ItineraryDay] = []
    inclusions: List[str] = []
    exclusions: List[str] = []
    category: str = "standard"
    status: PackageStatus = PackageStatus.active
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class PackageCreate(BaseModel):
    title: str
    description: str
    duration: str
    price: float
    groupSize: str
    image: str
    images: List[str] = []
    highlights: List[str] = []
    itinerary: List[ItineraryDay] = []
    inclusions: List[str] = []
    exclusions: List[str] = []
    category: str = "standard"

class PackageUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    price: Optional[float] = None
    groupSize: Optional[str] = None
    image: Optional[str] = None
    images: Optional[List[str]] = None
    highlights: Optional[List[str]] = None
    itinerary: Optional[List[ItineraryDay]] = None
    inclusions: Optional[List[str]] = None
    exclusions: Optional[List[str]] = None
    category: Optional[str] = None
    status: Optional[PackageStatus] = None
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

# Booking Models
class Booking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    customerName: str
    email: EmailStr
    phone: str
    packageId: Optional[str] = None
    packageTitle: str
    travelDate: datetime
    travelers: int
    totalAmount: float
    status: BookingStatus = BookingStatus.pending
    specialRequests: str = ""
    bookingType: str = "package"  # package or cab
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class BookingCreate(BaseModel):
    customerName: str
    email: EmailStr
    phone: str
    packageId: Optional[str] = None
    packageTitle: str
    travelDate: datetime
    travelers: int
    totalAmount: float
    specialRequests: str = ""
    bookingType: str = "package"

# Testimonial Models
class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    customerName: str
    location: str
    rating: int = Field(ge=1, le=5)
    review: str
    packageName: str
    date: str
    images: List[str] = []
    status: TestimonialStatus = TestimonialStatus.pending
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class TestimonialCreate(BaseModel):
    customerName: str
    location: str
    rating: int = Field(ge=1, le=5)
    review: str
    packageName: str
    date: str
    images: List[str] = []

# Cab Booking Models
class CabBooking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    customerName: str
    email: EmailStr
    phone: str
    pickupLocation: str
    dropLocation: str = ""
    pickupDate: datetime
    pickupTime: str
    returnDate: Optional[datetime] = None
    returnTime: Optional[str] = None
    tripType: TripType
    vehicleType: str
    passengers: int
    specialRequests: str = ""
    status: BookingStatus = BookingStatus.pending
    estimatedCost: float = 0.0
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class CabBookingCreate(BaseModel):
    customerName: str
    email: EmailStr
    phone: str
    pickupLocation: str
    dropLocation: str = ""
    pickupDate: datetime
    pickupTime: str
    returnDate: Optional[datetime] = None
    returnTime: Optional[str] = None
    tripType: TripType
    vehicleType: str
    passengers: int
    specialRequests: str = ""

# Contact Models
class ContactInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    email: EmailStr
    phone: str
    subject: str
    inquiryType: str = "general"
    message: str
    preferredContact: str = "email"
    status: InquiryStatus = InquiryStatus.new
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    subject: str
    inquiryType: str = "general"
    message: str
    preferredContact: str = "email"

# Gallery Models
class GalleryImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str
    description: str = ""
    imageUrl: str
    category: str = "gallery"  # package, gallery, testimonial
    tags: List[str] = []
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class ImageCreate(BaseModel):
    title: str
    description: str = ""
    imageUrl: str
    category: str = "gallery"
    tags: List[str] = []

# Admin Models
class Admin(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    username: str
    passwordHash: str
    email: EmailStr
    isActive: bool = True
    lastLogin: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class AdminLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Dashboard Stats
class DashboardStats(BaseModel):
    totalPackages: int
    activeBookings: int
    cabBookings: int
    customerReviews: int
    monthlyRevenue: float
    recentBookings: List[Dict[str, Any]]