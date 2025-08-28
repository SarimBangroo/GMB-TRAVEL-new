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

# Site Settings Models
class ContactInfo(BaseModel):
    phone: List[str] = ["+91 98765 43210", "+91 98765 43211"]
    email: List[str] = ["info@gmbtravelskashmir.com", "bookings@gmbtravelskashmir.com"]
    address: List[str] = ["Main Office: Srinagar, Kashmir, India", "Branch: Dal Lake Area"]
    workingHours: List[str] = ["Mon - Sat: 9:00 AM - 8:00 PM", "Sun: 10:00 AM - 6:00 PM"]
    whatsapp: str = "+919876543210"

class SocialMedia(BaseModel):
    facebook: str = ""
    instagram: str = ""
    twitter: str = ""
    youtube: str = ""
    linkedin: str = ""

class CompanyInfo(BaseModel):
    name: str = "G.M.B Travels Kashmir"
    tagline: str = "Discover Paradise on Earth"
    description: str = "Your trusted partner for exploring the magnificent beauty of Kashmir. We create unforgettable experiences that last a lifetime."
    logo: str = "https://customer-assets.emergentagent.com/job_gmb-tours/artifacts/u7oxyvzc_logo.jpg"
    aboutText: str = "With years of experience in Kashmir tourism, G.M.B Travels Kashmir has been the trusted companion for travelers seeking authentic experiences in the paradise on earth."
    missionStatement: str = "We specialize in creating unforgettable journeys through Kashmir's breathtaking landscapes."

class HeroSection(BaseModel):
    title: str = "Experience the Beauty of"
    subtitle: str = "Kashmir"
    description: str = "Discover the pristine valleys, serene lakes, and majestic mountains of Kashmir with our expertly crafted tour packages"
    backgroundImage: str = "https://customer-assets.emergentagent.com/job_gmb-tours/artifacts/u2wmxitn_pexels-abhilash-mishra-1539700.jpg"
    ctaButtonText: str = "Explore Packages"
    secondaryCtaText: str = "Contact Us"

class MapSettings(BaseModel):
    embedUrl: str = ""
    latitude: float = 34.0837
    longitude: float = 74.7973
    zoomLevel: int = 12
    address: str = "Srinagar, Kashmir, India"

class SeoSettings(BaseModel):
    homeTitle: str = "G.M.B Travels Kashmir - Experience Paradise on Earth"
    homeDescription: str = "Discover Kashmir's beauty with our expertly crafted tour packages. Book your dream vacation today!"
    homeKeywords: List[str] = ["Kashmir tours", "Kashmir travel", "Dal Lake", "Gulmarg", "Srinagar tours"]
    siteUrl: str = "https://gmbtravelskashmir.com"
    ogImage: str = "https://customer-assets.emergentagent.com/job_gmb-tours/artifacts/u2wmxitn_pexels-abhilash-mishra-1539700.jpg"

class BusinessStats(BaseModel):
    yearsExperience: int = 10
    happyCustomers: int = 500
    tourPackages: int = 50
    supportAvailability: str = "24/7"

class SiteSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    contactInfo: ContactInfo = ContactInfo()
    socialMedia: SocialMedia = SocialMedia()
    companyInfo: CompanyInfo = CompanyInfo()
    heroSection: HeroSection = HeroSection()
    mapSettings: MapSettings = MapSettings()
    seoSettings: SeoSettings = SeoSettings()
    businessStats: BusinessStats = BusinessStats()
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class SiteSettingsUpdate(BaseModel):
    contactInfo: Optional[ContactInfo] = None
    socialMedia: Optional[SocialMedia] = None
    companyInfo: Optional[CompanyInfo] = None
    heroSection: Optional[HeroSection] = None
    mapSettings: Optional[MapSettings] = None
    seoSettings: Optional[SeoSettings] = None
    businessStats: Optional[BusinessStats] = None
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

# Team Management Models
class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    agent = "agent"

class TeamMember(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    fullName: str
    email: EmailStr
    phone: str
    username: str
    passwordHash: str
    role: UserRole
    department: str
    joiningDate: datetime
    isActive: bool = True
    lastLogin: Optional[datetime] = None
    packagesCreated: int = 0
    clientsManaged: int = 0
    avatar: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class TeamMemberCreate(BaseModel):
    fullName: str
    email: EmailStr
    phone: str
    username: str
    password: str
    role: UserRole
    department: str
    joiningDate: datetime
    isActive: bool = True

class TeamMemberUpdate(BaseModel):
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    role: Optional[UserRole] = None
    department: Optional[str] = None
    joiningDate: Optional[datetime] = None
    isActive: Optional[bool] = None
    packagesCreated: Optional[int] = None
    clientsManaged: Optional[int] = None
    avatar: Optional[str] = None
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class PasswordChangeRequest(BaseModel):
    oldPassword: str
    newPassword: str

class TeamLogin(BaseModel):
    username: str
    password: str

# Popup/Announcement Models
class PopupType(str, Enum):
    offer = "offer"
    announcement = "announcement"
    news = "news"
    alert = "alert"

class Popup(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str
    content: str
    popupType: PopupType
    backgroundColor: str = "#ffffff"
    textColor: str = "#000000"
    buttonText: str = "Close"
    buttonColor: str = "#f59e0b"
    imageUrl: Optional[str] = None
    linkUrl: Optional[str] = None
    isActive: bool = True
    showOnPages: List[str] = ["home"]  # pages where popup should show
    displayDuration: int = 5000  # milliseconds
    cookieExpiry: int = 24  # hours before showing again
    startDate: datetime = Field(default_factory=datetime.utcnow)
    endDate: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class PopupCreate(BaseModel):
    title: str
    content: str
    popupType: PopupType
    backgroundColor: str = "#ffffff"
    textColor: str = "#000000"
    buttonText: str = "Close"
    buttonColor: str = "#f59e0b"
    imageUrl: Optional[str] = None
    linkUrl: Optional[str] = None
    showOnPages: List[str] = ["home"]
    displayDuration: int = 5000
    cookieExpiry: int = 24
    startDate: datetime = Field(default_factory=datetime.utcnow)
    endDate: Optional[datetime] = None

class PopupUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    popupType: Optional[PopupType] = None
    backgroundColor: Optional[str] = None
    textColor: Optional[str] = None
    buttonText: Optional[str] = None
    buttonColor: Optional[str] = None
    imageUrl: Optional[str] = None
    linkUrl: Optional[str] = None
    isActive: Optional[bool] = None
    showOnPages: Optional[List[str]] = None
    displayDuration: Optional[int] = None
    cookieExpiry: Optional[int] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    updatedAt: datetime = Field(default_factory=datetime.utcnow)