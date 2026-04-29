import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test admin login"""
    print("Testing admin login...")
    response = requests.post(f"{BASE_URL}/api/auth/token", json={
        "username": "admin@test.com",
        "password": "password123"
    })
    if response.status_code == 200:
        data = response.json()
        token = data["access_token"]
        print("✅ Admin login successful")
        return token
    else:
        print(f"❌ Admin login failed: {response.status_code} - {response.text}")
        return None

def test_admin_verifications(token):
    """Test admin verifications endpoint"""
    print("Testing admin verifications...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/admin/pending-verifications", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Admin verifications retrieved successfully")
        print(f"   Pending verifications: {len(data)}")
        if data:
            print(f"   First user email: {data[0].get('email', 'NO EMAIL')}")
        return True
    else:
        print(f"❌ Admin verifications failed: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    print("🧪 Testing FoodShare Admin API URLs")
    print("=" * 40)

    # Test admin functionality
    admin_token = test_admin_login()
    if admin_token:
        test_admin_verifications(admin_token)

    print("\n🎉 Testing complete!")