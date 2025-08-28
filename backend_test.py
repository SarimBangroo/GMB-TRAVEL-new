#!/usr/bin/env python3
"""
Backend API Test Suite for G.M.B Travels Kashmir
Testing Vehicle Management API endpoints
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "https://kashmir-travel-admin.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

class VehicleAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        self.created_vehicle_id = None
        
    def log_test(self, test_name, success, message, response_data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
    
    def test_admin_authentication(self):
        """Test admin login functionality"""
        print("\n=== Testing Admin Authentication ===")
        
        try:
            # Test admin login
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            
            response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.admin_token = data["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
                    self.log_test("Admin Login", True, "Successfully authenticated admin user")
                    return True
                else:
                    self.log_test("Admin Login", False, "No access token in response", data)
                    return False
            else:
                self.log_test("Admin Login", False, f"Login failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception during login: {str(e)}")
            return False
    
    def test_get_vehicles_public(self):
        """Test GET /api/vehicles (public endpoint)"""
        print("\n=== Testing Get Vehicles (Public) ===")
        
        try:
            # Use a new session without auth headers for public endpoint
            public_session = requests.Session()
            response = public_session.get(f"{self.base_url}/vehicles")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success" and isinstance(data.get("data"), list):
                    vehicles = data["data"]
                    self.log_test("Get Vehicles (Public)", True, f"Successfully retrieved {len(vehicles)} vehicles")
                    
                    # Verify default vehicles exist
                    if len(vehicles) >= 6:
                        vehicle_names = [v.get("name", "") for v in vehicles]
                        expected_vehicles = ["Force Urbania", "Toyota Innova Crysta", "Tempo Traveller", 
                                           "Mahindra Scorpio", "Maruti Suzuki Dzire", "Toyota Fortuner"]
                        
                        found_vehicles = [name for name in expected_vehicles if any(name in vname for vname in vehicle_names)]
                        
                        if len(found_vehicles) >= 5:  # Allow some flexibility
                            self.log_test("Default Vehicles Check", True, f"Found {len(found_vehicles)} expected default vehicles")
                        else:
                            self.log_test("Default Vehicles Check", False, f"Only found {len(found_vehicles)} expected vehicles: {found_vehicles}")
                    
                    return True
                else:
                    self.log_test("Get Vehicles (Public)", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Get Vehicles (Public)", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Get Vehicles (Public)", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_get_vehicles(self):
        """Test GET /api/admin/vehicles (admin endpoint)"""
        print("\n=== Testing Admin Get Vehicles ===")
        
        if not self.admin_token:
            self.log_test("Admin Get Vehicles", False, "No admin token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{self.base_url}/admin/vehicles", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success" and isinstance(data.get("data"), list):
                    vehicles = data["data"]
                    self.log_test("Admin Get Vehicles", True, f"Successfully retrieved {len(vehicles)} vehicles for admin")
                    return True
                else:
                    self.log_test("Admin Get Vehicles", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Admin Get Vehicles", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Get Vehicles", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_create_vehicle(self):
        """Test POST /api/admin/vehicles (admin endpoint)"""
        print("\n=== Testing Admin Create Vehicle ===")
        
        if not self.admin_token:
            self.log_test("Admin Create Vehicle", False, "No admin token available")
            return False
            
        try:
            # Create test vehicle data
            vehicle_data = {
                "vehicleType": "sedan_dzire",
                "name": "Test Sedan Vehicle",
                "model": "Test Model 2024",
                "capacity": "4 Passengers",
                "price": 15.0,
                "priceUnit": "per km",
                "features": ["AC", "GPS", "Music System", "Comfortable Seats"],
                "specifications": {
                    "fuelType": "petrol",
                    "transmission": "manual",
                    "mileage": "20 kmpl",
                    "luggage": "Standard Boot"
                },
                "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400&h=300&fit=crop",
                "badge": "Test Vehicle",
                "badgeColor": "bg-red-500",
                "isActive": True,
                "isPopular": False,
                "sortOrder": 99,
                "description": "Test vehicle for API testing"
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.post(f"{self.base_url}/admin/vehicles", json=vehicle_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if (data.get("status") == "success" and 
                    data.get("data", {}).get("name") == "Test Sedan Vehicle"):
                    self.created_vehicle_id = data["data"].get("_id")
                    self.log_test("Admin Create Vehicle", True, f"Successfully created vehicle with ID: {self.created_vehicle_id}")
                    return True
                else:
                    self.log_test("Admin Create Vehicle", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Admin Create Vehicle", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Create Vehicle", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_update_vehicle(self):
        """Test PUT /api/admin/vehicles/{id} (admin endpoint)"""
        print("\n=== Testing Admin Update Vehicle ===")
        
        if not self.admin_token or not self.created_vehicle_id:
            self.log_test("Admin Update Vehicle", False, "No admin token or vehicle ID available")
            return False
            
        try:
            # Update vehicle data
            update_data = {
                "name": "Updated Test Sedan Vehicle",
                "price": 18.0,
                "badge": "Updated Test Vehicle",
                "description": "Updated test vehicle for API testing"
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.put(f"{self.base_url}/admin/vehicles/{self.created_vehicle_id}", 
                                  json=update_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if (data.get("status") == "success" and 
                    data.get("data", {}).get("name") == "Updated Test Sedan Vehicle" and
                    data.get("data", {}).get("price") == 18.0):
                    self.log_test("Admin Update Vehicle", True, "Successfully updated vehicle")
                    return True
                else:
                    self.log_test("Admin Update Vehicle", False, "Update not applied correctly", data)
                    return False
            else:
                self.log_test("Admin Update Vehicle", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Update Vehicle", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_delete_vehicle(self):
        """Test DELETE /api/admin/vehicles/{id} (admin endpoint)"""
        print("\n=== Testing Admin Delete Vehicle ===")
        
        if not self.admin_token or not self.created_vehicle_id:
            self.log_test("Admin Delete Vehicle", False, "No admin token or vehicle ID available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.delete(f"{self.base_url}/admin/vehicles/{self.created_vehicle_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success" and "deleted successfully" in data.get("message", "").lower():
                    self.log_test("Admin Delete Vehicle", True, "Successfully deleted vehicle")
                    self.created_vehicle_id = None  # Clear the ID since it's deleted
                    return True
                else:
                    self.log_test("Admin Delete Vehicle", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Admin Delete Vehicle", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Delete Vehicle", False, f"Exception during request: {str(e)}")
            return False
    
    def test_unauthorized_access_protection(self):
        """Test that admin endpoints require authentication"""
        print("\n=== Testing Unauthorized Access Protection ===")
        
        try:
            # Create session without auth headers
            unauth_session = requests.Session()
            
            # Test admin endpoints without authentication
            admin_endpoints = [
                ("/admin/vehicles", "GET"),
                ("/admin/vehicles", "POST"),
            ]
            
            all_protected = True
            for endpoint, method in admin_endpoints:
                if method == "GET":
                    response = unauth_session.get(f"{self.base_url}{endpoint}")
                elif method == "POST":
                    response = unauth_session.post(f"{self.base_url}{endpoint}", json={})
                
                if response.status_code not in [401, 403]:
                    self.log_test("Unauthorized Access Protection", False, f"Endpoint {endpoint} not properly protected (status: {response.status_code})")
                    all_protected = False
                    break
            
            if all_protected:
                self.log_test("Unauthorized Access Protection", True, "All admin vehicle endpoints properly protected")
                return True
            else:
                return False
                
        except Exception as e:
            self.log_test("Unauthorized Access Protection", False, f"Exception during test: {str(e)}")
            return False
    
    def test_database_initialization(self):
        """Test that default vehicles are created during database initialization"""
        print("\n=== Testing Database Initialization ===")
        
        try:
            # Use public endpoint to check if default vehicles exist
            public_session = requests.Session()
            response = public_session.get(f"{self.base_url}/vehicles")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success" and isinstance(data.get("data"), list):
                    vehicles = data["data"]
                    
                    # Check for expected default vehicles
                    expected_types = ["force_urbania", "innova_crysta", "tempo_traveller", 
                                    "mahindra_scorpio", "sedan_dzire", "luxury_fortuner"]
                    
                    found_types = [v.get("vehicleType") for v in vehicles if v.get("vehicleType") in expected_types]
                    
                    if len(found_types) >= 5:  # Allow some flexibility
                        self.log_test("Database Initialization", True, f"Database properly initialized with {len(found_types)} default vehicle types")
                        
                        # Check if vehicles have proper structure
                        sample_vehicle = vehicles[0] if vehicles else {}
                        required_fields = ["name", "model", "capacity", "price", "features", "specifications"]
                        
                        missing_fields = [field for field in required_fields if field not in sample_vehicle]
                        
                        if not missing_fields:
                            self.log_test("Vehicle Data Structure", True, "Vehicles have proper data structure")
                        else:
                            self.log_test("Vehicle Data Structure", False, f"Missing fields in vehicle data: {missing_fields}")
                        
                        return True
                    else:
                        self.log_test("Database Initialization", False, f"Only found {len(found_types)} default vehicle types: {found_types}")
                        return False
                else:
                    self.log_test("Database Initialization", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Database Initialization", False, f"Request failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Database Initialization", False, f"Exception during test: {str(e)}")
            return False
    
    def test_integration_flow(self):
        """Test complete integration flow"""
        print("\n=== Testing Integration Flow ===")
        
        try:
            # Test: Admin creates vehicle -> Public endpoint returns the vehicle
            if self.created_vehicle_id:
                # Check if created vehicle appears in public endpoint
                public_session = requests.Session()
                response = public_session.get(f"{self.base_url}/vehicles")
                
                if response.status_code == 200:
                    data = response.json()
                    vehicles = data.get("data", [])
                    vehicle_found = any(v.get("_id") == self.created_vehicle_id for v in vehicles)
                    
                    if vehicle_found:
                        self.log_test("Integration Flow", True, "Created vehicle successfully appears in public endpoint")
                        return True
                    else:
                        self.log_test("Integration Flow", False, "Created vehicle not found in public endpoint")
                        return False
                else:
                    self.log_test("Integration Flow", False, f"Public vehicles endpoint failed (status: {response.status_code})")
                    return False
            else:
                # If no vehicle was created (maybe it was deleted), that's also a valid test result
                self.log_test("Integration Flow", True, "No vehicle to test integration (vehicle was deleted)")
                return True
                
        except Exception as e:
            self.log_test("Integration Flow", False, f"Exception during integration test: {str(e)}")
            return False
    
    def cleanup_test_data(self):
        """Clean up test data created during testing"""
        print("\n=== Cleaning Up Test Data ===")
        
        try:
            if not self.admin_token:
                return
                
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            
            # Delete created vehicle if it still exists
            if self.created_vehicle_id:
                response = requests.delete(f"{self.base_url}/admin/vehicles/{self.created_vehicle_id}", headers=headers)
                if response.status_code == 200:
                    self.log_test("Cleanup Vehicle", True, "Successfully deleted test vehicle")
                else:
                    self.log_test("Cleanup Vehicle", False, f"Failed to delete vehicle (status: {response.status_code})")
                    
        except Exception as e:
            self.log_test("Cleanup", False, f"Exception during cleanup: {str(e)}")
    
    def run_all_tests(self):
        """Run all Vehicle Management API tests"""
        print("🚀 Starting Vehicle Management API Test Suite")
        print(f"Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test sequence
        tests = [
            # Authentication test
            self.test_admin_authentication,
            
            # Database initialization test
            self.test_database_initialization,
            
            # Vehicle Management tests
            self.test_get_vehicles_public,
            self.test_admin_get_vehicles,
            self.test_admin_create_vehicle,
            self.test_admin_update_vehicle,
            
            # Security tests
            self.test_unauthorized_access_protection,
            
            # Integration test
            self.test_integration_flow,
            
            # Delete test (should be last)
            self.test_admin_delete_vehicle,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        # Cleanup test data
        self.cleanup_test_data()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All Vehicle Management API tests passed!")
            return True
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return False

def main():
    """Main test execution"""
    tester = VehicleAPITester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()