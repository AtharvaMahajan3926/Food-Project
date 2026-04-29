import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test admin login"""
    print("Testing admin login...")
    response = requests.post(f"{BASE_URL}/api/auth/token", json={
        "username": "admin@foodlink.com",
        "password": "admin123"
    })
    if response.status_code == 200:
        data = response.json()
        token = data["access_token"]
        print("✅ Admin login successful")
        return token
    else:
        print(f"❌ Admin login failed: {response.status_code} - {response.text}")
        return None

def test_admin_analytics(token):
    """Test admin analytics endpoint"""
    print("Testing admin analytics...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/admin/analytics", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Admin analytics retrieved successfully")
        print(f"   Total users: {data['total_users']}")
        print(f"   Verified users: {data['verified_users']}")
        print(f"   Unverified users: {data['unverified_users']}")
        print(f"   Total donations: {data['total_donations']}")
        return True
    else:
        print(f"❌ Admin analytics failed: {response.status_code} - {response.text}")
        return False

def test_admin_verifications(token):
    """Test admin verifications endpoint"""
    print("Testing admin verifications...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/admin/verifications", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Admin verifications retrieved successfully")
        print(f"   Pending verifications: {len(data)}")
        return True
    else:
        print(f"❌ Admin verifications failed: {response.status_code} - {response.text}")
        return False

def test_restaurant_login():
    """Test restaurant login (should work since verified)"""
    print("Testing restaurant login...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "restaurant@test.com",
        "password": "password123"
    })
    if response.status_code == 200:
        print("✅ Restaurant login successful (verified)")
        return True
    else:
        print(f"❌ Restaurant login failed: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    print("🧪 Testing FoodShare Admin System")
    print("=" * 40)

    # Test admin functionality
    admin_token = test_admin_login()
    if admin_token:
        test_admin_analytics(admin_token)
        test_admin_verifications(admin_token)

    print()

    # Test verified user access
    test_restaurant_login()

    print("\n🎉 Testing complete!")