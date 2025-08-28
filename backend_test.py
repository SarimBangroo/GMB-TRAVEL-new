#!/usr/bin/env python3
"""
Backend API Test Suite for G.M.B Travels Kashmir
Testing Team Management and Popup Management API endpoints
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "https://gmb-travel-admin.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Test team member credentials
TEAM_MANAGER_USERNAME = "rajesh_manager"
TEAM_MANAGER_PASSWORD = "manager123"
TEAM_AGENT_USERNAME = "priya_agent"
TEAM_AGENT_PASSWORD = "agent123"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        
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
    
    def test_token_verification(self):
        """Test token verification endpoint"""
        print("\n=== Testing Token Verification ===")
        
        if not self.admin_token:
            self.log_test("Token Verification", False, "No admin token available")
            return False
            
        try:
            response = self.session.get(f"{self.base_url}/auth/verify")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("valid") and data.get("admin"):
                    self.log_test("Token Verification", True, f"Token verified for admin: {data['admin']}")
                    return True
                else:
                    self.log_test("Token Verification", False, "Invalid token response format", data)
                    return False
            else:
                self.log_test("Token Verification", False, f"Verification failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Token Verification", False, f"Exception during verification: {str(e)}")
            return False
    
    def test_public_site_settings(self):
        """Test GET /api/site-settings (public endpoint)"""
        print("\n=== Testing Public Site Settings Endpoint ===")
        
        try:
            # Use a new session without auth headers for public endpoint
            public_session = requests.Session()
            response = public_session.get(f"{self.base_url}/site-settings")
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["contactInfo", "socialMedia", "companyInfo", "heroSection", "mapSettings", "seoSettings", "businessStats"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    # Check some key nested fields
                    contact_info = data.get("contactInfo", {})
                    company_info = data.get("companyInfo", {})
                    
                    if contact_info.get("phone") and company_info.get("name"):
                        self.log_test("Public Site Settings", True, "Successfully retrieved site settings with proper structure")
                        return True
                    else:
                        self.log_test("Public Site Settings", False, "Missing key nested fields in response", data)
                        return False
                else:
                    self.log_test("Public Site Settings", False, f"Missing required fields: {missing_fields}", data)
                    return False
            else:
                self.log_test("Public Site Settings", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Public Site Settings", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_get_site_settings(self):
        """Test GET /api/admin/site-settings (admin endpoint)"""
        print("\n=== Testing Admin Get Site Settings Endpoint ===")
        
        if not self.admin_token:
            self.log_test("Admin Get Site Settings", False, "No admin token available")
            return False
            
        try:
            response = self.session.get(f"{self.base_url}/admin/site-settings")
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure (same as public but with admin access)
                required_fields = ["contactInfo", "socialMedia", "companyInfo", "heroSection", "mapSettings", "seoSettings", "businessStats"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    self.log_test("Admin Get Site Settings", True, "Successfully retrieved site settings via admin endpoint")
                    return True
                else:
                    self.log_test("Admin Get Site Settings", False, f"Missing required fields: {missing_fields}", data)
                    return False
            else:
                self.log_test("Admin Get Site Settings", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Get Site Settings", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_update_site_settings(self):
        """Test PUT /api/admin/site-settings (admin endpoint)"""
        print("\n=== Testing Admin Update Site Settings Endpoint ===")
        
        if not self.admin_token:
            self.log_test("Admin Update Site Settings", False, "No admin token available")
            return False
            
        try:
            # First get current settings
            get_response = self.session.get(f"{self.base_url}/admin/site-settings")
            if get_response.status_code != 200:
                self.log_test("Admin Update Site Settings", False, "Could not retrieve current settings for update test")
                return False
            
            # Prepare update data with some changes
            update_data = {
                "companyInfo": {
                    "name": "G.M.B Travels Kashmir - Updated",
                    "tagline": "Discover Paradise on Earth - Test Update",
                    "description": "Updated description for testing purposes"
                },
                "contactInfo": {
                    "phone": ["+91 98765 43210", "+91 98765 43211", "+91 98765 43212"],
                    "email": ["info@gmbtravelskashmir.com", "bookings@gmbtravelskashmir.com"],
                    "address": ["Main Office: Srinagar, Kashmir, India - Updated", "Branch: Dal Lake Area"],
                    "workingHours": ["Mon - Sat: 9:00 AM - 8:00 PM", "Sun: 10:00 AM - 6:00 PM"],
                    "whatsapp": "+919876543210"
                }
            }
            
            response = self.session.put(f"{self.base_url}/admin/site-settings", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify the update was applied
                if (data.get("companyInfo", {}).get("name") == "G.M.B Travels Kashmir - Updated" and
                    data.get("companyInfo", {}).get("tagline") == "Discover Paradise on Earth - Test Update"):
                    self.log_test("Admin Update Site Settings", True, "Successfully updated site settings")
                    return True
                else:
                    self.log_test("Admin Update Site Settings", False, "Update did not apply correctly", data)
                    return False
            else:
                self.log_test("Admin Update Site Settings", False, f"Update failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Update Site Settings", False, f"Exception during update: {str(e)}")
            return False
    
    def test_admin_reset_site_settings(self):
        """Test POST /api/admin/site-settings/reset (admin endpoint)"""
        print("\n=== Testing Admin Reset Site Settings Endpoint ===")
        
        if not self.admin_token:
            self.log_test("Admin Reset Site Settings", False, "No admin token available")
            return False
            
        try:
            response = self.session.post(f"{self.base_url}/admin/site-settings/reset")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify reset response
                if "message" in data and "settings" in data:
                    settings = data["settings"]
                    
                    # Check if settings were reset to defaults
                    if (settings.get("companyInfo", {}).get("name") == "G.M.B Travels Kashmir" and
                        settings.get("companyInfo", {}).get("tagline") == "Discover Paradise on Earth"):
                        self.log_test("Admin Reset Site Settings", True, "Successfully reset site settings to defaults")
                        return True
                    else:
                        self.log_test("Admin Reset Site Settings", False, "Settings not properly reset to defaults", data)
                        return False
                else:
                    self.log_test("Admin Reset Site Settings", False, "Invalid reset response format", data)
                    return False
            else:
                self.log_test("Admin Reset Site Settings", False, f"Reset failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Reset Site Settings", False, f"Exception during reset: {str(e)}")
            return False
    
    def test_unauthorized_access(self):
        """Test that admin endpoints require authentication"""
        print("\n=== Testing Unauthorized Access Protection ===")
        
        try:
            # Create session without auth headers
            unauth_session = requests.Session()
            
            # Test admin endpoints without authentication
            admin_endpoints = [
                "/admin/site-settings",
                "/admin/site-settings/reset"
            ]
            
            all_protected = True
            for endpoint in admin_endpoints:
                if endpoint.endswith("/reset"):
                    response = unauth_session.post(f"{self.base_url}{endpoint}")
                else:
                    response = unauth_session.get(f"{self.base_url}{endpoint}")
                
                if response.status_code not in [401, 403]:
                    self.log_test("Unauthorized Access Protection", False, f"Endpoint {endpoint} not properly protected (status: {response.status_code})")
                    all_protected = False
                    break
            
            if all_protected:
                self.log_test("Unauthorized Access Protection", True, "All admin endpoints properly protected")
                return True
            else:
                return False
                
        except Exception as e:
            self.log_test("Unauthorized Access Protection", False, f"Exception during unauthorized access test: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all Site Settings API tests"""
        print("🚀 Starting Site Settings API Test Suite")
        print(f"Base URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence
        tests = [
            self.test_admin_authentication,
            self.test_token_verification,
            self.test_public_site_settings,
            self.test_admin_get_site_settings,
            self.test_admin_update_site_settings,
            self.test_admin_reset_site_settings,
            self.test_unauthorized_access
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return False

def main():
    """Main test execution"""
    tester = APITester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()