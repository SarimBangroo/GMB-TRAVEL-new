import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import { Toaster } from './components/ui/sonner';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Packages from './pages/Packages';
import PackageDetail from './pages/PackageDetail';
import Testimonials from './pages/Testimonials';
import BookCab from './pages/BookCab';
import Contact from './pages/Contact';
import AdminLogin from './pages/admin/AdminLogin';
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminPackages from './pages/admin/AdminPackages';
import AdminTestimonials from './pages/admin/AdminTestimonials';
import AdminImages from './pages/admin/AdminImages';
import AdminBookings from './pages/admin/AdminBookings';
import AdminTeam from './pages/admin/AdminTeam';
import AdminSiteSettings from './pages/admin/AdminSiteSettings';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={
            <>
              <Header />
              <Home />
              <Footer />
            </>
          } />
          <Route path="/packages" element={
            <>
              <Header />
              <Packages />
              <Footer />
            </>
          } />
          <Route path="/packages/:id" element={
            <>
              <Header />
              <PackageDetail />
              <Footer />
            </>
          } />
          <Route path="/testimonials" element={
            <>
              <Header />
              <Testimonials />
              <Footer />
            </>
          } />
          <Route path="/book-cab" element={
            <>
              <Header />
              <BookCab />
              <Footer />
            </>
          } />
          <Route path="/contact" element={
            <>
              <Header />
              <Contact />
              <Footer />
            </>
          } />
          
          {/* Admin Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/packages" element={<AdminPackages />} />
          <Route path="/admin/testimonials" element={<AdminTestimonials />} />
          <Route path="/admin/images" element={<AdminImages />} />
          <Route path="/admin/bookings" element={<AdminBookings />} />
          <Route path="/admin/team" element={<AdminTeam />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;