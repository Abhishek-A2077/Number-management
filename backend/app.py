import requests
import socket
import urllib3

class NumberWindowManager:
    def __init__(self):
        self.window = []
        self.base_url = "http://20.244.56.144/test"
        self.access_token = None
        urllib3.disable_warnings()  # Disable SSL warnings

    def register(self):
        """Registration with full network diagnostics"""
        print("\n🔧 Starting diagnostic checks...")
        
        # 1. Extract domain from URL
        try:
            domain = self.base_url.split("//")[-1].split("/")[0]
            print(f"🔍 Resolving DNS for: {domain}")
            ip_address = socket.gethostbyname(domain)
            print(f"✅ DNS Resolution Successful → IP: {ip_address}")
        except socket.gaierror:
            print("❌ DNS Error: Could not resolve server address")
            return None

        # 2. Test basic connectivity
        try:
            print(f"📡 Testing connection to server...")
            response = requests.get(self.base_url, timeout=10, verify=False)
            print(f"🏓 Server Response: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Connection Failed: {str(e)}")
            return None

        # 3. Attempt registration
        registration_data = {
            "companyName": "SRM Institute of Science and Technology",
            "ownerName": "Abhishek A",
            "rollNo": "RA2211003011636",
            "ownerEmail": "aa6422@srmist.edu.in",
            "accessCode": "SUfGJv"
        }

        print("\n🚀 Attempting registration with payload:")
        print(registration_data)
        
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json=registration_data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=30,
                verify=False
            )
            
            print(f"\n📊 Registration Response:")
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text[:500]}")  # Show first 500 chars
            
            response.raise_for_status()
            print("✅ Registration Successful!")
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e.response.status_code}")
            if e.response.status_code == 400:
                print("Possible Causes:")
                print("- Invalid registration data format")
                print("- Missing required fields")
                print("- Incorrect access code")
            return None
        except Exception as e:
            print(f"❌ General Error: {str(e)}")
            return None

    def get_auth_token(self, client_id, client_secret):
        """Authentication with enhanced diagnostics"""
        if not client_id or not client_secret:
            print("🔒 Missing client credentials")
            return False
            
        try:
            print(f"\n🔑 Attempting authentication...")
            response = requests.post(
                f"{self.base_url}/auth",
                json={
                    "clientID": client_id,
                    "clientSecret": client_secret
                },
                headers={"Content-Type": "application/json"},
                timeout=15,
                verify=False
            )
            
            print(f"🔐 Auth Response (HTTP {response.status_code}):")
            print(response.text[:200])
            
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
            
            if not self.access_token:
                print("❌ No access token in response")
                return False
                
            print("✅ Authentication Successful!")
            return True
            
        except Exception as e:
            print(f"❌ Auth Failed: {str(e)}")
            return False

    # Keep other methods unchanged from previous versions...

if __name__ == "__main__":
    print("🚀 Starting Full Diagnostic Test")
    manager = NumberWindowManager()
    
    # Phase 1: Registration Test
    credentials = manager.register()
    
    if credentials:
        # Phase 2: Authentication Test
        auth_success = manager.get_auth_token(
            credentials.get("clientID"),
            credentials.get("clientSecret")
        )
        
        if auth_success:
            # Phase 3: Endpoint Testing
            endpoints = ["primes", "fibo", "even", "rand"]
            for endpoint in endpoints:
                print(f"\n🔍 Testing {endpoint.upper()} endpoint:")
                numbers = manager.fetch_numbers(endpoint)
                result = manager.update_window(numbers)
                
                if numbers:
                    print(f"✅ Received {len(numbers)} numbers")
                    print(f"Current Average: {result['avg']:.2f}")
                else:
                    print("❌ No numbers received")
    else:
        print("\n🔴 Critical Failure: Could not register")
