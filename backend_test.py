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
BASE_URL = "https://kashmir-travel-admin.preview.emergentagent.com/api"
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
        self.team_manager_token = None
        self.team_agent_token = None
        self.test_results = []
        self.created_team_member_id = None
        self.created_popup_id = None
        
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
    
    def test_team_member_login_manager(self):
        """Test team member login with manager credentials"""
        print("\n=== Testing Team Manager Login ===")
        
        try:
            login_data = {
                "username": TEAM_MANAGER_USERNAME,
                "password": TEAM_MANAGER_PASSWORD
            }
            
            response = self.session.post(f"{self.base_url}/team/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.team_manager_token = data["access_token"]
                    self.log_test("Team Manager Login", True, f"Successfully authenticated manager: {TEAM_MANAGER_USERNAME}")
                    return True
                else:
                    self.log_test("Team Manager Login", False, "No access token in response", data)
                    return False
            else:
                self.log_test("Team Manager Login", False, f"Login failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Team Manager Login", False, f"Exception during login: {str(e)}")
            return False
    
    def test_team_member_login_agent(self):
        """Test team member login with agent credentials"""
        print("\n=== Testing Team Agent Login ===")
        
        try:
            login_data = {
                "username": TEAM_AGENT_USERNAME,
                "password": TEAM_AGENT_PASSWORD
            }
            
            response = self.session.post(f"{self.base_url}/team/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.team_agent_token = data["access_token"]
                    self.log_test("Team Agent Login", True, f"Successfully authenticated agent: {TEAM_AGENT_USERNAME}")
                    return True
                else:
                    self.log_test("Team Agent Login", False, "No access token in response", data)
                    return False
            else:
                self.log_test("Team Agent Login", False, f"Login failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Team Agent Login", False, f"Exception during login: {str(e)}")
            return False
    
    def test_admin_get_team_members(self):
        """Test GET /api/admin/team (admin endpoint)"""
        print("\n=== Testing Admin Get Team Members ===")
        
        if not self.admin_token:
            self.log_test("Admin Get Team Members", False, "No admin token available")
            return False
            
        try:
            # Set admin auth header
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{self.base_url}/admin/team", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Admin Get Team Members", True, f"Successfully retrieved {len(data)} team members")
                    return True
                else:
                    self.log_test("Admin Get Team Members", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Admin Get Team Members", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Get Team Members", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_create_team_member(self):
        """Test POST /api/admin/team (admin endpoint)"""
        print("\n=== Testing Admin Create Team Member ===")
        
        if not self.admin_token:
            self.log_test("Admin Create Team Member", False, "No admin token available")
            return False
            
        try:
            # Create test team member data with unique username
            import uuid
            unique_suffix = str(uuid.uuid4())[:8]
            team_data = {
                "fullName": "Test Employee",
                "email": f"test.employee.{unique_suffix}@gmbtravelskashmir.com",
                "phone": "+91 98765 43299",
                "username": f"test_employee_{unique_suffix}",
                "password": "testpass123",
                "role": "agent",
                "department": "Sales",
                "joiningDate": datetime.utcnow().isoformat(),
                "isActive": True
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.post(f"{self.base_url}/admin/team", json=team_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if ("id" in data or "_id" in data) and data.get("fullName") == "Test Employee":
                    self.created_team_member_id = data.get("id") or data.get("_id")
                    self.log_test("Admin Create Team Member", True, f"Successfully created team member with ID: {self.created_team_member_id}")
                    return True
                else:
                    self.log_test("Admin Create Team Member", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Admin Create Team Member", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Create Team Member", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_update_team_member(self):
        """Test PUT /api/admin/team/{id} (admin endpoint)"""
        print("\n=== Testing Admin Update Team Member ===")
        
        if not self.admin_token or not self.created_team_member_id:
            self.log_test("Admin Update Team Member", False, "No admin token or team member ID available")
            return False
            
        try:
            # Update team member data
            update_data = {
                "fullName": "Test Employee Updated",
                "department": "Marketing",
                "isActive": True
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.put(f"{self.base_url}/admin/team/{self.created_team_member_id}", json=update_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("fullName") == "Test Employee Updated" and data.get("department") == "Marketing":
                    self.log_test("Admin Update Team Member", True, "Successfully updated team member")
                    return True
                else:
                    self.log_test("Admin Update Team Member", False, "Update not applied correctly", data)
                    return False
            else:
                self.log_test("Admin Update Team Member", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Update Team Member", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_change_team_password(self):
        """Test POST /api/admin/team/{id}/change-password (admin endpoint)"""
        print("\n=== Testing Admin Change Team Password ===")
        
        if not self.admin_token or not self.created_team_member_id:
            self.log_test("Admin Change Team Password", False, "No admin token or team member ID available")
            return False
            
        try:
            # Change password data
            password_data = {"new_password": "newpassword123"}
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.post(f"{self.base_url}/admin/team/{self.created_team_member_id}/change-password", 
                                   data=password_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if "message" in data and "successfully" in data["message"].lower():
                    self.log_test("Admin Change Team Password", True, "Successfully changed team member password")
                    return True
                else:
                    self.log_test("Admin Change Team Password", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Admin Change Team Password", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Change Team Password", False, f"Exception during request: {str(e)}")
            return False
    
    def test_get_active_popups_public(self):
        """Test GET /api/popups (public endpoint)"""
        print("\n=== Testing Get Active Popups (Public) ===")
        
        try:
            # Use a new session without auth headers for public endpoint
            public_session = requests.Session()
            response = public_session.get(f"{self.base_url}/popups")
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Get Active Popups (Public)", True, f"Successfully retrieved {len(data)} active popups")
                    return True
                else:
                    self.log_test("Get Active Popups (Public)", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Get Active Popups (Public)", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Get Active Popups (Public)", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_get_all_popups(self):
        """Test GET /api/admin/popups (admin endpoint)"""
        print("\n=== Testing Admin Get All Popups ===")
        
        if not self.admin_token:
            self.log_test("Admin Get All Popups", False, "No admin token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{self.base_url}/admin/popups", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Admin Get All Popups", True, f"Successfully retrieved {len(data)} popups")
                    return True
                else:
                    self.log_test("Admin Get All Popups", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Admin Get All Popups", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Get All Popups", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_create_popup(self):
        """Test POST /api/admin/popups (admin endpoint)"""
        print("\n=== Testing Admin Create Popup ===")
        
        if not self.admin_token:
            self.log_test("Admin Create Popup", False, "No admin token available")
            return False
            
        try:
            # Create test popup data
            popup_data = {
                "title": "Special Kashmir Tour Offer",
                "content": "Book now and get 20% off on all Kashmir tour packages! Limited time offer.",
                "popupType": "offer",
                "backgroundColor": "#f0f9ff",
                "textColor": "#1e40af",
                "buttonText": "Book Now",
                "buttonColor": "#f59e0b",
                "showOnPages": ["home", "packages"],
                "displayDuration": 8000,
                "cookieExpiry": 48,
                "startDate": datetime.utcnow().isoformat(),
                "endDate": (datetime.utcnow() + timedelta(days=30)).isoformat()
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.post(f"{self.base_url}/admin/popups", json=popup_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if ("id" in data or "_id" in data) and data.get("title") == "Special Kashmir Tour Offer":
                    self.created_popup_id = data.get("id") or data.get("_id")
                    self.log_test("Admin Create Popup", True, f"Successfully created popup with ID: {self.created_popup_id}")
                    return True
                else:
                    self.log_test("Admin Create Popup", False, "Invalid response format", data)
                    return False
            else:
                self.log_test("Admin Create Popup", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Create Popup", False, f"Exception during request: {str(e)}")
            return False
    
    def test_admin_update_popup(self):
        """Test PUT /api/admin/popups/{id} (admin endpoint)"""
        print("\n=== Testing Admin Update Popup ===")
        
        if not self.admin_token or not self.created_popup_id:
            self.log_test("Admin Update Popup", False, "No admin token or popup ID available")
            return False
            
        try:
            # Update popup data
            update_data = {
                "title": "Updated Kashmir Tour Offer",
                "content": "Book now and get 25% off on all Kashmir tour packages! Extended offer.",
                "backgroundColor": "#fef3c7",
                "isActive": True
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.put(f"{self.base_url}/admin/popups/{self.created_popup_id}", json=update_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("title") == "Updated Kashmir Tour Offer" and "25% off" in data.get("content", ""):
                    self.log_test("Admin Update Popup", True, "Successfully updated popup")
                    return True
                else:
                    self.log_test("Admin Update Popup", False, "Update not applied correctly", data)
                    return False
            else:
                self.log_test("Admin Update Popup", False, f"Request failed with status {response.status_code}", response.json() if response.content else None)
                return False
                
        except Exception as e:
            self.log_test("Admin Update Popup", False, f"Exception during request: {str(e)}")
            return False
    
    def test_role_based_authentication(self):
        """Test role-based authentication and access control"""
        print("\n=== Testing Role-Based Authentication ===")
        
        try:
            # Test that team members cannot access admin endpoints
            if self.team_manager_token:
                headers = {"Authorization": f"Bearer {self.team_manager_token}"}
                response = requests.get(f"{self.base_url}/admin/team", headers=headers)
                
                if response.status_code in [401, 403]:
                    self.log_test("Role-Based Authentication", True, "Team member properly blocked from admin endpoints")
                    return True
                else:
                    self.log_test("Role-Based Authentication", False, f"Team member accessed admin endpoint (status: {response.status_code})")
                    return False
            else:
                self.log_test("Role-Based Authentication", False, "No team member token available for testing")
                return False
                
        except Exception as e:
            self.log_test("Role-Based Authentication", False, f"Exception during test: {str(e)}")
            return False
    
    def test_unauthorized_access_protection(self):
        """Test that admin endpoints require authentication"""
        print("\n=== Testing Unauthorized Access Protection ===")
        
        try:
            # Create session without auth headers
            unauth_session = requests.Session()
            
            # Test admin endpoints without authentication
            admin_endpoints = [
                ("/admin/team", "GET"),
                ("/admin/team", "POST"),
                ("/admin/popups", "GET"),
                ("/admin/popups", "POST")
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
                self.log_test("Unauthorized Access Protection", True, "All admin endpoints properly protected")
                return True
            else:
                return False
                
        except Exception as e:
            self.log_test("Unauthorized Access Protection", False, f"Exception during test: {str(e)}")
            return False
    
    def test_integration_flow(self):
        """Test complete integration flow"""
        print("\n=== Testing Integration Flow ===")
        
        try:
            # Test: Admin creates popup -> Public endpoint returns active popups
            if self.created_popup_id:
                # Check if created popup appears in public endpoint
                public_session = requests.Session()
                response = public_session.get(f"{self.base_url}/popups")
                
                if response.status_code == 200:
                    popups = response.json()
                    popup_found = any(popup.get("id") == self.created_popup_id or popup.get("_id") == self.created_popup_id for popup in popups)
                    
                    if popup_found:
                        self.log_test("Integration Flow", True, "Created popup successfully appears in public endpoint")
                        return True
                    else:
                        self.log_test("Integration Flow", False, "Created popup not found in public endpoint")
                        return False
                else:
                    self.log_test("Integration Flow", False, f"Public popups endpoint failed (status: {response.status_code})")
                    return False
            else:
                self.log_test("Integration Flow", False, "No popup created for integration test")
                return False
                
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
            
            # Delete created team member
            if self.created_team_member_id:
                response = requests.delete(f"{self.base_url}/admin/team/{self.created_team_member_id}", headers=headers)
                if response.status_code == 200:
                    self.log_test("Cleanup Team Member", True, "Successfully deleted test team member")
                else:
                    self.log_test("Cleanup Team Member", False, f"Failed to delete team member (status: {response.status_code})")
            
            # Delete created popup
            if self.created_popup_id:
                response = requests.delete(f"{self.base_url}/admin/popups/{self.created_popup_id}", headers=headers)
                if response.status_code == 200:
                    self.log_test("Cleanup Popup", True, "Successfully deleted test popup")
                else:
                    self.log_test("Cleanup Popup", False, f"Failed to delete popup (status: {response.status_code})")
                    
        except Exception as e:
            self.log_test("Cleanup", False, f"Exception during cleanup: {str(e)}")
    
    def run_all_tests(self):
        """Run all Team Management and Popup Management API tests"""
        print("🚀 Starting Team Management and Popup Management API Test Suite")
        print(f"Base URL: {self.base_url}")
        print("=" * 80)
        
        # Test sequence
        tests = [
            # Authentication tests
            self.test_admin_authentication,
            self.test_token_verification,
            
            # Team Management tests
            self.test_team_member_login_manager,
            self.test_team_member_login_agent,
            self.test_admin_get_team_members,
            self.test_admin_create_team_member,
            self.test_admin_update_team_member,
            self.test_admin_change_team_password,
            
            # Popup Management tests
            self.test_get_active_popups_public,
            self.test_admin_get_all_popups,
            self.test_admin_create_popup,
            self.test_admin_update_popup,
            
            # Security and Integration tests
            self.test_role_based_authentication,
            self.test_unauthorized_access_protection,
            self.test_integration_flow
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