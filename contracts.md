# G.M.B Travels Kashmir - API Contracts

## Overview
This document outlines the API contracts between frontend and backend for the G.M.B Travels Kashmir website with comprehensive admin management system.

## Authentication

### Admin Authentication
- **Login**: `POST /api/auth/login`
- **Logout**: `POST /api/auth/logout`
- **Verify Token**: `GET /api/auth/verify`

## Data Models

### 1. Package Model
```json
{
  "_id": "ObjectId",
  "title": "string",
  "description": "string",
  "duration": "string",
  "price": "number",
  "groupSize": "string",
  "image": "string (URL)",
  "images": ["array of URLs"],
  "highlights": ["array of strings"],
  "itinerary": [
    {
      "day": "number",
      "title": "string", 
      "description": "string",
      "activities": ["array"]
    }
  ],
  "inclusions": ["array of strings"],
  "exclusions": ["array of strings"],
  "category": "string",
  "status": "active/inactive",
  "createdAt": "Date",
  "updatedAt": "Date"
}
```

### 2. Booking Model
```json
{
  "_id": "ObjectId",
  "customerName": "string",
  "email": "string",
  "phone": "string",
  "packageId": "ObjectId",
  "packageTitle": "string",
  "travelDate": "Date",
  "travelers": "number",
  "totalAmount": "number",
  "status": "pending/confirmed/cancelled",
  "specialRequests": "string",
  "bookingType": "package/cab",
  "createdAt": "Date"
}
```

### 3. Testimonial Model
```json
{
  "_id": "ObjectId",
  "customerName": "string",
  "location": "string",
  "rating": "number",
  "review": "string",
  "packageName": "string",
  "date": "string",
  "images": ["array of URLs"],
  "status": "approved/pending",
  "createdAt": "Date"
}
```

### 4. Cab Booking Model
```json
{
  "_id": "ObjectId",
  "customerName": "string",
  "email": "string",
  "phone": "string",
  "pickupLocation": "string",
  "dropLocation": "string",
  "pickupDate": "Date",
  "pickupTime": "string",
  "returnDate": "Date",
  "returnTime": "string",
  "tripType": "oneway/roundtrip/local",
  "vehicleType": "string",
  "passengers": "number",
  "specialRequests": "string",
  "status": "pending/confirmed/completed/cancelled",
  "estimatedCost": "number",
  "createdAt": "Date"
}
```

### 5. Contact Inquiry Model
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string", 
  "phone": "string",
  "subject": "string",
  "inquiryType": "string",
  "message": "string",
  "preferredContact": "string",
  "status": "new/replied/closed",
  "createdAt": "Date"
}
```

### 6. Gallery Image Model
```json
{
  "_id": "ObjectId",
  "title": "string",
  "description": "string",
  "imageUrl": "string",
  "category": "package/gallery/testimonial",
  "tags": ["array of strings"],
  "isActive": "boolean",
  "createdAt": "Date"
}
```

## API Endpoints

### Packages
- `GET /api/packages` - Get all packages (public)
- `GET /api/packages/:id` - Get package by ID (public)
- `POST /api/admin/packages` - Create package (admin)
- `PUT /api/admin/packages/:id` - Update package (admin)
- `DELETE /api/admin/packages/:id` - Delete package (admin)

### Bookings
- `POST /api/bookings` - Create booking (public)
- `GET /api/admin/bookings` - Get all bookings (admin)
- `PUT /api/admin/bookings/:id` - Update booking status (admin)
- `DELETE /api/admin/bookings/:id` - Delete booking (admin)

### Testimonials
- `GET /api/testimonials` - Get approved testimonials (public)
- `POST /api/testimonials` - Submit testimonial (public)
- `GET /api/admin/testimonials` - Get all testimonials (admin)
- `PUT /api/admin/testimonials/:id` - Update testimonial (admin)
- `DELETE /api/admin/testimonials/:id` - Delete testimonial (admin)

### Cab Bookings
- `POST /api/cab-bookings` - Create cab booking (public)
- `GET /api/admin/cab-bookings` - Get all cab bookings (admin)
- `PUT /api/admin/cab-bookings/:id` - Update cab booking (admin)

### Contact
- `POST /api/contact` - Submit contact form (public)
- `GET /api/admin/contacts` - Get all inquiries (admin)
- `PUT /api/admin/contacts/:id` - Update inquiry status (admin)

### File Upload
- `POST /api/admin/upload` - Upload images (admin)
- `DELETE /api/admin/images/:id` - Delete image (admin)
- `GET /api/admin/images` - Get all images (admin)

### Dashboard Stats
- `GET /api/admin/stats` - Get dashboard statistics (admin)

## Mock Data Integration

### Frontend Mock Removal
1. Remove mock data from components
2. Replace with API calls using axios
3. Add loading states and error handling
4. Implement proper form submissions

### Backend Implementation
1. Implement all API endpoints
2. Add proper validation
3. File upload functionality
4. Admin authentication middleware
5. Error handling and logging

## Integration Steps

1. **Backend Setup**: Implement all models and API endpoints
2. **Authentication**: JWT-based admin authentication
3. **File Upload**: Multer for image uploads with proper storage
4. **Frontend Integration**: Replace mock data with API calls
5. **Admin Panel**: Complete CRUD operations for all entities
6. **Testing**: Test all functionality end-to-end

## Security Considerations

1. Admin routes protected with JWT authentication
2. Input validation on all forms
3. File upload restrictions (size, type)
4. CORS configuration
5. Rate limiting on public endpoints