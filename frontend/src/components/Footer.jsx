import React from 'react';
import { Link } from 'react-router-dom';
import { Phone, Mail, MapPin } from 'lucide-react';
import { Separator } from './ui/separator';

const Footer = () => {
  return (
    <footer className="bg-slate-800 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <img 
                src="https://customer-assets.emergentagent.com/job_gmb-tours/artifacts/u7oxyvzc_logo.jpg" 
                alt="G.M.B Travels Kashmir" 
                className="h-10 w-10 rounded-full object-cover"
              />
              <div>
                <h5 className="text-lg font-bold">G.M.B Travels Kashmir</h5>
                <p className="text-slate-300 text-sm">Paradise Awaits</p>
              </div>
            </div>
            <p className="text-slate-300 leading-relaxed">
              Your trusted partner for exploring the magnificent beauty of Kashmir. We create unforgettable experiences that last a lifetime.
            </p>
          </div>
          
          <div>
            <h5 className="text-lg font-semibold mb-4">Quick Links</h5>
            <ul className="space-y-2 text-slate-300">
              <li><Link to="/" className="hover:text-amber-400 transition-colors">Home</Link></li>
              <li><Link to="/packages" className="hover:text-amber-400 transition-colors">Packages</Link></li>
              <li><Link to="/book-cab" className="hover:text-amber-400 transition-colors">Book Cab</Link></li>
              <li><Link to="/testimonials" className="hover:text-amber-400 transition-colors">Testimonials</Link></li>
              <li><Link to="/contact" className="hover:text-amber-400 transition-colors">Contact</Link></li>
              <li className="pt-2 border-t border-slate-600">
                <Link to="/admin/login" className="text-slate-400 hover:text-amber-400 transition-colors text-sm flex items-center">
                  <span className="mr-1">🔐</span> Admin Login
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h5 className="text-lg font-semibold mb-4">Services</h5>
            <ul className="space-y-2 text-slate-300">
              <li>Kashmir Tour Packages</li>
              <li>Hotel & Houseboat Bookings</li>
              <li>Transportation Services</li>
              <li>Adventure Tours</li>
              <li>Cultural Experiences</li>
            </ul>
          </div>
          
          <div>
            <h5 className="text-lg font-semibold mb-4">Contact Info</h5>
            <div className="space-y-3 text-slate-300">
              <div className="flex items-center space-x-3">
                <Phone className="h-4 w-4" />
                <span>+91 98765 43210</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="h-4 w-4" />
                <span>info@gmbtravelskashmir.com</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="h-4 w-4" />
                <span>Srinagar, Kashmir, India</span>
              </div>
            </div>
          </div>
        </div>
        
        <Separator className="bg-slate-600 mb-8" />
        
        <div className="text-center text-slate-300">
          <p>&copy; 2024 G.M.B Travels Kashmir. All rights reserved. | Experience Paradise on Earth</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;