import requests

class NumberWindowManager:
    def __init__(self):
        self.window = []
        self.base_url = "http://20.244.56.144/test"
        self.access_token = None

    def register(self):
        """Registration with complete API-compliant payload"""
        registration_data = {
            "companyName": "SRM Institute of Science and Technology",
            "ownerName": "Abhishek A", 
            "rollNo": "RA2211003011636",
            "ownerEmail": "aa6422@srmist.edu.in",
            "accessCode": "SUfGJv"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/register",
                json=registration_data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=15
            )
            response.raise_for_status()
            print("✅ Registration Successful!")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Registration Failed [HTTP {e.response.status_code if e.response else ''}]")
            if e.response:
                print("Error Details:", e.response.text)
            return None

    def get_auth_token(self, client_id, client_secret):
        """Authentication with full error diagnostics"""
        try:
            response = requests.post(
                f"{self.base_url}/auth",
                json={
                    "clientID": client_id,
                    "clientSecret": client_secret
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            auth_data = response.json()
            self.access_token = auth_data.get("access_token")
            
            if not self.access_token:
                raise ValueError("No access token in response")
                
            print("🔑 Authentication Successful!")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"🔒 Auth Failed [HTTP {e.response.status_code if e.response else ''}]")
            if e.response:
                print("Auth Error:", e.response.text)
            return False

    def fetch_numbers(self, endpoint):
        """API call with retry logic"""
        if not self.access_token:
            raise PermissionError("Authentication required first")
            
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Accept": "application/json"
                },
                timeout=10
            )
            response.raise_for_status()
            return [int(num) for num in response.json().get("numbers", [])]
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ {endpoint} Error [HTTP {e.response.status_code if e.response else ''}]: {str(e)}")
            return []

    def update_window(self, new_numbers):
        """Window management with enhanced validation"""
        prev_window = self.window.copy()
        
        # Type conversion and filtering
        valid_numbers = []
        for num in new_numbers:
            try:
                valid_numbers.append(int(num))
            except (ValueError, TypeError):
                continue
                
        # Order-preserving deduplication
        seen = set()
        deduped = []
        for num in reversed(self.window + valid_numbers):
            if num not in seen:
                seen.add(num)
                deduped.append(num)
        self.window = list(reversed(deduped))[-10:]
        
        return {
            "windowPrevState": prev_window,
            "windowCurrState": self.window,
            "numbers": valid_numbers,
            "avg": round(sum(self.window)/len(self.window), 2) if self.window else 0
        }

    def full_operation(self, endpoint):
        """Complete workflow with endpoint testing"""
        try:
            credentials = self.register()
            if not credentials:
                return None
                
            if not self.get_auth_token(credentials.get("clientID"), credentials.get("clientSecret")):
                return None
                
            numbers = self.fetch_numbers(endpoint)
            return self.update_window(numbers)
            
        except Exception as e:
            print(f"🚨 Critical Error: {str(e)}")
            return None

if __name__ == "__main__":
    manager = NumberWindowManager()
    
    # Test all endpoints
    endpoints = ["primes", "fibo", "even", "rand"]
    
    for endpoint in endpoints:
        print(f"\n🔍 Testing {endpoint.upper()} endpoint:")
        result = manager.full_operation(endpoint)
        
        if result:
            print(f"\n📊 {endpoint.capitalize()} Results:")
            print(f"Previous Window: {result['windowPrevState']}")
            print(f"Current Window: {result['windowCurrState']}")
            print(f"New Numbers: {result['numbers']}")
            print(f"Average: {result['avg']:.2f}")
        else:
            print("❌ Endpoint test failed")
