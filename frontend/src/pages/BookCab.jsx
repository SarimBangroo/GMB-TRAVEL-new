import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Badge } from '../components/ui/badge';
import { Calendar } from '../components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '../components/ui/popover';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  Car,
  Users,
  MapPin,
  Calendar as CalendarIcon,
  Clock,
  Phone,
  Mail,
  CheckCircle,
  Star,
  Shield,
  Fuel
} from 'lucide-react';
import { format } from 'date-fns';
import { toast } from 'sonner';

const BookCab = () => {
  const [bookingForm, setBookingForm] = useState({
    pickupLocation: '',
    dropLocation: '',
    pickupDate: null,
    pickupTime: '',
    returnDate: null,
    returnTime: '',
    tripType: 'oneway',
    vehicleType: '',
    passengers: '',
    name: '',
    phone: '',
    email: '',
    specialRequests: ''
  });

  const vehicleTypes = [
    {
      id: 'sedan',
      name: 'Sedan Car',
      capacity: '4 Passengers',
      price: 12,
      features: ['AC', 'Comfortable Seating', 'GPS Navigation'],
      image: 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=300&h=200&fit=crop'
    },
    {
      id: 'suv',
      name: 'SUV',
      capacity: '6-7 Passengers',
      price: 18,
      features: ['AC', 'Spacious', 'Luggage Space', 'Mountain Roads'],
      image: 'https://images.unsplash.com/photo-1566473965997-3de9c817e938?w=300&h=200&fit=crop'
    },
    {
      id: 'innova',
      name: 'Toyota Innova',
      capacity: '7 Passengers',
      price: 20,
      features: ['AC', 'Premium Comfort', 'Extra Luggage', 'Experienced Driver'],
      image: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=300&h=200&fit=crop'
    },
    {
      id: 'tempo',
      name: 'Tempo Traveller',
      capacity: '12-15 Passengers',
      price: 35,
      features: ['AC', 'Group Travel', 'Push Back Seats', 'Entertainment System'],
      image: 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=300&h=200&fit=crop'
    }
  ];

  const popularRoutes = [
    { from: 'Srinagar Airport', to: 'Dal Lake', distance: '15 km', duration: '30 min' },
    { from: 'Srinagar', to: 'Gulmarg', distance: '52 km', duration: '1.5 hrs' },
    { from: 'Srinagar', to: 'Pahalgam', distance: '95 km', duration: '2.5 hrs' },
    { from: 'Srinagar', to: 'Sonamarg', distance: '80 km', duration: '2 hrs' },
    { from: 'Jammu Airport', to: 'Srinagar', distance: '270 km', duration: '6 hrs' },
    { from: 'Srinagar', to: 'Leh', distance: '434 km', duration: '8-10 hrs' }
  ];

  const handleInputChange = (field, value) => {
    setBookingForm(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Cab booking submitted:', bookingForm);
    toast.success('Cab booking request submitted successfully! We will contact you shortly.');
    
    // Reset form
    setBookingForm({
      pickupLocation: '',
      dropLocation: '',
      pickupDate: null,
      pickupTime: '',
      returnDate: null,
      returnTime: '',
      tripType: 'oneway',
      vehicleType: '',
      passengers: '',
      name: '',
      phone: '',
      email: '',
      specialRequests: ''
    });
  };

  const selectedVehicle = vehicleTypes.find(v => v.id === bookingForm.vehicleType);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-slate-800 to-slate-700">
        <div className="container mx-auto px-4">
          <div className="text-center text-white">
            <h1 className="text-5xl font-bold mb-4">Book Your Cab</h1>
            <p className="text-xl text-slate-200 max-w-2xl mx-auto">
              Reliable and comfortable transportation services across Kashmir. Travel with confidence and safety.
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Booking Form */}
          <div className="lg:col-span-2">
            <Card className="shadow-xl border-0">
              <CardHeader>
                <CardTitle className="text-2xl text-slate-800">Book Your Ride</CardTitle>
                <CardDescription>Fill in the details below to book your cab service</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Trip Type */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Trip Type</label>
                    <div className="flex space-x-4">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="tripType"
                          value="oneway"
                          checked={bookingForm.tripType === 'oneway'}
                          onChange={(e) => handleInputChange('tripType', e.target.value)}
                          className="mr-2"
                        />
                        One Way
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="tripType"
                          value="roundtrip"
                          checked={bookingForm.tripType === 'roundtrip'}
                          onChange={(e) => handleInputChange('tripType', e.target.value)}
                          className="mr-2"
                        />
                        Round Trip
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="tripType"
                          value="local"
                          checked={bookingForm.tripType === 'local'}
                          onChange={(e) => handleInputChange('tripType', e.target.value)}
                          className="mr-2"
                        />
                        Local Sightseeing
                      </label>
                    </div>
                  </div>

                  {/* Locations */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Pickup Location</label>
                      <Input
                        type="text"
                        placeholder="Enter pickup location"
                        value={bookingForm.pickupLocation}
                        onChange={(e) => handleInputChange('pickupLocation', e.target.value)}
                        required
                      />
                    </div>
                    {bookingForm.tripType !== 'local' && (
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Drop Location</label>
                        <Input
                          type="text"
                          placeholder="Enter drop location"
                          value={bookingForm.dropLocation}
                          onChange={(e) => handleInputChange('dropLocation', e.target.value)}
                          required
                        />
                      </div>
                    )}
                  </div>

                  {/* Date and Time */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Pickup Date</label>
                      <Popover>
                        <PopoverTrigger asChild>
                          <Button
                            variant="outline"
                            className="w-full justify-start text-left font-normal"
                          >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {bookingForm.pickupDate ? format(bookingForm.pickupDate, "PPP") : "Select date"}
                          </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                          <Calendar
                            mode="single"
                            selected={bookingForm.pickupDate}
                            onSelect={(date) => handleInputChange('pickupDate', date)}
                            disabled={(date) => date < new Date()}
                            initialFocus
                          />
                        </PopoverContent>
                      </Popover>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Pickup Time</label>
                      <Input
                        type="time"
                        value={bookingForm.pickupTime}
                        onChange={(e) => handleInputChange('pickupTime', e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  {/* Return Date for Round Trip */}
                  {bookingForm.tripType === 'roundtrip' && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Return Date</label>
                        <Popover>
                          <PopoverTrigger asChild>
                            <Button
                              variant="outline"
                              className="w-full justify-start text-left font-normal"
                            >
                              <CalendarIcon className="mr-2 h-4 w-4" />
                              {bookingForm.returnDate ? format(bookingForm.returnDate, "PPP") : "Select return date"}
                            </Button>
                          </PopoverTrigger>
                          <PopoverContent className="w-auto p-0" align="start">
                            <Calendar
                              mode="single"
                              selected={bookingForm.returnDate}
                              onSelect={(date) => handleInputChange('returnDate', date)}
                              disabled={(date) => date < bookingForm.pickupDate}
                              initialFocus
                            />
                          </PopoverContent>
                        </Popover>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Return Time</label>
                        <Input
                          type="time"
                          value={bookingForm.returnTime}
                          onChange={(e) => handleInputChange('returnTime', e.target.value)}
                        />
                      </div>
                    </div>
                  )}

                  {/* Vehicle and Passengers */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Vehicle Type</label>
                      <Select value={bookingForm.vehicleType} onValueChange={(value) => handleInputChange('vehicleType', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select vehicle type" />
                        </SelectTrigger>
                        <SelectContent>
                          {vehicleTypes.map((vehicle) => (
                            <SelectItem key={vehicle.id} value={vehicle.id}>
                              {vehicle.name} - {vehicle.capacity}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Number of Passengers</label>
                      <Select value={bookingForm.passengers} onValueChange={(value) => handleInputChange('passengers', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select passengers" />
                        </SelectTrigger>
                        <SelectContent>
                          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map((num) => (
                            <SelectItem key={num} value={num.toString()}>
                              {num} Passenger{num > 1 ? 's' : ''}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {/* Customer Details */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
                      <Input
                        type="text"
                        placeholder="Your full name"
                        value={bookingForm.name}
                        onChange={(e) => handleInputChange('name', e.target.value)}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Phone Number</label>
                      <Input
                        type="tel"
                        placeholder="Your phone number"
                        value={bookingForm.phone}
                        onChange={(e) => handleInputChange('phone', e.target.value)}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Email Address</label>
                      <Input
                        type="email"
                        placeholder="Your email address"
                        value={bookingForm.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        required
                      />
                    </div>
                  </div>

                  {/* Special Requests */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Special Requests (Optional)</label>
                    <Textarea
                      placeholder="Any special requirements or instructions..."
                      value={bookingForm.specialRequests}
                      onChange={(e) => handleInputChange('specialRequests', e.target.value)}
                      rows={3}
                    />
                  </div>

                  <Button 
                    type="submit" 
                    className="w-full bg-amber-600 hover:bg-amber-700 text-white py-3 text-lg font-semibold"
                  >
                    Book Cab Now
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Selected Vehicle Details */}
            {selectedVehicle && (
              <Card className="shadow-lg border-0">
                <CardHeader>
                  <CardTitle className="text-xl text-slate-800">Selected Vehicle</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <img 
                      src={selectedVehicle.image} 
                      alt={selectedVehicle.name}
                      className="w-full h-32 object-cover rounded-lg"
                    />
                    <div>
                      <h4 className="font-semibold text-slate-800">{selectedVehicle.name}</h4>
                      <p className="text-slate-600 text-sm">{selectedVehicle.capacity}</p>
                      <p className="text-amber-600 font-bold text-lg">₹{selectedVehicle.price}/km</p>
                    </div>
                    <div className="space-y-2">
                      <h5 className="font-medium text-slate-800">Features:</h5>
                      {selectedVehicle.features.map((feature, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span className="text-sm text-slate-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Vehicle Types Grid */}
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle className="text-xl text-slate-800">Available Vehicles</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-4">
                  {vehicleTypes.map((vehicle) => (
                    <div 
                      key={vehicle.id}
                      className={`p-4 border rounded-lg cursor-pointer transition-all ${
                        bookingForm.vehicleType === vehicle.id 
                          ? 'border-amber-600 bg-amber-50' 
                          : 'border-slate-200 hover:border-amber-300'
                      }`}
                      onClick={() => handleInputChange('vehicleType', vehicle.id)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-slate-800">{vehicle.name}</h4>
                        <Badge className="bg-amber-600 text-white">₹{vehicle.price}/km</Badge>
                      </div>
                      <p className="text-sm text-slate-600 flex items-center">
                        <Users className="h-4 w-4 mr-1" />
                        {vehicle.capacity}
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Popular Routes */}
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle className="text-xl text-slate-800">Popular Routes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {popularRoutes.map((route, index) => (
                    <div key={index} className="p-3 bg-slate-50 rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-slate-800">{route.from}</span>
                        <span className="text-slate-600">→</span>
                        <span className="font-medium text-slate-800">{route.to}</span>
                      </div>
                      <div className="flex items-center justify-between text-sm text-slate-600">
                        <span className="flex items-center">
                          <MapPin className="h-3 w-3 mr-1" />
                          {route.distance}
                        </span>
                        <span className="flex items-center">
                          <Clock className="h-3 w-3 mr-1" />
                          {route.duration}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Contact Info */}
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle className="text-xl text-slate-800">Need Help?</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-amber-100 rounded-full">
                      <Phone className="h-4 w-4 text-amber-600" />
                    </div>
                    <div>
                      <p className="font-medium text-slate-800">Call Us</p>
                      <p className="text-sm text-slate-600">+91 98765 43210</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-amber-100 rounded-full">
                      <Mail className="h-4 w-4 text-amber-600" />
                    </div>
                    <div>
                      <p className="font-medium text-slate-800">Email Us</p>
                      <p className="text-sm text-slate-600">info@gmbtravelskashmir.com</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-slate-800 mb-4">Why Choose Our Cab Service?</h3>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              Professional drivers, well-maintained vehicles, and reliable service across Kashmir
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="mx-auto mb-4 p-4 bg-green-100 rounded-full w-16 h-16 flex items-center justify-center">
                <Shield className="h-8 w-8 text-green-600" />
              </div>
              <h4 className="text-lg font-semibold text-slate-800 mb-2">Safe & Secure</h4>
              <p className="text-slate-600">Experienced drivers with clean driving records and GPS tracking</p>
            </div>
            
            <div className="text-center">
              <div className="mx-auto mb-4 p-4 bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center">
                <Car className="h-8 w-8 text-blue-600" />
              </div>
              <h4 className="text-lg font-semibold text-slate-800 mb-2">Well-Maintained Fleet</h4>
              <p className="text-slate-600">Regular maintenance and cleaning for comfortable journeys</p>
            </div>
            
            <div className="text-center">
              <div className="mx-auto mb-4 p-4 bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center">
                <Clock className="h-8 w-8 text-purple-600" />
              </div>
              <h4 className="text-lg font-semibold text-slate-800 mb-2">On-Time Service</h4>
              <p className="text-slate-600">Punctual pickup and drop services with real-time tracking</p>
            </div>
            
            <div className="text-center">
              <div className="mx-auto mb-4 p-4 bg-amber-100 rounded-full w-16 h-16 flex items-center justify-center">
                <Star className="h-8 w-8 text-amber-600" />
              </div>
              <h4 className="text-lg font-semibold text-slate-800 mb-2">Excellent Service</h4>
              <p className="text-slate-600">Highly rated by customers with 24/7 customer support</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default BookCab;