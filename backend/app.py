import requests

class NumberWindowManager:
    def __init__(self):
        self.window = []
        self.base_url = "http://20.244.56.144/test"
        self.access_token = None

    def register(self):
        """Registration with enhanced error logging"""
        registration_data = {
            "companyName": "SRMIST",  # Added required field
            "ownerName": "Abhishek A",  # Added required field
            "rollNo": "RA2211003011636",
            "ownerEmail": "aa6422@srmist.edu.in",  # Changed key from 'email'
            "accessCode": "SUfGJv"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json=registration_data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"  # Added accept header
                },
                timeout=15
            )
            response.raise_for_status()
            print("✅ Registration Successful!")
            print("Server Response:", response.json())  # Debug logging
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Registration Failed [HTTP {response.status_code if response else ''}]")
            if response:  # Added response body inspection
                print("Server Error Details:", response.text)
            return None

    def get_auth_token(self, client_id, client_secret):
        """Authentication with case-sensitive field names"""
        try:
            response = requests.post(
                f"{self.base_url}/auth",
                json={
                    "clientID": client_id,  # Maintain exact case
                    "clientSecret": client_secret
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            auth_data = response.json()
            self.access_token = auth_data.get("access_token")
            if not self.access_token:
                raise ValueError("No access token in response")
            print("🔑 Authentication Successful!")
            
        except requests.exceptions.RequestException as e:
            print(f"🔒 Auth Failed [HTTP {e.response.status_code}]: {e.response.text}")
            raise

    # Rest of the methods remain unchanged...

if __name__ == "__main__":
    manager = NumberWindowManager()
    
    try:
        # Test with different endpoints
        endpoints = ["primes", "fibo", "even", "rand"]
        
        credentials = manager.register()
        if credentials:
            manager.get_auth_token(
                credentials.get("clientID"),
                credentials.get("clientSecret")
            )
            
            for endpoint in endpoints:
                numbers = manager.fetch_numbers(endpoint)
                result = manager.update_window(numbers)
                print(f"\n🔢 {endpoint.capitalize()} Results:")
                print(f"Received Numbers: {result['numbers']}")
                print(f"Current Average: {result['avg']:.2f}")
                
    except Exception as e:
        print(f"🚨 Critical Error: {str(e)}")
