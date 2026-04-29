import requests

BASE_URL = "http://localhost:8000"

def test_login():
    """Test login with admin credentials"""
    print("Testing admin login...")

    # Test data from seed.py
    form_data = {
        'username': 'admin@test.com',
        'password': 'password123',
        'role': 'admin'
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/token", data=form_data)
        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print("✅ Login successful!")
            print(f"Token: {token[:50]}...")

            # Test the /me endpoint
            headers = {'Authorization': f'Bearer {token}'}
            me_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
            if me_response.status_code == 200:
                user_data = me_response.json()
                print("✅ /me endpoint works!")
                print(f"User: {user_data}")
            else:
                print(f"❌ /me endpoint failed: {me_response.status_code}")
                print(me_response.text)

            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing FoodShare Login API")
    print("=" * 40)
    test_login()